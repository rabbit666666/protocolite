import collections
import inspect
import os
import typing

def to_module_name(path):
    base_name = os.path.splitext(path)[0]
    module_path = base_name.replace('\\', '.')
    return module_path

def get_field(cls_info):
    fields = collections.OrderedDict()
    type_hint = typing.get_type_hints(cls_info)
    for (name, hint_info) in type_hint.items():
        def_value = None
        if hasattr(cls_info, name):
            def_value = getattr(cls_info, name)
        fields[name] = {'type': hint_info, 'def_value': def_value}
    return fields

def get_protocol_class(module):
    cls_lst = inspect.getmembers(module, inspect.isclass)
    cls_lst2 = []
    for (cls_name, cls_info) in cls_lst:
        if cls_name in ['List']:
            continue
        cls_lst2.append(cls_info)
    return cls_lst2

def is_custom_class_array(hint_info):
    t = hint_info['type']
    return type(t) == list and \
           (t[0].__name__ not in ['str', 'int', 'float'])

def is_custom_class(hint_info):
    t = hint_info['type']
    if t in [str, int, float, list, dict, bool]:
        is_custom = False
    elif isinstance(t, list) and t[0] in [str, int, float, list, dict, bool]:
        is_custom = False
    else:
        is_custom = True
    return is_custom
