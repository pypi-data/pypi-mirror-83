import typing
import re
import inspect
import docstring_parser

from typing import *
from abc import ABC, abstractmethod
from case_convert import snake_case, camel_case


##########
# Errors #
##########
class UpdateIdError(RuntimeError):
    def __init__(self, message="Trying to update the id", **kwargs):
        super().__init__(message, kwargs)


class IncorrectDataWhileEncodingError(RuntimeError):
    def __init__(self, message="Trying to encode with incorrect data", wrong_model=None, **kwargs):
        tmp = {}
        if wrong_model:
            for key in wrong_model._GruiModel__initial_attr:
                tmp[key] = wrong_model.__getattribute__(key)
        super().__init__(message, tmp, **kwargs)


class DuplicateTypeError(RuntimeError):
    pass


##############
# Interfaces #
##############
class GruiJsonSerializable(ABC):
    """
    This class is an abstract one. It works like a interface. It simply consist to declare the function to_json.
    Like that an simple check isinstance() is enough to safely serialize to the Json format.
    """
    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        pass


################
# Meta classes #
################
class _GruiModelMeta(type(GruiJsonSerializable)):
    """
    Meta class to implement the grui_attributes property to any class inherited from 'GruiModel'
    """
    __grui_attributes = {}

    @property
    def grui_attributes(cls) -> Dict[str, "GruiTypeModelAttribute"]:
        from .decorator import GruiFunction

        if cls.__grui_attributes.get(cls) is None:
            cls.__grui_attributes[cls] = {}
            signature = inspect.signature(cls.__init__)
            for name, type_ in get_type_hints(cls).items():
                attr = GruiTypeModelAttribute()
                attr.type = GruiType.get_instance(type_)
                attr.read_only = name == "id"
                attr.description = ""
                try:
                    tmp = signature.parameters[name].default
                    attr.default_value = tmp if tmp != inspect.Parameter.empty else None
                except KeyError:
                    attr.default_value = None
                cls.__grui_attributes[cls][name] = attr

            if cls != GruiFunction and cls.__doc__ is not None:
                doc_parsed = docstring_parser.parse(cls.__doc__)
                for attribute in doc_parsed.params:
                    if attribute.arg_name in cls.__grui_attributes[cls].keys() and attribute.description is not None:
                        cls.__grui_attributes[cls][attribute.arg_name].description = attribute.description

        return cls.__grui_attributes[cls]


###########
# Classes #
###########
class GruiModel(GruiJsonSerializable, metaclass=_GruiModelMeta):
    """
    Base class of the of any object model saved and use by the application.
    This class allow developer to focus mainly on how the data it saved and related to eachother.
    The class require to have a id. It type can be change but I always recommend to set it optional.
    """

    ##############
    # Attributes #
    ##############
    id: Optional[int]

    ###############
    # Constructor #
    ###############
    def __init__(self, **kwargs):
        self.__id = None
        self.__json_result = None
        self.__initial_attr = kwargs.keys()
        for attr_name, attr_value in kwargs.items():
            self.__setattr__(attr_name, attr_value) 

    ##########
    # Getter #
    ##########
    @property
    def id(self):
        return self.__id

    ##########
    # Setter #
    ##########
    @id.setter
    def id(self, id_: int):
        if self.__id is None:
            self.__id = id_
        else:
            raise UpdateIdError()

    def __setattr__(self, key, value):
        self.__dict__["_GruiModel__json_result"] = None
        super().__setattr__(key, value)

    ###########
    # Methods #
    ###########
    def to_json(self):
        if not self.validate():
            raise IncorrectDataWhileEncodingError(self.__class__.__name__)
        if self.__json_result is None:
            json_result = {}
            tmp = self.__class__
            for attr_name, attr in self.__class__.grui_attributes.items():
                toto = self.__getattribute__(attr_name)
                json_result[camel_case(attr_name)] = attr.type.jsonify_value(self.__getattribute__(attr_name))
            self.__json_result = json_result
        return self.__json_result

    def validate(self) -> bool:
        for attr_name, attr in self.__class__.grui_attributes.items():
            try:
                attr_value = self.__getattribute__(attr_name)
            except AttributeError:
                attr_value = None
                self.__setattr__(attr_name, attr_value)
            valid, attr_validated = attr.type.validate_value(attr_value)
            if not valid:
                return False
            elif attr_validated != attr_value:
                if attr_name == "id":
                    self.__dict__["_GruiModel__id"] = attr_validated
                else:
                    self.__setattr__(attr_name, attr_validated)
        return True

    @classmethod
    def from_json(cls, values: Any) -> "GruiModel":
        parameters = {}
        if isinstance(values, dict):
            for key in values:
                parameters[snake_case(key)] = values[key]
            return cls(**parameters)
        else:
            return cls(values)

    def update(self, other: "GruiModel"):
        updated = self.__class__(**self.__dict__)
        for key in other.__initial_attr:
            updated.__setattr__(key, other.__getattribute__(key))
        return updated


