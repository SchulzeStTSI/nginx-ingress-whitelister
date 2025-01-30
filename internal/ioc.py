import inspect
import json
import importlib.util
from typing import Callable, Type



class IoCContainer:
    def __init__(self, services_json_file: str):
        self._services = {}
        self._interface_definition = self.load_interface_from_json(services_json_file)
        self.type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "dict": dict,
            "list": list,
            "tuple": tuple,
            "None": None
        }

    def register(self, service_name: str, service_reference: Type):
        """Registers a service class and checks if it implements the correct methods from the JSON specification."""
        service_class = self._get_service_class(service_reference)

        # Check if the service is defined in the JSON specification
        if service_name not in self._interface_definition["services"]:
            raise ValueError(f"Service {service_name} is not defined in the JSON specification.")
        
        service_functions = self._interface_definition["services"][service_name]["functions"]

        for method_name, method_info in service_functions.items():
            if not hasattr(service_class, method_name):
                raise TypeError(f"Service {service_class.__name__} does not implement the method {method_name}")

            # Check the parameters of the method
            method = getattr(service_class, method_name)
            expected_params = method_info['parameters']
            actual_params = inspect.signature(method).parameters

            # Check if the number of parameters matches, including *args and **kwargs
            self._check_parameter_count_and_types(expected_params, actual_params, method_name, service_class)

            # Check the types of the parameters
            for idx, (param_name, param) in enumerate(actual_params.items()):
                expected_type = eval(expected_params[idx]['type'])  # Type from JSON
                actual_type = param.annotation if param.annotation != inspect.Parameter.empty else None
                if actual_type != expected_type:
                    raise TypeError(f"Parameter '{param_name}' in method {method_name} of {service_class.__name__} should be of type {expected_type.__name__}, but got {actual_type.__name__}")

            expected_return_type = method_info.get("return_type")
            if expected_return_type:
                expected_return_type = self._get_type_from_string(expected_return_type)  # Convert from string to actual type
                actual_return_type = method.__annotations__.get("return", None)

                # Compare the expected and actual return types
                if actual_return_type != expected_return_type:
                    raise TypeError(f"Return type of method {method_name} in service {service_class.__name__} should be {expected_return_type.__name__}, but got {actual_return_type.__name__}")

        # Store the service class in the container
        if service_name not in self._services:
            self._services[service_name] = []
        self._services[service_name].append(service_class)

    def _get_type_from_string(self, type_name: str):
        """Converts a string type name to the corresponding Python type."""
        return self.type_mapping.get(type_name)
    
    def _check_parameter_count_and_types(self, expected_params, actual_params, method_name, service_class):
        """Checks the number and types of the parameters."""
        expected_param_names = [param["name"] for param in expected_params]
        actual_param_names = list(actual_params.keys())

        # Check if the number of parameters matches, including *args and **kwargs
        if len(expected_param_names) != len(actual_param_names):
            raise TypeError(f"Method {method_name} in service {service_class.__name__} has an incorrect number of parameters")

        # Check the types of the parameters
        for idx, param_name in enumerate(expected_param_names):
            expected_param = expected_params[idx]
            actual_param = actual_params.get(param_name)

            # If the parameter is optional (with default values), skip the check
            if actual_param is None:
                continue

            # Check if the actual parameter has the correct type
            expected_type = eval(expected_param["type"])
            actual_type = actual_param.annotation if actual_param.annotation != inspect.Parameter.empty else None
            if actual_type != expected_type:
                raise TypeError(f"Parameter '{param_name}' in method {method_name} of {service_class.__name__} should be of type {expected_type.__name__}, but got {actual_type.__name__}")

    def get(self, name: str) -> Callable:
        """Returns the first registered service for a given name."""
        service_classes = self._services.get(name)
        if not service_classes:
            raise ValueError(f"Service {name} not found.")
        return service_classes[0]()

    def get_all(self, name: str) -> list:
        """Returns all service implementations for a given name."""
        service_classes = self._services.get(name)
        if not service_classes:
            raise ValueError(f"Service {name} not found.")
        return [service_class() for service_class in service_classes]

    def list_services(self):
        """Returns all registered services with their respective instances."""
        services = {}
        for service_name, service_classes in self._services.items():
            services[service_name] = [service_class() for service_class in service_classes]
        return services
            

    def _get_service_class(self, service_reference: Type) -> Type:
        """Loads a service class from a file path or class name."""
        if service_reference.endswith(".py"):
            return self._load_class_from_file(service_reference)
        else:
            return self._load_class_from_name(service_reference)

    def _load_class_from_file(self, file_path: str) -> Type:
        """Loads a class from a Python file."""
        module_name = file_path.replace(".py", "").replace("/", ".")
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        class_name = module_name.split(".")[-1]  # Assuming the class name is the same as the file name
        return getattr(module, class_name)

    def _load_class_from_name(self, class_name: str) -> Type:
        """Loads a class by its name from the current code base."""
        parts = class_name.split(".")
        module_name = ".".join(parts[:-1])
        class_name = parts[-1]

        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def load_interface_from_json(self, json_file: str) -> dict:
        """Loads the service specification from the JSON file."""
        with open(json_file, 'r') as f:
            return json.load(f)
