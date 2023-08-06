import wrapt
import abc
import copy
import json

from wafec_wrapt_custom.utility import fullname, starts_with
from wafec_wrapt_custom.comm.clients import add_proxy_interception_info

__all__ = [
    'WafecDefaultProxy',
    'create_proxy',
    'WafecDefaultProxyIterator',
    'add_to_white_list',
    'create_name'
]


_simple_types = (int, float, str, bool, complex)
_json_default_encoder_default = json._default_encoder.default
_white_list = ['nova.', 'glance.', 'neutron.', 'cinder.']

_default_add_proxy_interception_info = add_proxy_interception_info


def set_default_add_proxy_interception_info(new_func):
    global _default_add_proxy_interception_info
    _default_add_proxy_interception_info = new_func


def create_name(*args):
    name = ''
    for arg in [arg for arg in args if arg]:
        if type(arg) not in _simple_types and type(arg) not in (list, dict, tuple):
            name += fullname(arg) + ' '
        else:
            name += str(arg) + ' '
    return name.strip()


def add_to_white_list(item):
    global _white_list
    _white_list.append(item)


def _is_allowed(x):
    if not isinstance(x, wrapt.ObjectProxy):
        if isinstance(x, dict) or isinstance(x, list) or callable(x) or\
           type(x).__name__ == 'dict_items' or isinstance(x, tuple):
            return True
        if x is not None and type(x) not in _simple_types:
            if starts_with(_white_list, fullname(x)):
                return True
    return False


def _resolve_json_encoder():
    def default(cls, o):
        if isinstance(o, WafecDefaultProxy):
            return o.__wrapped__
        raise TypeError('')
    json._default_encoder.default = default.__get__(json._default_encoder, _json_default_encoder_default)


def create_proxy(x, trace=None):
    if _is_allowed(x):
        return WafecDefaultProxy(x, trace=trace)
    return x


class WafecDefaultProxy(wrapt.ObjectProxy, abc.ABC):
    def __init__(self, wrapped, trace=None):
        super(WafecDefaultProxy, self).__init__(wrapped)
        self._self_trace = trace

        _resolve_json_encoder()

    def __copy__(self):
        result = copy.copy(self.__wrapped__)
        return create_proxy(result)

    def __deepcopy__(self, memodict={}):
        result = copy.deepcopy(self.__wrapped__, memodict)
        return create_proxy(result)

    def __getitem__(self, item):
        trace = create_name(self._self_trace, f'[{item}]')
        _default_add_proxy_interception_info(item, x=self.__wrapped__, trace=trace)
        result = self.__wrapped__[item]
        return create_proxy(result, trace=trace)

    def __getattr__(self, item):
        trace = create_name(self._self_trace, f'.{item}')
        _default_add_proxy_interception_info(item, x=self.__wrapped__, trace=trace)
        result = getattr(self.__wrapped__, item)
        return create_proxy(result, trace=trace)

    def __call__(self, *args, **kwargs):
        result = self.__wrapped__(*args, **kwargs)
        return create_proxy(result, trace=self._self_trace)

    def __iter__(self):
        return WafecDefaultProxyIterator(self._self_trace, self.__wrapped__)

    def __reduce__(self):
        result = self.__wrapped__.__reduce__()
        return result

    def __reduce_ex__(self, protocol):
        result = self.__wrapped__.__reduce_ex__(protocol)
        return result


class WafecDefaultProxyIterator:
    def __init__(self, self_trace, wrapped):
        self.self_trace = self_trace
        self.wrapped = wrapped
        self.iterator = iter(wrapped)
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = next(self.iterator)
        self.n += 1
        trace = create_name(self.self_trace, f'[{self.n - 1}]')
        return create_proxy(result, trace=trace)