class GruiSubModel(GruiJsonSerializable, metaclass=_GruiModelMeta):

    ###############
    # Constructor #
    ###############
    def __init__(self, **kwargs):
        self.__json_result = None
        for attr_name, attr_value in kwargs.items():
            self.__setattr__(attr_name, attr_value)

    ##########
    # Setter #
    ##########
    def __setattr__(self, key, value):
        self.__dict__["_GruiSubModel__json_result"] = None
        super().__setattr__(key, value)

    ##########
    # Method #
    ##########
    def to_json(self):
        if self.__json_result is None:
            json_result = {}
            for attr_name, attr in self.__class__.grui_attributes.items():
                json_result[camel_case(attr_name)] = attr.type.jsonify_value(self.__getattribute__(attr_name))
            self.__json_result = json_result
        return self.__json_result


class Text(str):
    pass


class GruiType(GruiModel):
    """
    It the different data types the application can handle.
    This class shouldn't be instanced directly. Instead use the 'get_instance' with the int of data you want handle.
    """

    ###################
    # Class variables #
    ###################
    __instance = {}

    ##############
    # Attributes #
    ##############
    id: int
    name: str
    primitive: bool
    model: bool
    container: bool
    multiple: bool
    nullable: bool

    #########################
    # Constructor / Builder #
    #########################
    def __new__(cls, type_):
        if cls == GruiType:
            raise RuntimeError("Trying to initiate wrong instance")
        if GruiType.__instance.get(type_) is None:
            GruiType.__instance[type_] = object.__new__(cls)
        elif GruiType.__instance[type_].__class__ != cls:
            raise RuntimeError("Trying to override grui type")
        return GruiType.__instance[type_]

    def __init__(self, original_type):
        super().__init__(id=id(self))
        self._original_type = original_type
        self.primitive = self.model = self.container = self.multiple = self.nullable = False

    ###########
    # Getters #
    ###########
    @staticmethod
    def get_instance(type_):
        """
        Return the right GruiType for the type pass in parameter.
        This function allow us to also have only one instance by type.
        Indeed it is not require to have different instance for the same type.
        """
        if GruiType.__instance.get(type_) is None:
            if type_ == type(None):
                GruiType.__instance[type_] = GruiTypeNull(type_)
            elif type_ == bool:
                GruiType.__instance[type_] = GruiTypeBool(type_)
            elif type_ == int:
                GruiType.__instance[type_] = GruiTypeInt(type_)
            elif type_ == float:
                GruiType.__instance[type_] = GruiTypeFloat(type_)
            elif inspect.isclass(type_) and issubclass(type_, Text):
                GruiType.__instance[type_] = GruiTypeText(type_)
            elif type_ == str:
                GruiType.__instance[type_] = GruiTypeStr(type_)
            elif get_origin(type_) == list:
                GruiType.__instance[type_] = GruiTypeArray(type_)
            elif get_origin(type_) == dict:
                GruiType.__instance[type_] = GruiTypeMap(type_)
            elif get_origin(type_) == tuple:
                GruiType.__instance[type_] = GruiTypeFixedArray(type_)
            elif get_origin(type_) == Union:
                if len(type_.__args__) == 2 and type_.__args__[1] == type(None):
                    tmp = GruiType.get_instance(type_.__args__[0])
                    GruiType.__instance[type_] = tmp.__class__(type_)
                    GruiType.__instance[type_].nullable = True
                else:
                    GruiType.__instance[type_] = GruiTypeMultiple(type_)
            elif inspect.isclass(type_) and issubclass(type_, GruiModel):
                GruiType.__instance[type_] = GruiTypeModel(type_)
            elif inspect.isclass(type_) and issubclass(type_, GruiSubModel):
                GruiType.__instance[type_] = GruiTypeSubModel(type_)
            else:
                GruiType.__instance[type_] = GruiTypeUnknown(type_)

        return GruiType.__instance[type_]

    ###########
    # Methods #
    ###########
    def validate(self):
        return True

    @abstractmethod
    def validate_value(self, value):
        pass

    def jsonify_value(self, value):
        return value

    def register(self, register: Dict[int, "GruiType"]):
        if register.get(self.id) is not None and register[self.id] != self:
            raise DuplicateTypeError
        register[self.id] = self

    def __eq__(self, other):
        if self.name == "__unknown__":
            return self.name == other.name
        else:
            return super(GruiType, self).__eq__(other)


class GruiTypeUnknown(GruiType):

    def __init__(self, unknown_type):
        super().__init__(unknown_type)
        self.name = "__unknown__"

    def validate_value(self, value) -> Tuple[bool, Any]:
        return True, value


