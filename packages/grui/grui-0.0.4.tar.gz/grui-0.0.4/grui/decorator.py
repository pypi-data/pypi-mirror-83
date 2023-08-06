import docstring_parser
import re
import inspect

from abc import ABC, abstractmethod
from case_convert import snake_case, upper_case
from typing import *

from .typing import GruiModel, GruiSubModel, GruiType


##########
# Errors #
##########
class InitialisationFunctionError(RuntimeError):
    pass


####################
# Module variables #
####################
MAX_ARGUMENT_PATTERN = re.compile("\\(max: (\\d+.?\\d*)\\)", re.IGNORECASE)
MIN_ARGUMENT_PATTERN = re.compile("\\(min: (\\d+.?\\d*)\\)", re.IGNORECASE)


###########
# Classes #
###########
class GruiFunction(GruiModel):
    """
    Every function decorated by any GruiDecorator will be replace by an instance of this class.
    Like that the GruiApp will be able to expose this function (or method if the function is define into a class)
    """
    class Argument(GruiSubModel):
        type: GruiType
        description: str
        condition: Dict[str, Any]
        optional: bool

    class Result(GruiSubModel):
        type: GruiType
        description: str

    ##############
    # Attributes #
    ##############
    id: int
    path: str
    method: str
    args: Dict[str, Argument]
    presentation: str
    description: str
    result: Optional[Result]
    depreciated: bool

    ###############
    # Constructor #
    ###############
    def __init__(self, callable_, grui_decorator):
        super().__init__()
        self.__instance = None
        self.__owner = None
        self.__properties_updated = False
        self._http_path = ""
        self._http_method = ""
        self.__args = {}
        self.__presentation = ""
        self.__description = ""
        self.__result = None
        self.default_return_code = 200  # HTTP code for OK
        self.previous_actions = []
        self.next_actions = []
        self.multiple_action = False
        if isinstance(callable_, GruiFunction):
            self.id = callable_.id
            self.__callable = callable_.__callable
            self.__grui_decorators = callable_.__grui_decorators
            if self.__properties_updated:
                raise InitialisationFunctionError
        else:
            self.id = id(callable_)
            self.__callable = callable_
            self.__grui_decorators = []
        self.__grui_decorators.append(grui_decorator)

    ###########
    # Getters #
    ###########
    @property
    def __code__(self):
        return self.__callable.__code__

    @property
    def __defaults__(self):
        return self.__callable.__defaults__

    @property
    def __kwdefaults__(self):
        return self.__callable.__kwdefaults__

    # Can not override annotation because of the grui model
    # The signature need to get the attribute of the GruiFunction
    #@property
    #def __annotations__(self):
    #    return self.__callable.__annotations__

    @property
    def __name__(self):
        if self.__owner:
            return "%s.%s.%s" % (self.__callable.__module__, self.__owner.__name__, self.__callable.__name__)
        else:
            return "%s.%s" % (self.__callable.__module__, self.__callable.__name__)

    # To trick the inspect python module we override the 5 previous properties:
    # code, defaults, kwdefaults, annotation and name.
    # Like that the method inspect.signature() return the same result as an undecorated function.

    @property
    def callable(self):
        return self.__callable

    @property
    def path(self):
        self.__update_properties()
        return "/api" + self._http_path

    @property
    def method(self):
        self.__update_properties()
        return self._http_method

    @property
    def args(self):
        self.__update_properties()
        return self.__args

    @property
    def presentation(self):
        self.__update_properties()
        return self.__presentation

    @property
    def description(self):
        self.__update_properties()
        return self.__description

    @property
    def result(self):
        self.__update_properties()
        return self.__result

    @property
    def __doc__(self):
        return self.__callable.__doc__

    @property
    def is_method(self):
        return self.__owner is not None

    @property
    def instance_class(self):
        return self.__owner

    ###########
    # Methods #
    ###########
    def __get__(self, instance, owner):
        # We save the instance of the object from the method class. In case the function is a method
        self.__instance = instance
        self.__owner = owner
        return self

    def __call__(self, *args, **kwargs):
        # Invoked on every call of any decorated method
        if self.__instance:
            return self.__callable(self.__instance, *args, **kwargs)
        else:
            return self.__callable(*args, **kwargs)

    def validate(self):
        return True

    #def to_json(self):
    #    self.__update_properties()
    #    return super().to_json()

    def __update_properties(self):
        if not self.__properties_updated:
            # Update the properties by the decorators
            for grui_decorator in self.__grui_decorators:
                grui_decorator.update_props(self)

            # Parse the docstring to get the documentation
            doc_parsed = docstring_parser.parse(self.__callable.__doc__)
            self.__presentation = doc_parsed.short_description or ""
            self.__description = doc_parsed.long_description or ""
            if doc_parsed.deprecation is None:
                self.depreciated = False

            # Save the parameter description into a temporary map.
            parameter_doc_by_name = {}
            for param_doc in doc_parsed.params:
                parameter_doc_by_name[param_doc.arg_name] = param_doc

            signature = inspect.signature(self.__callable)
            if signature.return_annotation != inspect.Signature.empty:
                self.__result = GruiFunction.Result(
                    description="" if doc_parsed.returns is None else doc_parsed.returns.description,
                    type=GruiType.get_instance(signature.return_annotation)
                )

            for param_name in signature.parameters:
                if param_name == "self":
                    continue
                annotation = self.__callable.__annotations__.get(param_name)
                parameter_doc = parameter_doc_by_name.get(param_name)
                description = ""
                optional = False
                condition = {}

                if parameter_doc is not None and annotation is not None:
                    description = parameter_doc.description
                    optional = parameter_doc.is_optional or False

                    # Parse the description to extract the condition
                    if annotation in (int, float):
                        max_value_match = re.search(MAX_ARGUMENT_PATTERN, description)
                        min_value_match = re.search(MIN_ARGUMENT_PATTERN, description)
                        if max_value_match is not None:
                            description = re.sub(MAX_ARGUMENT_PATTERN, "", description, 1).strip()
                            condition['max'] = annotation(max_value_match.group(1))
                        if min_value_match is not None:
                            description = re.sub(MIN_ARGUMENT_PATTERN, "", description, 1).strip()
                            condition['min'] = annotation(min_value_match.group(1))

                self.__args[param_name] = GruiFunction.Argument(
                    type=GruiType.get_instance(annotation),
                    description=description,
                    condition=condition,
                    optional=optional
                )

            tt = self.__callable.__name__
            if self.__callable.__name__.startswith("get") and self.__presentation == "" and \
                    self.__result is not None and self.__result.description != "":
                self.__presentation = "Retrieve " + self.__result.description[0].lower() + self.__result.description[1:]

            self.__properties_updated = True


