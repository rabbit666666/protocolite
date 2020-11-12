from src import util

def to_lua_type(hint):
    t = hint['type']
    if isinstance(t, list):
        emmy_t = '{}[]'.format(t[0].__name__)
        lua_t = 'table'
    elif t in [str]:
        emmy_t = 'string'
        lua_t = 'string'
    elif t in [int, float]:
        emmy_t = 'number'
        lua_t = 'number'
    elif t in [bool]:
        emmy_t = 'boolean'
        lua_t = 'boolean'
    else:
        emmy_t = t.__name__
        lua_t = 'table'
    return emmy_t, lua_t

def get_lua_prefix():
    code = '''
local json = require("cjson")
local _m = {}
local function extend_lua_object(lua_object, mt)
    local old_mt = getmetatable(lua_object)    
    mt.__index = mt
    setmetatable(lua_object, mt)
end
---@param msg string|table
function _m.parse(msg)
    local msg_name = msg["__msg__"]
    local obj = _m["new_" .. msg_name]()
    obj:parse(msg)
    return obj
end
'''
    return code

def get_lua_suffix():
    code = '''
return _m
'''
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
_m.{cls_name} = "{cls_name}"
---@class {cls_name}
local {cls_name} = {{}}
---@return {cls_name}
function _m.new_{cls_name}()
    local self = {{}}   ---@type {cls_name}
    extend_lua_object(self, {cls_name})
    return self
end'''.format(cls_name=self.cls_name)
        return code

    def _gen_parse_code(self, fields):
        code = '''
---@param msg string|table
---@return {cls_name}
function {cls_name}:parse(msg)
    if type(msg) == "string" then
        msg = json.decode(msg)
    end'''.format(cls_name=self.cls_name)
        for (value_name, hint) in fields.items():
            t = hint['type']
            if util.is_custom_class_array(hint):
                cls_name = t[0].__name__
                code += '''
    if msg["{name}"] then
        self._has_{name} = true
        self._{name} = {{}}
        for i, x in pairs(msg["{name}"]) do
            self._{name}[i] = _m.new_{cls_name}():parse(x)
        end        
    end'''.format(name=value_name, cls_name=cls_name)
            elif util.is_custom_class(hint):
                cls_name = t.__name__
                code += '''
    if msg["{name}"] then
        self._has_{name} = true
        self._{name} = _m.new_{cls_name}()
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
---@return table
function {cls_name}:serialize()
    local msg = {{}}
    msg["__msg__"] = "{cls_name}"'''.format(cls_name=self.cls_name)
        for (value_name, hint) in fields.items():
            if util.is_custom_class_array(hint):
                code += '''
    if self._has_{name} then
        _{name} = {{}}
        for i, x in pairs(self._{name}) do
            _{name}[i] = x:serialize()
        end
        msg["{name}"] = _{name}
    end'''.format(name=value_name)
            elif util.is_custom_class(hint):
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
    return msg
end'''
        return code

    def _gen_getter_setter(self, fields):
        setter_getter_code = []
        for (value_name, value) in fields.items():
            emmy_t, lua_t = to_lua_type(value)
            member = '''
---@param value {emmy_type}
function {cls_name}:set_{value_name}(value)
    assert(type(value) == "{lua_type}", 
           string.format("set_{value_name}. need {lua_type}, but pass:%s", type(value)))
    self._has_{value_name} = true
    self._{value_name} = value
end
---@return {emmy_type}
function {cls_name}:get_{value_name}()
    return self._{value_name}
end
---@return boolean
function {cls_name}:has_{value_name}()
    return self._has_{value_name}
end
'''.format(cls_name=self.cls_name, value_name=value_name, emmy_type=emmy_t, lua_type=lua_t)
            setter_getter_code.append(member)
        return ''.join(setter_getter_code)
