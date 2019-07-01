# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import sys
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

    def to_dict(self):
        dct = dict()
        for attr, value in self._constant_fields.items():
            dct[attr] = value.get_value()
        for attr, value in self._deriable_fields.items():
            dct[attr] = value.get_value(self)
        return dct

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def pprint(self):
        print(self.to_json())

    CONFIG_DIR = None

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


    class Config(Config_2): pass


    config = Config()
    config.SERVICE_NAME.set_value("my_service")
    config.STAGE.set_value("dev")
    assert config.SERVICE_NAME_SLUG.get_value(config) == "my-service"
    assert config.ENVIRONMENT_NAME.get_value(config) == "my-service-dev"
    assert config.NAMING_PREFIX.get_value(config) == "my-service-dev"

    config_data = config.to_dict()
    assert config_data == {
        'SERVICE_NAME': 'my_service',
        'STAGE': 'dev',
        'SERVICE_NAME_SLUG': 'my-service',
        'ENVIRONMENT_NAME': 'my-service-dev',
        'NAMING_PREFIX': 'my-service-dev',
    }

    config1 = Config.from_dict(config_data)
    assert config_data == config1.to_dict()
