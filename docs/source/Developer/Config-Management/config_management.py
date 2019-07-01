# -*- coding: utf-8 -*-

"""
Config Management is a Tool to help you manage config values in single place,
and allow external tools, such as Shell Scripts, Cloudformation, AWS SAM,
Serverless Framework, Terraform to read config value from the centralized place.
"""

from __future__ import print_function
import os
import re
import sys
import copy
import json
import inspect
from collections import OrderedDict

if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
    from typing import Dict


def strip_comment_line_with_symbol(line, start):
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(re.findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part))
              for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):
    """
    Strip comments from json string.

    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)
    return '\n'.join(lines)


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


class Field(object):
    _creation_index = 0

    def __init__(self, value=None, default=None):
        if value is None:
            self.value = default
        self.value = value
        self._creation_index = Field._creation_index
        Field._creation_index += 1


class Constant(Field):
    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Derivable(Field):
    def __init__(self, value=None, default=None):
        super(Derivable, self).__init__(value, default)
        self.__getter_method = None

    def getter(self, method):
        self.__getter_method = method

    def get_value(self, instance):
        return self.__getter_method(instance)


def is_instance_or_subclass(val, class_):
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def _get_fields(attrs, field_class, pop=False, ordered=False):
    """Get fields from a class. If ordered=True, fields will sorted by creation index.
    :param attrs: Mapping of class attributes
    :param type field_class: Base field class
    :param bool pop: Remove matching fields
    """
    fields = [
        (field_name, field_value)
        for field_name, field_value in attrs.items()
        if is_instance_or_subclass(field_value, field_class)
    ]
    if pop:
        for field_name, _ in fields:
            del attrs[field_name]
    if ordered:
        fields.sort(key=lambda pair: pair[1]._creation_index)
    return fields


def _get_fields_by_mro(klass, field_class, ordered=False):
    """Collect fields from a class, following its method resolution order. The
    class itself is excluded from the search; only its parents are checked. Get
    fields from ``_declared_fields`` if available, else use ``__dict__``.
    :param type klass: Class whose fields to retrieve
    :param type field_class: Base field class
    """
    mro = inspect.getmro(klass)
    # Loop over mro in reverse to maintain correct order of fields
    return sum(
        (
            _get_fields(
                getattr(base, "_declared_fields", base.__dict__),
                field_class,
                ordered=ordered,
            )
            for base in mro[:0:-1]
        ),
        [],
    )


class ConfigMeta(type):
    def __new__(cls, name, bases, attrs):
        cls_fields = _get_fields(attrs, Field, pop=False, ordered=True)
        klass = super(ConfigMeta, cls).__new__(cls, name, bases, attrs)
        inherited_fields = _get_fields_by_mro(klass, Field, ordered=True)

        # Assign _declared_fields on class
        klass._declared_fields = OrderedDict(inherited_fields + cls_fields)
        klass._constant_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Constant)
        ])
        klass._deriable_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Derivable)
        ])
        return klass


class BaseConfigClass(object):
    _declared_fields = dict()  # type: Dict[str: Constant]
    _constant_fields = dict()  # type: Dict[str: Constant]
    _deriable_fields = dict()  # type: Dict[str: Derivable]

    def __init__(self):
        self._declared_fields = copy.deepcopy(self._declared_fields)
        self._constant_fields = OrderedDict([
            (name, field)
            for name, field in self._declared_fields.items()
            if isinstance(field, Constant)
        ])
        self._deriable_fields = OrderedDict([
            (name, field)
            for name, field in self._declared_fields.items()
            if isinstance(field, Derivable)
        ])

        for name, field in self._constant_fields.items():
            setattr(self, name, field)

    @classmethod
    def from_dict(cls, dct):
        """
        :type dct: dict
        :rtype: BaseConfig
        """
        config = cls()
        for key, value in dct.items():
            if key in config._constant_fields:
                config._constant_fields[key].set_value(value)
        return config

    @classmethod
    def from_json(cls, json_str):
        """
        :type json_str: str
        :rtype: BaseConfig
        """
        return cls.from_dict(json.loads(strip_comments(json_str)))

    def to_dict(self, constant_only=False):
        """
        Dump the current config values to dictionary, include both
        constant values and derived values.

        :type constant_only: bool
        :param constant_only: only dump constant values.

        :rtype: dict
        """
        dct = dict()
        for attr, value in self._constant_fields.items():
            dct[attr] = value.get_value()
        if constant_only is False:
            for attr, value in self._deriable_fields.items():
                dct[attr] = value.get_value(self)
        return dct

    def to_json(self, constant_only=False):
        """
        Dump the current config values to json string, include both
        constant values and derived values.

        :type constant_only: bool
        :param constant_only: only dump constant values.

        :rtype: str
        """
        return json.dumps(self.to_dict(constant_only=constant_only),
                          indent=4, sort_keys=True, ensure_ascii=False)

    def pprint(self):
        """
        Pretty print current config values.
        """

        print(self.to_json())

    @classmethod
    def create_config_raw_json_template(cls):
        """
        Create an empty config json file to work with.
        """
        import random
        abspath = os.path.join(
            os.path.dirname(__file__),
            "config-raw-{}.json".format(random.randint(100000, 999999))
        )
        with open(abspath, "wb") as f:
            f.write(cls().to_json(constant_only=True).encode("utf-8"))

    CONFIG_DIR = None  # type: str # Where the config-xxx.json file stays

    @property
    def CONFIG_RAW_JSON_FILE(self):
        return os.path.join(self.CONFIG_DIR, "config-raw.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_PYTHON(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-python.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-shell-script.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-cloudformation.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SAM(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-sam.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-serverless.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM(self):
        return os.path.join(self.CONFIG_DIR, "config-final-for-terraform.json")

    # shortcut method for ``with open(...) as f`` syntax
    @classmethod
    def read_from_json(cls, abspath):
        with open(abspath, "rb") as f:
            return f.read().decode("utf-8")

    @classmethod
    def write_to_json(cls, abspath, json_str):
        with open(abspath, "wb") as f:
            f.write(json_str.encode("utf-8"))

    def dump_final_config_json_for_python(self):
        pass

    def dump_final_config_json_for_shell_script(self):
        pass

    def dump_final_config_json_for_cloudformation(self):
        pass

    def dump_final_config_json_for_sam(self):
        pass

    def dump_final_config_json_for_serverless(self):
        pass

    def dump_final_config_json_for_terraform(self):
        pass

    def dump_final_config_json(self):
        self.dump_final_config_json_for_python()
        self.dump_final_config_json_for_shell_script()
        self.dump_final_config_json_for_cloudformation()
        self.dump_final_config_json_for_sam()
        self.dump_final_config_json_for_serverless()
        self.dump_final_config_json_for_terraform()

    @classmethod
    def visit_json_path(cls, data, json_path):
        value = data
        for p in json_path.split("."):
            value = value[p]
        return value

    @classmethod
    def print_python_json_field(cls, json_path):
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_PYTHON))
        print(cls.visit_json_path(data, json_path))

    @classmethod
    def print_shell_script_json_field(cls, json_path):
        """
        Utility method to make a simple python script to allow shell scripts to
        read data from json, without using jq https://stedolan.github.io/jq/.

        Usage:

        Content of Python script:
        
        .. code-block:: python
    
            # content of read_config_final_for_shell_script.py
            
            if __name__ == "__main__":
                import sys
                from xxx import Config
            
                json_path = sys.argv[1]
                Config.print_shell_script_json_field(json_path)

        In your shell script, you can do:

        .. code-block:: bash
        
            $ ENVIRONMENT_NAME="$(python read_config_final_for_shell_script.py ENVIRONMENT_NAME)"
        """
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT))
        print(cls.visit_json_path(data, json_path))

    @classmethod
    def print_cloudformation_json_field(cls, json_path):
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION))
        print(cls.visit_json_path(data, json_path))

    @classmethod
    def print_sam_json_field(cls, json_path):
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_SAM))
        print(cls.visit_json_path(data, json_path))

    @classmethod
    def print_serverless_json_field(cls, json_path):
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS))
        print(cls.visit_json_path(data, json_path))

    @classmethod
    def print_terraform_json_field(cls, json_path):
        data = json.loads(cls.read_from_json(cls().CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM))
        print(cls.visit_json_path(data, json_path))


@add_metaclass(ConfigMeta)
class ConfigClass(BaseConfigClass):
    pass


# --- Test
if __name__ == "__main__":
    class Config_1(ConfigClass):
        SERVICE_NAME = Constant()

        SERVICE_NAME_SLUG = Derivable()

        @SERVICE_NAME_SLUG.getter
        def get_service_name_slug(self):
            return self.SERVICE_NAME.get_value().replace("_", "-")


    class Config_2(Config_1):
        STAGE = Constant()

        ENVIRONMENT_NAME = Derivable()

        @ENVIRONMENT_NAME.getter
        def get_environment_name(self):
            return "{}-{}".format(self.SERVICE_NAME_SLUG.get_value(self), self.STAGE.get_value())

        NAMING_PREFIX = Derivable()

        @NAMING_PREFIX.getter
        def get_naming_prefix(self):
            return self.ENVIRONMENT_NAME.get_value(self)


    class Config(Config_2):
        CONFIG_DIR = os.path.dirname(__file__)

        def dump_final_config_json_for_shell_script(self):
            self.write_to_json(self.CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT, self.to_json())


    config1 = Config()
    assert config1.SERVICE_NAME.get_value() == None
    assert config1.STAGE.get_value() == None

    config1.SERVICE_NAME.set_value("my_service")
    config1.STAGE.set_value("dev")
    assert config1.SERVICE_NAME.get_value() == "my_service"
    assert config1.STAGE.get_value() == "dev"

    assert config1.SERVICE_NAME_SLUG.get_value(config1) == "my-service"
    assert config1.ENVIRONMENT_NAME.get_value(config1) == "my-service-dev"
    assert config1.NAMING_PREFIX.get_value(config1) == "my-service-dev"

    config_data = config1.to_dict()
    assert config_data == {
        'SERVICE_NAME': 'my_service',
        'STAGE': 'dev',
        'SERVICE_NAME_SLUG': 'my-service',
        'ENVIRONMENT_NAME': 'my-service-dev',
        'NAMING_PREFIX': 'my-service-dev',
    }

    # test for whether new Config instance get new field instance
    config2 = Config()
    assert config2.SERVICE_NAME.get_value() == None
    assert config2.STAGE.get_value() == None
    config2.SERVICE_NAME.set_value("your_service")
    config2.STAGE.set_value("prod")
    assert config2.SERVICE_NAME.get_value() == "your_service"
    assert config2.STAGE.get_value() == "prod"

    assert config2.SERVICE_NAME_SLUG.get_value(config2) == "your-service"
    assert config2.ENVIRONMENT_NAME.get_value(config2) == "your-service-prod"
    assert config2.NAMING_PREFIX.get_value(config2) == "your-service-prod"

    config_data = config2.to_dict()
    assert config_data == {
        'SERVICE_NAME': 'your_service',
        'STAGE': 'prod',
        'SERVICE_NAME_SLUG': 'your-service',
        'ENVIRONMENT_NAME': 'your-service-prod',
        'NAMING_PREFIX': 'your-service-prod',
    }

    config1.dump_final_config_json()

    Config.print_shell_script_json_field("ENVIRONMENT_NAME")
