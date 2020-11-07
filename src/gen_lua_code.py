from src import util

def to_lua_type(def_value):
    if type(def_value) in [str]:
        emmy_t = 'string'
    elif type(def_value) in [int, float]:
        emmy_t = 'number'
    elif type(def_value) in [list, map]:
        emmy_t = 'table'
    else:
        emmy_t = 'table'
    return emmy_t

def get_lua_prefix():
    code = '''
local json = require("cjson")

local function extend_lua_object(lua_object, mt)
    local old_mt = getmetatable(lua_object)    
    mt.__index = mt
    setmetatable(lua_object, mt)
end'''
    return code

class LuaCodeGenerator:
    def __init__(self):
        pass

    def gen(self, cls_info):
        self.cls_name = cls_info.__name__
        fields = util.get_field(cls_info)
        create_code = self._gen_create_code()
        parse_code = self._gen_parse_code(fields)
        serialize_code = self._gen_serialize_code(fields)
        setget_code = self._gen_getter_setter(fields)
        code = '''
{create_code}
{parse_code}
{serialize_code}
{setget_code}
'''.format(create_code=create_code, parse_code=parse_code, serialize_code=serialize_code, setget_code=setget_code)
        return code

    def _gen_create_code(self):
        code = '''
-----------------------------------------------
---@class {cls_name}
{cls_name} = {{}}
---@return {cls_name}
function {cls_name}.new()
    local self = {{}}   ---@type {cls_name}
    extend_lua_object(self, {cls_name})
    return self
end'''.format(cls_name=self.cls_name)
        return code

    def _gen_parse_code(self, fields):
        code = '''
---@param msg string
---@return {cls_name}
function {cls_name}:parse(msg)
    msg = json.decode(msg)'''.format(cls_name=self.cls_name)
        for (value_name, value) in fields.items():
            if util.is_custom_class(value):
                cls_name = type(value).__name__
                code += '''
    if msg["{name}"] then
        self._has_{name} = true
        self._{name} = {cls_name}.new()
        self._{name}:parse(msg["{name}"])
    end'''.format(name=value_name, cls_name=cls_name)
            else:
                code += '''
    if msg["{name}"] then 
        self._has_{name} = true
        self._{name} = msg["{name}"]
    end'''.format(name=value_name)
        code += '''
    return self
end'''
        return code

    def _gen_serialize_code(self, fields):
        code = '''
---@return string
function {cls_name}:serialize()
    local msg = {{}}'''.format(cls_name=self.cls_name)
        for (value_name, value) in fields.items():
            if util.is_custom_class(value):
                code += '''
    if self._has_{name} then
        msg["{name}"] = self._{name}:serialize()
    end'''.format(name=value_name)
            else:
                code += '''
    if self._has_{name} then
        msg["{name}"] = self._{name}
    end'''.format(name=value_name)
        code += '''
    return json.encode(msg)
end'''
        return code

    def _gen_getter_setter(self, fields):
        setter_getter_code = []
        for (value_name, value) in fields.items():
            member = '''
---@param value {value_type}                        
function {cls_name}:set_{value_name}(value)
    assert(type(value) == "{value_type}", 
           string.format("set_{value_name}. need {value_type}, but pass:%s", type(value)))
    self._has_{value_name} = true
    self._{value_name} = value
end
---@return {value_type}
function {cls_name}:get_{value_name}()
    return self._{value_name}
end
---@return boolean
function {cls_name}:has_{value_name}()
    return self._has_{value_name}
end
'''.format(cls_name=self.cls_name, value_name=value_name, value_type=to_lua_type(value))
            setter_getter_code.append(member)
        return ''.join(setter_getter_code)
