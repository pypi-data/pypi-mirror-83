MODE_PRIVATE = "private"
MODE_PROTECTED = "protected"
MODE_PUBLIC = "public"

GENERIC_TYPE_PLACEHOLDER = "GENERIC"

TYPE_CLASS = "CLASS"
TYPE_ENUM = "ENUM"
TYPE_INTERFACE = "INTERFACE"

TYPE_INTEGER = "INTEGER"
TYPE_FLOAT = "FLOAT"
TYPE_BOOLEAN = "BOOLEAN"
TYPE_STRING = "STRING"
TYPE_EVALUATED = "EVALUATED"
TYPE_ANNOTATION = "ANNOTATION"
TYPE_LIST = "LIST"
TYPE_LIST_INTEGER = "LIST_INTEGER"
TYPE_LIST_FLOAT = "LIST_FLOAT"
TYPE_LIST_BOOLEAN = "LIST_BOOLEAN"
TYPE_LIST_STRING = "LIST_STRING"
TYPE_LIST_CLASS = "LIST_CLASS"
TYPE_LIST_EVALUATED = "LIST_EVALUATED"
TYPE_LIST_ANNOTATION = "LIST_ANNOTATION"
TYPE_VOID = "void"

ANNOTATION_LEVEL_ATTRIBUTE = "ATTRIBUTE_ANNOTATION"
ANNOTATION_LEVEL_GETTER = "GETTER_ANNOTATION"
ANNOTATION_LEVEL_METHOD = "METHOD_ANNOTATION"

CONSTRUCTOR_ALL = "ALL"
CONSTRUCTOR_EMPTY = "EMPTY"
CONSTRUCTOR_SELECTED = "SELECTED"

class Generator:
    def generate(self, indentation=0):
        pass


def to_camel_case(s):
    return s[0].upper() + s[1:] if s else s


def padding(indentation):
    return f'{"":>{indentation}}'


def package_name_from_package(clazz):
    splits = clazz.split(".")
    return ".".join(splits[:-1])


def class_name_from_package(clazz):
    splits = clazz.split(".")
    return splits[-1]