class GruiTypeNull(GruiType):

    def __init__(self, original_type):
        super().__init__(original_type)
        self.name = "__null__"
        self.nullable = self.primitive = True

    def validate_value(self, value) -> Tuple[bool, None]:
        if value is None:
            return True, None
        return False, value


class GruiTypeInt(GruiType):

    __REGEX_NUMBER_10 = re.compile("^\\d+$")
    __REGEX_NUMBER_16 = re.compile("^0x[0-9a-f]+$")
    __REGEX_NUMBER_8 = re.compile("^0o[0-7]+$")
    __REGEX_NUMBER_2 = re.compile("^0b[0-1]+$")

    def __init__(self, original_type):
        super().__init__(original_type)
        self.primitive = True
        self._original_type = original_type
        self.name = "__int__"

    def validate_value(self, value) -> Tuple[bool, Optional[int]]:
        if self.nullable and value is None:
            return True, value
        if type(value) is int:
            return True, value
        elif type(value) is str:
            if GruiTypeInt.__REGEX_NUMBER_10.match(value):
                return True, int(value)
            elif GruiTypeInt.__REGEX_NUMBER_16.match(value.lower()):
                return True, int(value, 16)
            elif GruiTypeInt.__REGEX_NUMBER_8.match(value):
                return True, int(value, 8)
            elif GruiTypeInt.__REGEX_NUMBER_2.match(value):
                return True, int(value, 2)
        return False, value


class GruiTypeFloat(GruiType):

    __REGEX_FLOAT = re.compile("^\\d*\\.\\d+$")

    def __init__(self, original_type):
        super().__init__(original_type)
        self.primitive = True
        self.name = "__float__"

    def validate_value(self, value) -> Tuple[bool, Optional[float]]:
        if self.nullable and value is None:
            return True, value
        if type(value) is float:
            return True, value
        elif type(value) is int:
            return True, float(value)
        elif type(value) is str and GruiTypeFloat.__REGEX_FLOAT.match(value):
            return True, float(value)
        return False, value


class GruiTypeBool(GruiType):

    def __init__(self, original_type):
        super().__init__(original_type)
        self.primitive = True
        self.name = "__bool__"

    def validate_value(self, value) -> Tuple[bool, Optional[bool]]:
        if self.nullable and value is None:
            return True, None
        elif type(value) is bool:
            return True, value
        return False, value


class GruiTypeStr(GruiType):

    def __init__(self, original_type):
        super().__init__(original_type)
        self.primitive = True
        self.name = "__str__"

    def validate_value(self, value) -> Tuple[bool, Optional[str]]:
        if self.nullable and value is None:
            return True, None
        if type(value) is str:
            return value != "", value
        return False, value


class GruiTypeText(GruiTypeStr):

    def __init__(self, original_type):
        super().__init__(original_type)
        self.name = "__text__"


class GruiTypeModelAttribute(GruiSubModel):

    read_only: bool
    type: GruiType
    default_value: Any
    description: str


class GruiTypeModel(GruiType):

    children: Dict[str, GruiTypeModelAttribute]

    def __init__(self, original_type):
        super().__init__(original_type)
        if isinstance(original_type, typing._GenericAlias) and original_type.__origin__ is Union:
            self.name = snake_case(original_type.__args__[0].__name__)
        else:
            self.name = snake_case(original_type.__name__)
        self.model = True
        self.__children = None

    @property
    def children(self) -> Dict[str, GruiTypeModelAttribute]:
        tt = self._original_type
        return self._original_type.__args__[0].grui_attributes if self.nullable else self._original_type.grui_attributes

    def jsonify_value(self, value):
        return None if value is None else value.id

    def register(self, register: Dict[int, GruiType]):
        super().register(register)
        for attr in self.children.values():
            attr.type.register(register)

    def validate_value(self, value) -> Tuple[bool, Optional[GruiModel]]:
        if self.nullable and value is None:
            return True, None
        if type(value) is self._original_type:
            return True, value
        return False, value


class GruiTypeSubModel(GruiType):

    children: Dict[str, GruiTypeModelAttribute]

    def __init__(self, original_type):
        super().__init__(original_type)
        if isinstance(original_type, typing._GenericAlias) and original_type.__origin__ is Union:
            self.name = snake_case(original_type.__args__[0].__name__)
        else:
            self.name = snake_case(original_type.__name__)
        self.model = True

    @property
    def children(self) -> Dict[str, GruiTypeModelAttribute]:
        return self._original_type.grui_attributes

    def jsonify_value(self, value):
        return None if value is None else value.to_json()

    def validate_value(self, value) -> Tuple[bool, Optional[GruiModel]]:
        if self.nullable and value is None:
            return True, None
        if type(value) is self._original_type:
            return True, value
        return False, value


