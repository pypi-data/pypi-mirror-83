from collections import Mapping
from typing import List, Optional, BinaryIO, Dict

KEY_METHOD = 'http_method'
KEY_CONTENT_TYPE = 'content_type'
KEY_HEADERS = 'headers'
KEY_HTTP_HEADERS = 'http_headers'
KEY_CONTENTS = 'contents'
KEY_BODY = 'body'
KEY_FILENAME = 'file_name'
KEY_FORMNAME = 'form_name'


class Content(Mapping):

    def __init__(
            self,
            content_type: Optional[str],
            body: Optional[BinaryIO],
            file_name: Optional[str] = None,
            form_name: Optional[str] = None):
        self.__dict = {
            KEY_CONTENT_TYPE: content_type,
            KEY_BODY: body,
            KEY_FILENAME: file_name,
            KEY_FORMNAME: form_name
        }

    def __getitem__(self, key):
        return self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __contains__(self, item):
        return item in self.__dict

    def __str__(self):
        return str(self.__dict)

    def __eq__(self, o):
        return self.__dict.__eq__(o)

    def __ne__(self, o):
        return self.__dict.__ne__(o)

    def keys(self):
        return self.__dict.keys()

    def items(self):
        return self.__dict.items()

    def values(self):
        return self.__dict.values()

    def get(self, key, default=None):
        return self.__dict.get(key, default)

    def read(self, size: int = -1) -> bytes:
        body = self.__dict.get(KEY_BODY, None)
        if not body:
            raise ValueError('no body')
        return body.read(size)  # type: ignore

    def close(self):
        body = self.__dict.get(KEY_BODY, None)
        if body:
            body.close()


class Request(Mapping):

    def __init__(self, _method: str, _content_type: str, _headers: list = None, _contents: List[Content] = None):
        headers = _headers
        if not headers:
            headers = []
        contents = _contents
        if not contents:
            contents = []

        http_headers = HttpHeaders(headers)
        self.__dict = {
            KEY_METHOD: _method,
            KEY_CONTENT_TYPE: _content_type,
            KEY_HEADERS: headers,
            KEY_HTTP_HEADERS: http_headers,
            KEY_CONTENTS: contents
        }

    def append_content(self, content: Content) -> None:
        contents = self.__dict.get(KEY_CONTENTS, [])
        contents.append(content)  # type: ignore
        self.__dict[KEY_CONTENTS] = contents

    ###############################
    # methods for Mapping
    ###############################

    def __getitem__(self, key):
        return self.__dict[key]

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __contains__(self, item):
        return item in self.__dict

    def __str__(self):
        return str(self.__dict)

    def __eq__(self, o):
        return self.__dict.__eq__(o)

    def __ne__(self, o):
        return self.__dict.__ne__(o)

    def keys(self):
        return self.__dict.keys()

    def items(self):
        return self.__dict.items()

    def values(self):
        return self.__dict.values()

    def get(self, key, default=None):
        return self.__dict.get(key, default)

    ###############################
    # methods for file like object
    ###############################

    def read(self, size: int = -1) -> bytes:
        contents = self.__dict.get(KEY_CONTENTS, [])
        if not contents:
            raise ValueError('no body')
        return contents[0].read(size)  # type: ignore

    def close(self):
        contents = self.__dict.get(KEY_CONTENTS, [])
        for c in contents:
            c.close()


class HttpHeaders(Mapping):
    """HttpHeaders gives interface to get http headers.
    This class is readonly.

    HttpHeaders is partly compatible with with `werkzeug.datastructures.Headers`
    """

    def __init__(self, _headers: List[Dict] = []):
        """
        Input format of headers are,
         [
            {'key': 'accept', 'values': ['*/*']},
            {'key': 'user-agent', 'values': ['curl/7.64.1']},
            {'key': 'xyz', 'values': ['5', '3']},
            {'key': 'zzz', 'values': ['9']}
        ]
        """
        self.__list: List = []
        for item in _headers:
            key = item['key']
            values = item['values']
            for value in values:
                self.__list.append((key, value))

    def get_all(self, key: str):
        """Get all values for a given key.
        header names are case-insensitive.
        """
        ret = []
        lower_case_key = key.lower()
        for _key, _value in self.__list:
            if lower_case_key == _key.lower():
                ret.append(_value)
        return ret

    def __getitem__(self, key: str):
        """Returns the last item for the key out of the values.
        header names are case-insensitive.
        """
        values = self.get_all(key)
        if len(values) == 0:
            return None
        return values[-1]

    def __iter__(self):
        return iter(self.__list)

    def __len__(self):
        return len(self.__list)

    def __contains__(self, key):
        value = self.__getitem__(key)
        return value is not None

    has_key = __contains__

    def __eq__(self, o):
        def lowered(item):
            return (item[0].lower(),) + item[1:]
        return o.__class__ is self.__class__ and set(
            map(lowered, o.__list)
        ) == set(map(lowered, self.__list))

    def __ne__(self, o):
        return not self.__eq__(o)

    def keys(self):
        for item in self.__list:
            yield item[0]

    def items(self):
        for item in self.__list:
            yield item

    def values(self):
        for item in self.__list:
            yield item[1]

    def get(self, key, default=None):
        ret_val = self.__getitem__(key)
        if ret_val is not None:
            return ret_val
        return default
