import wrapt
import abc
import copy
import json

__all__ = [
    'WafecDefaultProxy',
    'create_proxy'
]


_simple_types = (int, float, str, bool, complex)
_json_default_encoder_default = json._default_encoder.default


def _is_allowed(x):
    if not isinstance(x, wrapt.ObjectProxy):
        if isinstance(x, dict) or isinstance(x, list) or callable(x) or\
           type(x).__name__ == 'dict_items' or isinstance(x, tuple):
            return True
    if x is not None and type(x) not in _simple_types:
        return True
    return False


def _resolve_json_encoder():
    def default(cls, o):
        if isinstance(o, WafecDefaultProxy):
            return o.__wrapped__
        raise TypeError('')
    json._default_encoder.default = default.__get__(json._default_encoder, _json_default_encoder_default)


def create_proxy(x):
    if _is_allowed(x):
        return WafecDefaultProxy(x)
    return x


class WafecDefaultProxy(wrapt.ObjectProxy, abc.ABC):
    def __init__(self, wrapped):
        super(WafecDefaultProxy, self).__init__(wrapped)
        _resolve_json_encoder()

    def __copy__(self):
        result = copy.copy(self.__wrapped__)
        return create_proxy(result)

    def __deepcopy__(self, memodict={}):
        result = copy.deepcopy(self.__wrapped__, memodict)
        return create_proxy(result)

    def __getitem__(self, item):
        result = self.__wrapped__[item]
        return create_proxy(result)

    def __getattr__(self, item):
        result = getattr(self.__wrapped__, item)
        return create_proxy(result)

    def __call__(self, *args, **kwargs):
        result = self.__wrapped__(*args, **kwargs)
        return create_proxy(result)

    def __iter__(self):
        return WafecDefaultProxyIterator(self.__wrapped__)

    def __reduce__(self):
        result = self.__wrapped__.__reduce__()
        return result

    def __reduce_ex__(self, protocol):
        result = self.__wrapped__.__reduce_ex__(protocol)
        return result


class WafecDefaultProxyIterator:
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.iterator = iter(wrapped)

    def __next__(self):
        result = next(self.iterator)
        return create_proxy(result)
