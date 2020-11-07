import os
import sys
import importlib
import inspect
from src import util
from src.gen_python_code import PyCodeGenerator, get_python_prefix
from src.gen_lua_code import LuaCodeGenerator, get_lua_prefix
import argparse
import argcomplete
import shutil

def out_code(out_dir, protocol_file, code, ext):
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(protocol_file))[0]
    out_path = os.path.join(out_dir, '{0}{1}'.format(base_name, ext))
    with open(out_path, 'w') as fd:
        fd.write(code)

def main(root, py_out, lua_out):
    sys.path.append(root)
    for file in os.listdir(root):
        path = os.path.join(root, file)
        if os.path.isdir(path):
            continue
        module_path = util.to_module_name(file)
        module = importlib.import_module(module_path)
        cls_lst = inspect.getmembers(module, inspect.isclass)
        py_code = get_python_prefix()
        lua_code = get_lua_prefix()
        for (cls_name, cls_info) in cls_lst:
            py_code = py_code + PyCodeGenerator().gen(cls_info)
            lua_code = lua_code + LuaCodeGenerator().gen(cls_info)
        out_code(py_out, file, py_code, '.py')
        out_code(lua_out, file, lua_code, '.lua')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='input source')
    parser.add_argument('--py_out', help='python out file')
    parser.add_argument('--lua_out', help='lua out file')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not args.input or not (args.py_out or args.lua_out):
        parser.print_usage()
        exit(1)
    main(args.input, args.py_out, args.lua_out)

