# from sanic import Sanic
# from sanic.response import json

# app = Sanic(__file__)


# @app.route("/")
# async def test(request):
#     return json({"hello": "world"})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)

import time
import datetime
import subprocess
import asyncio
import re

'''

def progress_bar(parameter_list):
    """
    docstring
    """
    scale = 50
    print("执行开始".center(scale//2, "-"))
    start = time.perf_counter()
    for i in range(scale+1):
        a = '*' * i
        b = '.' * (scale-i)
        c = (i/scale)*100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end='')
        time.sleep(0.1)

    print("\n"+"执行结果".center(scale//2, '-'))

'''