class GruiTypeArray(GruiType):

    child: GruiType

    def __init__(self, original_type):
        super().__init__(original_type)
        self.child = GruiType.get_instance(original_type.__args__[0])
        self.name = "__array__(" + self.child.name + ")"
        self.container = True
        self.primitive = self.child.primitive
        self.model = self.child.model
        self.jsonify = 44

    def jsonify_value(self, value):
        result = []
        for tmp in value:
            result.append(self.child.jsonify_value(tmp))
        return result

    def register(self, register: Dict[int, "GruiType"]):
        super().register(register)
        self.child.register(register)

    def validate_value(self, value) -> Tuple[bool, Optional[list]]:
        if self.nullable and value is None:
            return True, None
        if type(value) is list:
            for i, tmp in enumerate(value):
                child_valid, child_value = self.child.validate_value(tmp)
                if not child_valid:
                    return False, value
                value[i] = child_value
            return True, value
        return False, value


class GruiTypeMap(GruiType):

    key_type: GruiType
    value_type: GruiType

    def __init__(self, original_type):
        super().__init__(original_type)
        if isinstance(original_type, typing._GenericAlias) and original_type.__origin__ is Union and \
                len(original_type.__args__) == 2 and original_type.__args__[1] == type(None):
            self.nullable = True
            self.key_type = GruiType.get_instance(original_type.__args__[0].__args__[0])
            self.value_type = GruiType.get_instance(original_type.__args__[0].__args__[1])
        else:
            self.key_type = GruiType.get_instance(original_type.__args__[0])
            self.value_type = GruiType.get_instance(original_type.__args__[1])
        self.name = "__map__(" + self.key_type.name + ", " + self.value_type.name + ")"
        self.container = True

    def jsonify_value(self, value):
        if value is None:
            return None
        result = {}
        for key, map_value in value.items():
            result[self.key_type.jsonify_value(key)] = self.value_type.jsonify_value(map_value)
        return result

    def register(self, register: Dict[int, "GruiType"]):
        super().register(register)
        self.key_type.register(register)
        self.value_type.register(register)

    def validate_value(self, dict_) -> Tuple[bool, Optional[dict]]:
        if self.nullable and dict_ is None:
            return True, None
        if type(dict_) is dict:
            for key, value in dict_.items():
                key_valid, key = self.key_type.validate_value(key)
                value_valid, value = self.value_type.validate_value(value)
                if not key_valid or not value_valid:
                    return False, value
                value[key] = value
            return True, dict_
        return False, dict_


class GruiTypeFixedArray(GruiType):

    children: Tuple[GruiType, ...]

    def __init__(self, original_type):
        super().__init__(original_type)
        children = []
        name = "__fixed_array__("
        for arg in original_type.__args__:
            tmp = GruiType.get_instance(arg)
            children.append(tmp)
            name += tmp.name + ", "
        self.children = tuple(children)
        self.name = name[:-2] + ")"

    def jsonify_value(self, value):
        result = []
        for i, tmp in enumerate(value):
            result.append(self.children[i].jsonify_value(tmp))
        return result

    def register(self, register: Dict[int, "GruiType"]):
        super().register(register)
        for child in self.children:
            child.register(register)

    def validate_value(self, value) -> Tuple[bool, Optional[tuple]]:
        if self.nullable and value is None:
            return True, None
        if type(value) is tuple and len(value) == len(self.children):
            for i, tmp in enumerate(value):
                child_valid, child_value = self.children[i].validate(tmp)
                if not child_valid:
                    return False, value
                value[i] = child_value
            return True, value
        return False, value


class GruiTypeMultiple(GruiType):

    choices: Tuple[GruiType, ...]

    def __init__(self, multiple_type):
        super().__init__(multiple_type)
        self.primitive = True
        self.multiple = True
        choices = []
        name = "__multiple__("
        for arg in multiple_type.__args__:
            if arg == type(None):
                self.nullable = True
            else:
                child = GruiType.get_instance(arg)
                if not child.primitive:
                    self.primitive = False
                if child.model:
                    self.model = True
                choices.append(child)
                name += child.name + ", "
        self.name = name[:-2] + ")"
        self.choices = tuple(choices)

    def jsonify_value(self, value):
        for choice in self.choices:
            if isinstance(value, choice._original_type):
                return choice.jsonify_value(value)
        return value

    def register(self, register: Dict[int, "GruiType"]):
        super().register(register)
        for choice in self.choices:
            choice.register(register)

    def validate_value(self, value) -> Tuple[bool, Optional[Any]]:
        if self.nullable and value is None:
            return True, None
        for choice in self.choices:
            valid, tmp = choice.validate_value(value)
            if valid:
                return True, tmp
        return False, value
