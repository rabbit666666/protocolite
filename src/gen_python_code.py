import json
from src import util

def to_py_value(value):
    if type(value) in [str, int, float]:
        py_value = json.dumps(value)
    elif type(value) in [list]:
        py_value = []
    elif type(value) in [dict]:
        py_value = {}
    else:
        py_value = '{}()'.format(type(value).__name__)
    return py_value

def get_python_prefix():
    return 'import json\n'

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
        print(code)
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
            member = '''
    def set_{name}(self, value):
        assert isinstance(value, {value_type}), "set_{name}. need {value_type}, but pass:{{}}".format(type(value))
        self._has_{name} = True
        self._{name} = value
    def get_{name}(self):
        return self._{name}
    def has_{name}(self):
        return self._has_{name}
    '''.format(name=name, value_type=type(value).__name__)
            setter_getter_code.append(member)
        return ''.join(setter_getter_code)

    def _gen_parse_code(self, fields):
        code = '''
    def parse(self, msg):        
        msg = json.loads(msg)'''
        for (name, value) in fields.items():
            code += '''
        if "{name}" in msg:
            self._has_{name} = True'''.format(name=name)
            if util.is_custom_class(value):
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
        msg["name"] = "{cls_name}"'''.format(cls_name=self.cls_name)
        for (name, value) in fields.items():
            code += '''
        if self._has_{name}:'''.format(name=name)
            if util.is_custom_class(value):
                code += '''        
            msg["{name}"] = self._{name}.serialize()'''.format(name=name)
            else:
                code += '''
            msg["{name}"] = self._{name}'''.format(name=name)
        code += '''
        return json.dumps(msg)'''
        return code
