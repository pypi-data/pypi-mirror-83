"""This module contains data types used by model developers."""
import array
import cgi
import csv
import http
import json
from collections import OrderedDict
from collections.abc import ByteString
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from abejaruntime36.helper.json_encoder import BetterJSONEncoder

OrderedKeyPairs = List[Tuple[str, Any]]

Content = Union[Dict, bytes]

Input = Union[OrderedKeyPairs, Content]

Metadata = Tuple[str, str]


class Response:
    """The data wrapper class to specify detail information of output content.

    Initialization
    ==============

    A ``Response`` object can be initialized with *content_type*, *contents* and *status_code*.
    The *contents* parameter is an *iterable* object containing elements of which
    type is one of below:

    - `bytes-like object`
    - ``dict``
    - ``list`` of key-value tuple (e.g. ``[(key, value), ...]``)

    >>> Response('text/plain', [b'Hello, World!'])
    <abejaruntime36.entity.response.Response object at 0x...>
    >>> Response('application/json', [{'apple': 103, 'orange': 250}])
    <abejaruntime36.entity.response.Response object at 0x...>
    >>> Response('application/json', [
    ...     [('apple', 103), ('orange', 250)],
    ...     [('apple', 345), ('orange', 87)]
    ... ])
    <abejaruntime36.entity.response.Response object at 0x...>

    You can specify status_code (e.g. HTTP Status Code) as the *status_code* parameter.
    A parameter can be ``http.HTTPStatus``:

    >>> Response('application/json', [{'status': 'bad request'}], status_code=HTTPStatus.BAD_REQUEST)
    <abejaruntime36.entity.response.Response object at 0x...>

    Default value of *status_code* is HTTPStatus.OK .

    You can specify HTTP headers as *metadata* parameter.
    A parameter can be ``dict``:

    >>> r = Response('text/plain; charset=utf-8', [b'Hello, World!'], metadata={'Retry-After', '100'})
    >>> r.metadata
    {'Retry-After', '100'}
    >>> r.mimetype
    'text/plain'

    Iterating contents
    ==================

    An instance of ``Response`` class is also an *iterator* of contents. You can read
    contents of a response by iterating partial contents with ``for`` loop.

    >>> r = Response([{'id': 1}, {'id': 2}])
    >>> for content in r:
    ...     print(content)
    ...
    {'id': 1}
    {'id': 2}

    Each partial content can be one of:

    - `bytes-like object`_
    - ``dict`` or ``collections.OrderedDict``

    If a partial content is ``list`` of key-value tuple, it will be converted to
    ``collections.OrderedDict``.

    >>> r = Response('application/json', [
    ...     [('apple', 103), ('orange', 250)],
    ...     [('apple', 345), ('orange', 87)]
    ... ])
    >>> list(r)
    [OrderedDict([('apple', 103), ('orange', 250)]), OrderedDict([('apple', 345), ('orange', 87)])]

    Like read-only I/O object, once you read the contents of a response,
    you can't read the contents anymore.

    >>> r = Response([{'id': 1}, {'id': 2}])
    >>> list(r)
    [{'id': 1}, {'id': 2}]
    >>> list(r)
    []

    .. _bytes-like object: https://docs.python.org/3/glossary.html#term-bytes-like-object
    """

    def __init__(self,
                 content_type: str,
                 contents: Optional[Iterable[Input]],
                 status_code: http.HTTPStatus = http.HTTPStatus.OK,
                 metadata: Dict[str, str] = None):
        if content_type is None or content_type.strip() == '':
            raise ValueError("need content_type")

        self.__content_type = content_type
        self.__status_code = status_code
        self.__iter = iter(contents) if contents else iter([])
        self.__metadata = metadata if metadata else {}

    def __iter__(self):
        return self

    def __next__(self) -> Content:
        element = next(self.__iter)

        # We have to convert an element to an instance of ``OrderedDict``
        # if it is a list of key-value tuples. However precisely checking
        # the type can be expensive, so we try to convert it if it is a list.
        if isinstance(element, list):
            try:
                return OrderedDict(element)
            except TypeError:
                pass
        return element  # type: ignore

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def status_code(self) -> http.HTTPStatus:
        return self.__status_code

    @property
    def metadata(self) -> Dict[str, str]:
        """Return an metadata.

        >>> r = Response("application/json", [], metadata={'Retry-After': '100'})
        >>> r.metadata
        {'Retry-After', '100'}
        """
        return self.__metadata

    @property
    def mimetype(self) -> Optional[str]:
        """Return the media type.

        This function parses *content_type* value and return MIME type part without options.
         e.g. ``application/json``.

        >>> r = Response("text/plain; charset=utf8", [])
        >>> r.mimetype
        'text/plain'
        """
        media_type, _options = cgi.parse_header(self.__content_type)
        return media_type.lower() if media_type else None

    class ByteBuffer(object):

        def __init__(self):
            self.buffer = []

        def extend(self, obj: bytes) -> None:
            self.buffer.append(obj)

        def write(self, content: str) -> None:
            self.buffer.append(content.encode('utf-8'))

        def empty(self) -> bool:
            """Return ``True`` if the queue is empty, ``False`` otherwise."""
            return len(self.buffer) == 0

        def tobytes(self) -> bytes:
            # Avoid copying buffered content if possible.
            if len(self.buffer) == 1:
                return self.buffer[0]
            else:
                return b''.join(self.buffer)

    def tobytes(self) -> bytes:
        r"""Convert the contents to ``bytes`` representation.

        Convertion Rules
        ================

        To convert its contents to ``bytes``, this method iterates elements and:

        1. If the element is a bytes-like object, no convertion happen.
        2. If ``Content-Type`` is ``text/csv``, use ``csv.DictWriter`` to
           convert it into csv format.
        3. Otherwise, convert it into json format by ``json.dumps``.
        4. To make it separated by newlines, insert newline characters appropriately.

        Examples
        ========

        *Bytes-like object*

        >>> r = Response('text/plain', [b'Hello, ', b'World!'])
        >>> r.tobytes()
        b'Hello, World!'

        *CSV*

        >>> r = Response('text/csv', [
        ...     [('apple', 103), ('orange', 250)],
        ...     [('apple', 345), ('orange', 87)]
        ... ])
        >>> r.tobytes()
        b'apple,orange\r\n103,250\r\n345,87\r\n'

        *JSON*

        >>> r = Response('application/json', [{'id': 123}])
        >>> r.tobytes()
        b'{"id": 123}'

        *JSON Lines*

        >>> r = Response('application/json', [
        ...     [('apple', 103), ('orange', 250)],
        ...     [('apple', 345), ('orange', 87)]
        ... ])
        >>> r.tobytes()
        b'{"apple": 103, "orange": 250}\n{"apple": 345, "orange": 87}'
        """
        buffer = Response.ByteBuffer()
        mimetype = self.mimetype
        csv_writer = None

        # TODO: Should we handle `str` object by encoding it with `charset` option in
        # `Content-Type`?
        for c in self:
            # Test an object is a bytes-like object.
            if isinstance(c, ByteString) or isinstance(c, array.array):
                buffer.extend(c)  # type: ignore
            elif isinstance(c, str):
                if not buffer.empty():
                    buffer.extend(b'\n')
                buffer.extend(c.encode('utf-8'))
            else:
                if mimetype == 'text/csv':
                    if not csv_writer:
                        csv_writer = csv.DictWriter(buffer, c.keys())
                        csv_writer.writeheader()

                    csv_writer.writerow(c)
                else:
                    if not buffer.empty():
                        # JSON serialization text should always be start at
                        # the begining of a line.
                        buffer.extend(b'\n')

                    buffer.write(json.dumps(c, cls=BetterJSONEncoder))

        return buffer.tobytes()