#############
# Decorator #
#############
def _grui_decorator(default_param=()):
    def __inner(cls):
        def ___wrapper(*args, **kwargs):
            if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
                # actual decorated function
                return cls(*default_param)(*args)
            else:
                # decorator arguments
                return lambda *a, **kw: cls(*args, **kwargs)(*a, **kw)
        return ___wrapper
    return __inner


class _AbstractGruiDecorator(ABC):

    # This function is doing nothing but keep to avoid getting warning during Intellij inspections
    def __init__(self, *args):
        pass

    def __call__(self, action):
        return GruiFunction(action, self)

    @abstractmethod
    def update_props(self, grui_function: GruiFunction):
        pass


class _AbstractHttpRoute(_AbstractGruiDecorator):

    __REPLACE_SLASH_REGEX = re.compile("//+/")

    def __init__(self, path):
        self.path = path

    def update_props(self, grui_function: GruiFunction):
        if grui_function.is_method:
            tmp = grui_function.instance_class.url_prefix + "/" + (self.path or "")
        else:
            if self.path is None:
                tmp = snake_case(grui_function.__name__).replace(".", "-")
            else:
                tmp = self.path
        grui_function._http_path = "/" + _AbstractHttpRoute.__REPLACE_SLASH_REGEX.sub("/", tmp).strip("/")
        grui_function._http_method = upper_case(self.__class__.__name__)


@_grui_decorator((None,))
class Get(_AbstractHttpRoute):
    pass


@_grui_decorator((None,))
class Post(_AbstractHttpRoute):

    def update_props(self, grui_function: GruiFunction):
        super().update_props(grui_function)
        grui_function.default_return_code = 201  # HTTP code for Created


@_grui_decorator((None,))
class Put(_AbstractHttpRoute):
    pass


@_grui_decorator((None,))
class Delete(_AbstractHttpRoute):
    pass


@_grui_decorator((None,))
class _Grui(_AbstractHttpRoute):
    pass


@_grui_decorator(())
class NotFoundIfNone(_AbstractGruiDecorator):

    def update_props(self, grui_function: GruiFunction):
        def _(result: Any, code: int):
            if result is None:
                return None, 404  # HTTP code for Not found
            return result, code
        grui_function.next_actions.append(_)


@_grui_decorator(())
class NotFoundIfEmpty(_AbstractGruiDecorator):

    def update_props(self, grui_function: GruiFunction):
        def _(result: Any, code: int):
            if len(result) == 0:
                return None, 404  # HTTP code for Not found
            return result, code
        grui_function.next_actions.append(_)


@_grui_decorator(())
class MultipleCallAtOnce(_AbstractGruiDecorator):

    def update_props(self, grui_function: GruiFunction):
        grui_function.multiple_action = True
