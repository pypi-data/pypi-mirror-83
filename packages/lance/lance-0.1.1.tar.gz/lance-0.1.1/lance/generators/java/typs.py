from lance.generators.java import *
from lance.generators.java.annotations import parse_annotations


def process_type(typ, fqcn=None, annotations=None, generic_types=None):
    import_list = []
    final_type = None

    if typ.upper() == TYPE_VOID.upper():
        final_type = "void"
    if typ == TYPE_STRING:
        import_list.append("java.lang.String")
        final_type = "String"
    elif typ == TYPE_INTEGER:
        final_type = "int"
    elif typ == TYPE_FLOAT:
        final_type = "float"
    elif typ == TYPE_BOOLEAN:
        final_type = "boolean"
    elif typ == TYPE_CLASS:
        if not fqcn:
            raise ValueError("For custom type, the fqcn of the class must be provided")
        if generic_types and len(generic_types) > 0:
            final_type, generic_imports = handle_generic_types(fqcn, generic_types)
            import_list.extend(generic_imports)

        # If the final type is not evaluated we do this, since even after having all the data provided, the final_type
        # may not be calculated
        if not final_type:
            final_type = class_name_from_package(fqcn)
            import_list.append(fqcn)
    elif typ == TYPE_LIST_STRING:
        final_type = "List<String>"
        import_list.append("java.util.List")
        import_list.append("java.lang.String")
    elif typ == TYPE_LIST_INTEGER:
        final_type = "List<Integer>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Integer")
    elif typ == TYPE_LIST_FLOAT:
        final_type = "List<Float>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Float")
    elif typ == TYPE_LIST_BOOLEAN:
        final_type = "List<Boolean>"
        import_list.append("java.util.List")
        import_list.append("java.lang.Boolean")
    elif typ == TYPE_LIST_CLASS:
        if not fqcn:
            raise ValueError("For custom type, the fqcn of the class must be provided")
        final_type = f"List<{class_name_from_package(fqcn)}>"
        import_list.append("java.util.List")
        import_list.append(fqcn)

    if annotations and len(annotations) > 0:
        for a in annotations:
            final_type = f'{a.generate()} {final_type}'
            import_list.extend(a.get_imports())

    return final_type, import_list


def handle_generic_types(fqcn, types):
    imports = []
    imports.append(fqcn)
    if types and len(types) > 0:
        generic_types = []
        if GENERIC_TYPE_PLACEHOLDER in types:
            return f'{class_name_from_package(fqcn)}<?>', imports
        else:
            for typ in types:
                imports.append(typ)
                generic_types.append(class_name_from_package(typ))
        return f'{class_name_from_package(fqcn)}<{",".join(generic_types)}>', imports

    return class_name_from_package(fqcn), imports


def obtain_type(name, doc):
    __get_type_checked(name, doc)

    # Type information
    type_of = doc.get("of")
    object_fqcn = doc.get("fqcn")
    annotations_info = doc.get("annotations")
    generic_types = doc.get("generic_types")

    annotations = None
    if annotations_info:
        annotations = parse_annotations(annotations_info)

    if not type_of:
        raise ValueError("Check attribute section, it is not properly structured")

    typ, imports = process_type(type_of, fqcn=object_fqcn, annotations=annotations, generic_types=generic_types)
    if not typ:
        raise ValueError("The attribute type could not be parsed")
    return typ, imports


def __get_type_checked(name, doc):
    if not doc or not type(doc) == dict:
        raise ValueError(f"Please check the type information of member {name}")
