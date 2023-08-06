import os
import subprocess
import sys
import importlib
from collections import deque
from pathlib import Path
from typing import Callable, Optional, List

from abejaruntime36.exception.exceptions import ModelSetupException
from abejaruntime36.logging.logger import get_logger

CONFIGURE_BASE_DIRECTORY = '.abeja'
WORKING_DIRECTORY_SEARCH_DEPTH = 3

logger = get_logger()


def _find_working_dir() -> Optional[str]:
    """
    Let the working directory be the path where the .abeja directory resides.

    """
    base_path = Path(os.curdir)
    base_depth = str(base_path.resolve()).count(os.sep)
    q: deque = deque([])
    q.append(base_path)
    while len(q) > 0:
        p = q.popleft()
        for child in p.iterdir():
            current_depth = str(child.resolve()).count(os.sep)
            if child.is_dir():
                if child.name == CONFIGURE_BASE_DIRECTORY:
                    return str(child.parent.resolve())
                else:
                    if (current_depth - base_depth) > WORKING_DIRECTORY_SEARCH_DEPTH:
                        continue
                    q.append(child)
    return None


def _install_packages() -> None:
    if os.path.exists('Pipfile'):
        logger.info('start installing packages from Pipfile')
        _install_from_pipfile()
        logger.info('packages are installed from Pipfile')
    elif os.path.exists('requirements.txt'):
        logger.info('start installing packages from requirements.txt')
        _install_from_requirements_txt()
        logger.info('packages are installed from requirements.txt')
    else:
        logger.info('requirements.txt/Pipfile not found, skip installing dependencies process')


def _install_from_pipfile() -> None:
    commands = ['pipenv', 'install', '--system']
    if not os.path.exists('Pipfile.lock'):
        commands.append('--skip-lock')
    _wait_subprocess(commands)


def _install_from_requirements_txt(requirements_path: str = 'requirements.txt') -> None:
    """installs python packages described in requirements
    Args:
        requirements_path:
    Returns:
        ``True`` if pip install succeeded.
        ``False`` if requirements.txt not found.
    Raises:
        CalledProcessError - failed to `pip install`
    """
    _wait_subprocess(['pip', 'install', '-r', requirements_path])


def _import_model(handler: str) -> Callable:
    """loads user model identified by handler
    Args:
        handler: path to the handler of user definied model
    Returns:
        function object of user defined model
    Raises:
        ImportError: failed to import user definied model
    """

    if handler.count(':') != 1:
        raise ImportError(
            'Possibility, your HANDLER[{}] parameter is wrong. '
            'handler needs one ":" separator. The format is <module>:<function>.'
            .format(handler))

    module_name, func_name = handler.split(':', 1)

    # Temporarily modify sys.path to include current working directory.
    if '' not in sys.path:
        sys.path.insert(0, '')

    try:
        model = getattr(importlib.import_module(module_name), func_name)
    except ImportError as e:
        raise ImportError(
            "Couldn't import a module named [{}] specified in HANDLER[{}]. "
            "Possibly, your HANDLER parameter or packaging (zip/tar) file structure is wrong. {}"
            .format(module_name, handler, e.__str__()))
    except AttributeError:
        raise ImportError(
            "Couldn't import a function named [{}] specified in HANDLER[{}]. "
            "Possibly, your HANDLER parameter or packaging (zip/tar) file structure is wrong."
            .format(func_name, handler))

    return model


def _wait_subprocess(command: List[str], max_wait: int = 5) -> None:
    """
    run and wait subprocess.
    Args:
        command (List[str]): command
        max_wait (int): max seconds to wait for subprocess to finish after closing stdout/err

    Returns:
        None

    Raises:
        RuntimeError
    """
    future = _run(command)
    for line in iter(future.stdout.readline, b''):
        logger.info(line.decode('utf-8'))

    try:
        returncode = future.wait(max_wait)
    except subprocess.TimeoutExpired:
        raise RuntimeError('subprocess did not exit after {} seconds'.format(max_wait))
    if returncode != 0:
        raise RuntimeError('subprocess finished with exit code {}'.format(future.returncode))


def _run(command: List[str]) -> subprocess.Popen:
    """
    run subprocess with specified *command*.
    Args:
        command (List[str]): command

    Returns:
        subprocess.Popen:
    """
    try:
        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except (OSError, ValueError) as e:
        raise RuntimeError(e)


def setup_model(handler: str) -> Callable:
    working_dir = _find_working_dir()
    if working_dir:
        logger.debug('found .abeja directory in {}.'.format(working_dir))
        try:
            os.chdir(working_dir)
        except Exception as e:
            raise ModelSetupException(str(e))

    try:
        _install_packages()
    except RuntimeError as e:
        logger.exception(
            'error while installing from requirements.txt/Pipfile:')
        tb = sys.exc_info()[2]
        raise ModelSetupException(e).with_traceback(tb)

    try:
        logger.info("Loading user model handler with {}...".format(handler))
        model = _import_model(handler)
        return model
    except ImportError as e:
        logger.exception('error while importing user model')
        raise ModelSetupException('Exception occurred while loading handler function: {}'.format(str(e)))
