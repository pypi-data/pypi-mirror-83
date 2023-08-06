import docstring_parser
import inspect

from typing import List
from case_convert import kebab_case

from .typing import GruiType


# This class allow us to generate the url path from the name of the class
# If the developer want to specify a specific name he can use the _url_prefix class variable
class _AbstractGruiServiceMeta(type):

    @property
    def url_prefix(cls):
        try:
            name = cls.__dict__["_url_prefix"]
        except KeyError:
            name = kebab_case(cls.__name__)
            if name.endswith('-service'):
                name = name[:-8]
        return name

    def generate_doc(cls, app):
        docstring_parsed = docstring_parser.parse(cls.__doc__)
        result = {
            'name': cls.url_prefix,
            'methods': [],
            'presentation': docstring_parsed.short_description,
            'description': docstring_parsed.long_description,
        }

        for func_id in app.registered_function:
            func_doc = app.registered_function[func_id]
            if func_doc.path.startswith(cls.url_prefix, 1):
                result["methods"].append(func_id)
        return result


class AbstractGruiService(metaclass=_AbstractGruiServiceMeta):
    pass


class GruiDocService(AbstractGruiService):
    from .decorator import _Grui, NotFoundIfEmpty, NotFoundIfNone, MultipleCallAtOnce
    from .app import GruiApp

    _url_prefix = "grui"

    def __init__(self, app: GruiApp):
        self._app = app

    @_Grui("title")
    def get_title(self):
        return self._app.title

    @_Grui("function/all")
    @NotFoundIfEmpty
    def get_all_function_doc(self):
        return self._app.registered_function.values()

    @_Grui("function/<id_>")
    @NotFoundIfNone
    @MultipleCallAtOnce
    def get_function_doc(self, id_: int):
        return self._app.registered_function.get(id_, None)

    @_Grui("service/all")
    @NotFoundIfEmpty
    def get_all_service_doc(self):
        return self._app.service_doc.values()

    @_Grui("service/<name>")
    @NotFoundIfNone
    @MultipleCallAtOnce
    def get_service_doc(self, name: str):
        return self._app.service_doc.get(name, None)

    @_Grui("type/all")
    @NotFoundIfEmpty
    def get_all_type_doc(self) -> List[GruiType]:
        return self._app.registered_type.values()

    @_Grui("type/<name>")
    @NotFoundIfNone
    @MultipleCallAtOnce
    def get_type_doc(self, name: str) -> GruiType:
        return self._app.registered_type.get(name, None)
