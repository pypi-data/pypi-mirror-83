import asyncio
import functools
import os
import signal
import sys

from abejaruntime36.exception.exceptions import ModelSetupException
from abejaruntime36.logging.logger import get_logger
from abejaruntime36.model.model import setup_model
from abejaruntime36.server_protocol import SocketServerProtocol
from abejaruntime36 import version

DEFAULT_HANDLER = 'main:handler'

loop: asyncio.AbstractEventLoop
logger = get_logger()


def signal_handler(signame):
    logger.warning(f"runtime: signal [{signame}] received")
    global loop
    loop.stop()


def main():
    logger.info(f'start executing model with abeja-runtime-python (version: {version.VERSION})')

    socket_path = os.environ.get('ABEJA_IPC_PATH', None)
    if socket_path is None:
        logger.error("specify ABEJA_IPC_PATH for Inter Process Communication")
        sys.exit(1)

    handler = os.environ.get('HANDLER', DEFAULT_HANDLER)
    try:
        model = setup_model(handler)
    except ModelSetupException:
        logger.warning("failed to setup model", exc_info=True)
        sys.exit(1)

    global loop
    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(signal_handler, signame))

    def get_protocol_factory() -> SocketServerProtocol:
        return SocketServerProtocol(model)

    server_coroutine = loop.create_unix_server(get_protocol_factory, socket_path)
    server = loop.run_until_complete(server_coroutine)

    try:
        loop.run_forever()
    except Exception:
        logger.exception("unexpected error")
    finally:
        server.close()
        loop.close()
        os.remove(socket_path)


if __name__ == "__main__":
    main()
