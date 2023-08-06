import asyncio
import binascii
import json
import os
import struct
import tempfile
from typing import Callable, Optional

from abejaruntime36.converter.converter import convert_from_request, convert_from_response
from abejaruntime36.entity.response import Response
from abejaruntime36.exception.exceptions import HttpError, InternalServerError
from abejaruntime36.logging.logger import get_logger

HEADER = b'\xAB\xE9\xA0'
VERSION = b'\x01'

logger = get_logger()

str_context = os.environ.get('CONTEXT', '{}')
CONTEXT = json.loads(str_context)


class SocketServerProtocol(asyncio.Protocol):
    transport: asyncio.Transport

    def __init__(self, model: Callable):
        self.model = model
        self.msg_part_header = bytearray()
        self.msg_part_len = bytearray()
        self.msg_part_body = bytearray()

    def connection_made(self, transport) -> None:
        self.transport = transport

    def _to_file(self, data: bytes) -> Optional[str]:
        if len(data) < 1:
            return None

        try:
            with tempfile.NamedTemporaryFile(delete=False) as fp:
                filename = fp.name
                fp.write(data)
        except IOError:
            logger.exception(f'failed to write response to {filename}')
            raise InternalServerError(f'failed to write response to {filename}')

        return filename

    def _send_response(self, res: dict) -> None:
        logger.debug(f'send response to proxy: {str(res)}')
        res_bytes = json.dumps(res).encode('utf-8')
        header = HEADER + VERSION + struct.pack('>I', len(res_bytes))
        self.transport.write(header)
        self.transport.write(res_bytes)

    def _transport_error(self, error: HttpError) -> None:
        res = {
            'content_type': 'application/json',
            'error_message': error.message,
            'status_code': error.status_code
        }
        return self._send_response(res)

    def _transport_response(self, resp: Response) -> None:
        try:
            filename = self._to_file(resp.tobytes())
        except HttpError as e:
            self._transport_error(e)
        except Exception:
            logger.exception("failed to transport:")
            return self._transport_error(InternalServerError("unexpected error occurred"))

        res = {
            'content_type': resp.content_type,
            'metadata': resp.metadata,
            'path': filename,
            'status_code': resp.status_code
        }
        self._send_response(res)

    def _parse_data(self, data: bytes) -> Optional[tuple]:
        data_len = len(data)
        header_len = len(self.msg_part_header)
        remain_header_len = 4 - header_len  # HEADER + VERSION = 4 byte
        if remain_header_len > 0:
            self.msg_part_header.extend(data[:remain_header_len])
        if data_len <= remain_header_len:
            return None

        len_len = len(self.msg_part_len)
        remain_len_len = 4 - len_len  # LENGTH-OF-BODY is 4 byte
        pos_len_end = remain_header_len + remain_len_len
        if remain_len_len > 0:
            self.msg_part_len.extend(data[remain_header_len:pos_len_end])
        if data_len <= pos_len_end:
            return None

        ret = None
        (length,) = struct.unpack('>I', self.msg_part_len)
        body_len = len(self.msg_part_body)
        remain_body_len = length - body_len
        pos_body_end = pos_len_end + length
        if remain_body_len > 0:
            self.msg_part_body.extend(data[pos_len_end:pos_body_end])
        if length == len(self.msg_part_body):
            ret = (self.msg_part_header.copy(), self.msg_part_body.decode('utf-8'))
            self.msg_part_header = bytearray()
            self.msg_part_len = bytearray()
            self.msg_part_body = bytearray()
        return ret

    def data_received(self, data: bytes) -> None:
        parsed_data = self._parse_data(data)
        if parsed_data is None:
            return

        header = parsed_data[0]
        if header != (HEADER + VERSION):
            hex_str = str(binascii.hexlify(header), 'utf-8')
            logger.error(f'request received with unsupported header or version: {hex_str}')
            return self._transport_error(InternalServerError('unexpected error occurred'))

        req_body = parsed_data[1]
        try:
            request = json.loads(req_body)
        except Exception:
            logger.exception(f'failed to decode request json from proxy: {req_body}')
            return self._transport_error(InternalServerError('unexpected error occurred'))

        logger.debug(f'request received from proxy: {str(request)}')
        try:
            req_contents = convert_from_request(request)
        except HttpError as e:
            self._transport_error(e)
            return

        try:
            resp = self.model(req_contents, CONTEXT)
            res_content = convert_from_response(resp)
        except Exception:
            logger.exception('unexpected error occurred in user model.')
            self._transport_error(InternalServerError('unexpected error occurred'))
            return
        finally:
            req_contents.close()

        self._transport_response(res_content)

    def connection_lost(self, exc) -> None:
        self.transport.close()
