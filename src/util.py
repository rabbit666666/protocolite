import os
import collections
import inspect

def to_module_name(path):
    base_name = os.path.splitext(path)[0]
    module_path = base_name.replace('\\', '.')
    return module_path

def get_field(module):
    fields = collections.OrderedDict()
    for (name, def_value) in inspect.getmembers(module):
        if name.find('__') != -1:
            continue
        fields[name] = def_value
    return fields

def is_custom_class(value):
    if type(value) in [str, int, float, list, dict]:
        yes = False
    else:
        yes = True
    return yes
