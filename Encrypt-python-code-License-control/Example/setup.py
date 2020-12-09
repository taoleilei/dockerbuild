# coding:utf-8
import os
import shutil
from pathlib import Path
from distutils.core import setup
from concurrent.futures import ProcessPoolExecutor

from Cython.Build import cythonize
'''
该文件的执行需要的在Terminal中输入   python setup.py build_ext --inplace 
使用Cpython 编译python文件，关键函数编译成pyd文件（相当于dll）
'''
# 在列表中输入需要加密的py文件
# key_funs = ['get_time.py']

# key_funs = []
# p = Path('.')
# files = list(p.glob('**/*.py'))
# for file in files:
#     key_funs.append(file.absolute().__str__())

# # print(key_funs)
# setup(
#     name="XX app",
#     ext_modules=cythonize(key_funs),
# )

# '''
# 1、将编译后的pyd文件的命名更改成与原py文件一致
# 2、删除编译后得到的c文件和原py文件
# '''
# print("——————", os.getcwd(), "——————")

# files = os.listdir(os.getcwd())
# print(files)

# for fi in files:
#     if fi.endswith(".pyd"):
#         re_name = fi.split(".")[0] + ".pyd"
#         print(re_name)
#         os.rename(fi, re_name)
#     elif fi.endswith(".c") or fi in key_funs:
#         os.remove(fi)

# p = Path('.')
# files = list(p.glob('**/*.so'))
# for file in files:
#     shutil.move(file.absolute().__str__(), p.absolute().__str__())
# shutil.rmtree(p / 'build')
# print('Done!')
funs_list = []


def compile(filepath):
    """
    docstring
    """
    # os.chdir(filepath)
    # print(os.getcwd().center(100, "-"))

    # funs_list = []
    p = Path(filepath)
    files = list(p.glob('*.py'))
    for file in files:
        funs_list.append(file.absolute().__str__())

    # setup(
    #     name="XX app",
    #     ext_modules=cythonize(funs_list),
    # )

    # dir_files = os.listdir(os.getcwd())
    # for fi in dir_files:
    #     if fi.endswith(".pyd"):
    #         re_name = fi.split(".")[0] + ".pyd"
    #         print(re_name)
    #         os.rename(fi, re_name)
    #     elif fi.endswith(".c") or fi in funs_list:
    #         os.remove(fi)
    # shutil.rmtree(p / 'build')


def main():
    """
    docstring
    """
    p = Path('.')
    compile(p.absolute().__str__())

    current_dir = list(p.iterdir())
    for struct in current_dir:
        if struct.is_dir():
            compile(struct.absolute().__str__())
            # compile(struct.absolute().__str__())
            # with ProcessPoolExecutor(max_workers=5) as executor:
            #     executor.map(compile, struct.absolute().__str__())


if __name__ == "__main__":
    main()
    print(funs_list)
    setup(
        name="XX app",
        ext_modules=cythonize(funs_list),
    )
    print('Done!')
