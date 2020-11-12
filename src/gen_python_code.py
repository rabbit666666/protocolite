import json
from src import util

def to_py_value(hint_info):
    t = hint_info['type']
    if t in [str, int, float, bool]:
        py_value =  hint_info['def_value']
        if py_value is not None:
            py_value = json.dumps(py_value)
    elif t in [list] or type(t) in [list]:
        py_value = []
    elif t in [dict]:
        assert False, "unsupport dict, please use class insted it."
    else:
        py_value = '{}()'.format(t.__name__)
    return py_value

def get_py_type(hint_info):
    t = hint_info['type']
    if isinstance(t, type):
        return t
    else:
        return type(t)

def get_python_prefix():
    code = '''
import json
def parse(msg):
    msg_name = msg["__msg__"]
    obj = globals()[msg_name]()
    return obj.parse(msg)'''
    return code

class PyCodeGenerator:
    def __init__(self):
        self.cls_name = None

    def gen(self, cls_info):
        self.cls_name = cls_info.__name__
        fields = util.get_field(cls_info)
        field_code = self._gen_fields(fields)
        setget_code = self._gen_getter_setter(fields)
        parse_code = self._gen_parse_code(fields)
        serialize_code = self._gen_serialize_code(fields)
        code = '''
class {cls_name}:
    {fields_code}
    {setget_code}
    {parse_code}
    {serialize_code}
        '''.format(cls_name=self.cls_name, fields_code=field_code, setget_code=setget_code,
                   parse_code=parse_code, serialize_code=serialize_code)
        #print(code)
        return code

    def _gen_fields(self, fields):
        field_code = '''def __init__(self):'''
        for (name, value) in fields.items():
            value = to_py_value(value)
            field_code += '''
        self._{name} = {value}
        self._has_{name} = False'''.format(name=name, value=value)
        return field_code

    def _gen_getter_setter(self, fields):
        setter_getter_code = []
        for (name, value) in fields.items():
            t = get_py_type(value)
            member = '''
    def set_{name}(self, value):
        assert isinstance(value, {value_type}), "set_{name}. need {value_type}, but pass:{{}}".format(type(value))
        self._has_{name} = True
        self._{name} = value
    def get_{name}(self):
        return self._{name}
    def has_{name}(self):
        return self._has_{name}
    '''.format(name=name, value_type=t.__name__)
            setter_getter_code.append(member)
        return ''.join(setter_getter_code)

    def _gen_parse_code(self, fields):
        code = '''
    def parse(self, msg):
        if isinstance(msg, str):        
            msg = json.loads(msg)'''
        for (name, hint) in fields.items():
            code += '''
        if "{name}" in msg:
            self._has_{name} = True'''.format(name=name)
            if util.is_custom_class_array(hint):
                code += '''
            self._{name} = []
            for x in msg["{name}"]:
                self._{name}.append({ele_type}().parse(x))'''.format(name=name, ele_type=hint['type'][0].__name__)
            elif util.is_custom_class(hint):
                code += '''            
            self._{name}.parse(msg["{name}"])'''.format(name=name)
            else:
                code += '''
            self._{name} = msg["{name}"]'''.format(name=name)
        code += '''
        return self'''
        return code

    def _gen_serialize_code(self, fields):
        code = '''
    def serialize(self):
        msg = {{}}
        msg["__msg__"] = "{cls_name}"'''.format(cls_name=self.cls_name)
        for (name, value) in fields.items():
            code += '''
        if self._has_{name}:'''.format(name=name)
            if util.is_custom_class_array(value):
                code += '''
            _{name} = []
            for x in self._{name}:
                _{name}.append(x.serialize())
            msg["{name}"] = _{name}'''.format(name=name)
            elif util.is_custom_class(value):
                code += '''        
            msg["{name}"] = self._{name}.serialize()'''.format(name=name)
            else:
                code += '''
            msg["{name}"] = self._{name}'''.format(name=name)
        code += '''
        return msg'''
        return code
