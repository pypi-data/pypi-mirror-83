import http
from abc import ABCMeta, abstractmethod
from collections import Iterable
from typing import List, Optional, BinaryIO

from abejaruntime36.entity.request import Request, Content
from abejaruntime36.entity.response import Response
from abejaruntime36.exception.exceptions import BadRequest, InternalServerError
from abejaruntime36.logging.logger import get_logger
from abejaruntime36 import version

logger = get_logger()

RESPONSE_KEY_STATUS_CODE = 'status_code'
RESPONSE_KEY_CONTENT_TYPE = 'content_type'
RESPONSE_KEY_CONTENT = 'content'
RESPONSE_KEY_METADATA = 'metadata'
DEFAULT_RESPONSE_STATUS_CODE = http.HTTPStatus.OK
DEFAULT_RESPONSE_CONTENT_TYPE = 'text/plain'
KEY_ABEJA_RUNTIME_VERSION = 'x-abeja-sys-meta-runtime-version'


class Converter(object, metaclass=ABCMeta):

    @abstractmethod
    def is_target(self, content_type: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def from_request(self, body: dict) -> Request:
        raise NotImplementedError()

    @abstractmethod
    def from_response(self, resp: dict) -> Response:
        raise NotImplementedError()

    def add_runtime_version(self, metadata: dict = None) -> dict:
        ret = metadata.copy() if metadata else {}
        ret[KEY_ABEJA_RUNTIME_VERSION] = version.VERSION
        return ret


class DefaultConverter(Converter):

    def is_target(self, content_type: str) -> bool:
        return True

    def from_request(self, req: dict) -> Request:
        http_method = req.get('method')
        content_type = req.get('content_type')
        headers = req.get('headers', [])
        ret = Request(str(http_method), str(content_type), headers, None)
        contents = req.get('contents', [])
        if contents is None:
            contents = []
        for c in contents:
            ret.append_content(self._from_content(c))
        return ret

    def from_response(self, resp: dict) -> Response:
        status_code = resp.get(RESPONSE_KEY_STATUS_CODE, DEFAULT_RESPONSE_STATUS_CODE)
        content_type = resp.get(RESPONSE_KEY_CONTENT_TYPE, DEFAULT_RESPONSE_CONTENT_TYPE)
        content = resp.get(RESPONSE_KEY_CONTENT)
        if content is not None:
            if not isinstance(content, Iterable) or isinstance(content, dict) or isinstance(content, str):
                content = [content]
        metadata = resp.get(RESPONSE_KEY_METADATA, None)
        metadata = super().add_runtime_version(metadata)
        return Response(content_type=content_type, contents=content, status_code=status_code, metadata=metadata)

    def _open_file(self, path: str) -> BinaryIO:
        body: BinaryIO
        try:
            body = open(path, "rb")
        except Exception as e:
            logger.error(f'failed to open file[{path}] that including request-body with error {e}')
            raise InternalServerError('failed to load request-body')

        return body

    def _from_content(self, content: dict) -> Content:
        content_type = content.get('content_type', None)
        file_name = content.get('file_name', None)
        form_name = content.get('form_name', None)
        path = content.get('path', None)
        body: Optional[BinaryIO] = None
        if path is not None:
            body = self._open_file(path)
        return Content(content_type=content_type, body=body, file_name=file_name, form_name=form_name)


converters: List[Converter] = [DefaultConverter()]


def convert_from_request(data: dict) -> Request:
    content_type = data.get('content_type', None)
    if content_type is None:
        raise BadRequest('content_type is null')

    for converter in converters:
        if converter.is_target(content_type):
            return converter.from_request(data)
    raise InternalServerError(f'unsupported content_type[{content_type}]')


def convert_from_response(data: dict) -> Response:
    if not isinstance(data, dict):
        raise TypeError('response of user-model is not dict')

    content_type = data.get('content_type', None)
    if content_type is None:
        return DefaultConverter().from_response(data)

    for converter in converters:
        if converter.is_target(content_type):
            return converter.from_response(data)
    raise InternalServerError(f'unsupported content_type[{content_type}]')
