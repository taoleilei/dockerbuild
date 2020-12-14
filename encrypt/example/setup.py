# coding:utf-8
import os
import time
import shutil
from pathlib import Path
from distutils.core import setup
from distutils.extension import Extension
from concurrent.futures import ProcessPoolExecutor

from Cython.Build import cythonize
'''
该文件的执行需要的在Terminal中输入   python setup.py build_ext --inplace
使用Cpython 编译python文件，关键函数编译成pyd文件（相当于dll）
'''


def main(ignore_files):
    """
    编译python源代码
    """
    extensions = []
    p = Path('.')
    files = list(p.glob('**/*.py'))
    for file in files:
        if file.name not in ignore_files:
            if file.parent == p:
                extensions.append(
                    Extension(file.name.rsplit('.', 1)[0], [file.name]))
            else:
                extensions.append(Extension(f"{'.'.join(file.parent.__str__().split('/'))}.{file.name.rsplit('.', 1)[0]}", [
                    Path(file.parent, file.name).__str__()]))

    # extensions = [
    #     Extension("get_time", ["get_time.py"])
    # ]
    print(extensions)

    setup(
        name="App",
        version="2.0",
        ext_modules=cythonize(extensions),
    )

    rm_files = list(p.glob('**/*.c')) + \
        list(p.glob('**/*.py')) + list(p.glob('**/*.pyc'))
    for fi in rm_files:
        if fi.name not in ignore_files:
            os.remove(fi)

    shutil.rmtree(p / 'build')


if __name__ == "__main__":
    ignore_files = ["setup.py", "manage.py",
                    "settings.py", "main.py", "__init__.py"]
    main(ignore_files)
    print('Done!')
