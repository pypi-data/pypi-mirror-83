import json

from typing import List


def dict2list(dict_: dict) -> List[dict]:
    """:return A list of dict where every dict contains one value"""
    result = []
    for key in dict_:
        for i, value in enumerate(dict_[key]):
            try:
                result[i][key] = value
            except IndexError:
                result.append({key: value})
    return result


# def type_as_string(type_) -> str:
#     if type_ is None:
#         return "unknown"
#     if isinstance(type_, typing._GenericAlias):
#         res = ""
#         if len(type_.__args__) > 0:
#             res = "["
#             for arg in type_.__args__:
#                 res += type_as_string(arg) + ", "
#             res = res[:-2]
#             res += "]"
#         return "GenericAlias" + res
#     else:
#         return type_.__name__


_DICT_VALUES_TYPE = type({}.values())
_DICT_KEYS_TYPE = type({}.keys())


class GruiJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        from .typing import GruiJsonSerializable

        if isinstance(obj, _DICT_VALUES_TYPE) or isinstance(obj, _DICT_KEYS_TYPE):
            return tuple(obj)
        elif isinstance(obj, GruiJsonSerializable):
            return obj.to_json()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
