import os
import importlib
import inspect
from src import util
from src.gen_python_code import PyCodeGenerator, get_python_prefix
from src.gen_lua_code import LuaCodeGenerator, get_lua_prefix

def out_code(out_dir, protocol_file, code, ext):
    base_name = os.path.splitext(os.path.basename(protocol_file))[0]
    out_path = os.path.join(out_dir, '{0}{1}'.format(base_name, ext))
    with open(out_path, 'w') as fd:
        fd.write(code)

def main(root, out_dir):
    for file in os.listdir(root):
        path = os.path.join(root, file)
        if os.path.isdir(path):
            continue
        module_path = util.to_module_name(path)
        module = importlib.import_module(module_path)
        cls_lst = inspect.getmembers(module, inspect.isclass)
        py_code = get_python_prefix()
        lua_code = get_lua_prefix()
        for (cls_name, cls_info) in cls_lst:
            py_code = py_code + PyCodeGenerator().gen(cls_info)
            lua_code = lua_code + LuaCodeGenerator().gen(cls_info)
        out_code(out_dir, file, py_code, '.py')
        out_code(out_dir, file, lua_code, '.lua')

if __name__ == '__main__':
    root = 'protocol'
    out_dir = 'out'
    main(root, out_dir)
