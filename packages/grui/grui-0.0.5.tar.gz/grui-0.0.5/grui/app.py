import inspect
import json
import os
from functools import wraps
from typing import *

import docstring_parser
from case_convert import upper_case
from flask import Flask, request, Response, send_file
from flask_cors import CORS

from .decorator import GruiFunction
from .service import AbstractGruiService
from .typing import GruiType, GruiModel, IncorrectDataWhileEncodingError
from .utils import dict2list, GruiJsonEncoder


##########
# Errors #
##########
class ArgumentMatchError(RuntimeError):
    pass


class DuplicateServiceError(RuntimeError):
    pass


def _convert_argument_list(type_: type, value: Any) -> List[Any]:
    result = []
    if isinstance(value, (list, tuple)):
        for tmp in value:
            result.append(_convert_argument(type_, tmp, False))
    elif isinstance(value, str):
        for tmp in value.split(","):
            result.append(_convert_argument(type_, tmp, False))
    else:
        result.append(_convert_argument(type_, value, False))
    return result


def _convert_argument(type_: type, value: Any, to_list: bool) -> Any:
    if to_list:
        return _convert_argument_list(type_, value)
    else:
        if type_ is int:
            return int(value)
        elif type_ is float:
            return float(value)
        elif type_ is bool:
            return bool(value)
        elif isinstance(type_, List.__class__):
            return _convert_argument_list(type_.__args__[0], value)
        elif issubclass(type_, GruiModel):
            return type_.from_json(value)
    return value


def _match_argument(func: GruiFunction, input_: dict, additional_data: Any = None) -> Any:
    result = {}
    parameters = func.__annotations__
    param_found = []

    for param_name, param_class in parameters.items():
        if param_name in input_:
            result[param_name] = _convert_argument(param_class, input_[param_name], func.props.multiple_action)
            param_found.append(param_name)

    unfounded = None
    for param_name in parameters:
        if param_name not in param_found:
            unfounded = param_name
            break

    if additional_data is not None and unfounded is not None and len(parameters) == len(param_found) + 1:
        result[unfounded] = _convert_argument(parameters[unfounded], additional_data, func.multiple_action)
        param_found.append(unfounded)

    if len(inspect.signature(func).parameters) - 1 != len(param_found):
        raise ArgumentMatchError

    if func.multiple_action:
        return dict2list(result)

    return result


