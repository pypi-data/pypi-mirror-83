import importlib.abc
import importlib.util
import inspect
from contextlib import suppress
from importlib.util import module_from_spec, spec_from_loader

from django.db.models.fields.files import FieldFile

from .loaders import StringLoader


class PyScriptFieldFile(FieldFile):
    def __init__(self, instance, field, name):
        super().__init__(instance, field, name)
        self.initialize_internal()

    def initialize_internal(self):
        # This method has to be called by every other method, because it is non deterministic when
        # exactly the file will be uploaded and therefore when the module will be accessable  

        if hasattr(self, "_module") and hasattr(self, "_callable") and hasattr(self, "_parameters"):
            return

        with suppress(FileNotFoundError):
            self._module, self._callable = self.import_script()
            self._parameters = getattr(self.instance, self.field.parameter_field) if self.field.parameter_field else {}

    def import_script(self):
        # Imports the script and returns the module and the module's callable
        spec = spec_from_loader(self.name.split(".")[0], StringLoader(self.file.read()))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module, module._CALLABLE

    def run_script(self, **injected_parameters):
        # Runs the script and injects the parameters, in case there any from the parameter field
        # As well as the paramters passed in through the injected_keyworks arguments
        self.initialize_internal()

        injected_parameters.update(self.get_casted_parameters())
        return self._callable(**injected_parameters)

    def get_casted_parameters(self):
        # Casts the parameters into the datatypes provided in the script file.
        # If a datatype is not provided, then it is provided as a string
        self.initialize_internal()

        signature = inspect.signature(self._callable)
        parameters = {}

        for k, v in self._parameters.items():
            parameter = signature.parameters[k]
            value = v
            if parameter.annotation:
                value = parameter.annotation(value)
            parameters[k] = value

        return parameters

    def extract_parameters(self):
        # Gets the parameters from the script's callable and passes them into the fields parameter field
        # Removes the parameters that are in the injected_paramters list, because they will be added to the script in runtime
        self.initialize_internal()

        signature = inspect.signature(self._callable)
        parameters = signature.parameters

        parameter_field = getattr(self.instance, self.field.parameter_field)
        keys = list(parameter_field.keys())

        if parameter_field is None:
            parameter_field = {}

        filtered_parameters = filter(lambda p: p[0] not in self.field.injected_parameters, parameters.items())
        for parameter_key, parameter in filtered_parameters:

            with suppress(ValueError):
                keys.remove(parameter_key)

            default = "" if parameter.default == inspect.Parameter.empty else parameter.default
            parameter_field.setdefault(parameter.name, str(default))

        for key in keys:
            del parameter_field[key]

        return parameter_field