###########
# Classes #
###########
class GruiApp:

    def __init__(self, service_package=None, debug: bool = False, title: str = None):
        from .service import GruiDocService
        self._debug = debug
        self.title = title if title is not None else os.path.split(os.getcwd())[-1]
        self._registered_service = {}
        self.registered_function = {}
        self.registered_type = {}
        self.service_doc = {}
        self._flask_app = None
        self.register_service(GruiDocService)
        if service_package is not None:
            self.register_package(service_package)

    def register_package(self, package):
        for _, service_class in \
                inspect.getmembers(package, lambda c: inspect.isclass(c) and issubclass(c, AbstractGruiService)):
            self.register_service(service_class)

    def register_service(self, service_class):
        if self._registered_service.get(service_class) is not None:
            raise DuplicateServiceError

        service_init_arguments = []
        for annotation in service_class.__init__.__annotations__.values():
            if isinstance(self, annotation):
                service_init_arguments.append(self)
            elif annotation in self._registered_service.keys():
                service_init_arguments.append(self._registered_service[annotation])
        service_instance = service_class(*service_init_arguments)
        self._registered_service[service_class] = service_instance
        self.service_doc[service_class.url_prefix] = _GruiServiceDoc(service_class)
        for _, method in inspect.getmembers(service_instance, lambda m: isinstance(m, GruiFunction)):
            self.register_function(method)

    def register_function(self, function: GruiFunction):
        if self._flask_app is not None:
            raise RuntimeError("The app have been started no function can be added anymore")
        self.registered_function[function.id] = function
        if function.result is not None:
            self.register_type(function.result.type)
        for argument in function.args.values():
            self.register_type(argument.type)
        for service_class in self._registered_service.keys():
            tmp = service_class.url_prefix
            if function.path.startswith("/api/" + tmp):
                self.service_doc[tmp].methods.append(function)

    def register_type(self, type_: GruiType):
        type_.register(self.registered_type)

    def run(self):
        self._build_flask_app()
        self._flask_app.run(debug=self._debug)

    def _build_flask_app(self):
        if self._flask_app is not None:
            return
        self._flask_app = Flask(__name__)
        CORS(self._flask_app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "GRUI"]}})
        self._flask_app.url_map.strict_slashes = False
        self._flask_app.route('/shutdown', methods=['GET'])(GruiApp.shutdown)
        #self._flask_app.route("/", methods=["GET", "POST", "PUT", "DELETE", "GRUI"])(
        #    lambda: "Hello, cross-origin-world!")

        for function in self.registered_function.values():
            self.log("register", "%-6s" % function.method, function.path)
            self._flask_app.route(function.path, methods=[function.method])(self._build4flask(function))

        self._flask_app.route('/<path>', methods=['GET'])(GruiApp.send_js)

    def _find_argument(self, func: GruiFunction, path_parameters: Dict[str, str], body_parameters: Any) -> Dict[str, Any]:
        parameters_found = {}
        signature = inspect.signature(func.callable)

        annotations = dict(signature.parameters.items())
        if func.is_method:
            del annotations["self"]

        if len(annotations) == 0:
            yield {}

        nb_parameter = None

        for param_name in annotations:
            if param_name in path_parameters:
                tmp = _convert_argument(annotations[param_name].annotation, path_parameters[param_name], func.multiple_action)
                if nb_parameter is not None and len(tmp) != nb_parameter:
                    raise ValueError
                else:
                    nb_parameter = len(tmp)
                parameters_found[param_name] = tmp

        if len(parameters_found.keys()) != len(annotations) and body_parameters is not None:
            missing_parameters = [x for x in annotations.keys() if x not in parameters_found.keys()]
            if len(missing_parameters) == 1:
                # Auto convert the body parameter to the missing param
                tmp = _convert_argument(annotations[missing_parameters[0]].annotation, body_parameters, func.multiple_action)
                if nb_parameter is not None and len(tmp) != nb_parameter:
                    raise ValueError
                else:
                    nb_parameter = len(tmp)
                parameters_found[missing_parameters[0]] = tmp

        result = {}
        if func.multiple_action:
            for index in range(nb_parameter):
                for key in parameters_found:
                    result[key] = parameters_found[key][index]
                yield result
        else:
            yield parameters_found

    def _build4flask(self, func: GruiFunction):
        @wraps(func)
        def _(*args, **kwargs):
            try:
                code = func.default_return_code
                result = []
                for method_arguments in self._find_argument(func, kwargs, request.json):
                    for previous_action in func.previous_actions:
                        previous_action(code)
                    res = func(*args, **method_arguments)
                    for next_action in func.next_actions:
                        (res, code) = next_action(res, code)
                    if res is None:
                        return Response(json.dumps(res, cls=GruiJsonEncoder), status=code, content_type="application/json")
                    if func.multiple_action:
                        result.append(res)
                    else:
                        return Response(json.dumps(res, cls=GruiJsonEncoder), status=code, content_type="application/json")
                return Response(json.dumps(result, cls=GruiJsonEncoder), status=code, content_type="application/json")
            except IncorrectDataWhileEncodingError as e:
                return Response(json.dumps(str(e), cls=GruiJsonEncoder), status=400, content_type="application/json")
        return _

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    @staticmethod
    def shutdown():
        GruiApp.shutdown_server()
        return 'Server shutting down...'

    def log(self, *args):
        # if self._debug:
        print(*args)
    # set the project root directory as the static folder, you can set others.
    app = Flask(__name__, static_url_path='')

    @staticmethod
    def send_js(path):
        tt = os.path.join(os.getcwd(), 'build', path)

        print("path", os.path.join(os.getcwd(), 'build', path))
        return send_file(os.path.join(os.getcwd(), 'build', path))


class _GruiServiceDoc(GruiModel):

    id: str
    name: str
    methods: List[GruiFunction]
    presentation: str
    description: str

    def __init__(self, service_class):
        doc_parsed = docstring_parser.parse(service_class.__doc__)
        super().__init__(id=service_class.url_prefix,
                         name=upper_case(service_class.__name__),
                         methods=[],
                         presentation=doc_parsed.short_description or "",
                         description=doc_parsed.long_description or "")

    def validate(self) -> bool:
        return True
