import time
import datetime
import subprocess
import asyncio
import re


async def ping_call(num):
    # 当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ip = "192.168.125.%s" % num
    # 超时时间为1秒，ping 1次
    # cmd = 'ping -c 1 -w 1 -W 1 %s' % ip
    # print(cmd)
    proc = await asyncio.create_subprocess_exec('ping', '-c', '1', '-w', '1', '-W', '1', ip,
                                                stdout=asyncio.subprocess.PIPE)
    # print("proc",proc,type(proc))
    result = await proc.stdout.read()

    # 通过正则匹配是否有100%关键字
    regex = re.findall('100% packet loss', result.decode('utf-8'))
    # 长度为0时，表示没有出现100% packet loss
    if len(regex) == 0:
        return current_time, ip, True
    else:
        return current_time, ip, False


async def main():  # 调用方
    tasks = []
    for i in range(1, 256):
        tasks.append(ping_call(i))
    # 子生成器
    done, pending = await asyncio.wait(tasks)
    # done和pending都是一个任务，所以返回结果需要逐个调用result()
    for r in done:
        # print(r.result())
        # 判断布尔值
        if r.result()[2]:
            # 颜色代码
            color_code = 32
        else:
            color_code = 31

        info = "\033[1;{};1m{}\033[0m".format(color_code, r.result())
        print(info)


if __name__ == '__main__':
    start = time.perf_counter()
    # 创建一个事件循环对象loop
    # loop = asyncio.get_event_loop()
    # try:
    #     # 完成事件循环，直到最后一个任务结束
    #     loop.run_until_complete(main())
    # finally:
    #     # 结束事件循环
    #     loop.close()
    asyncio.run(main())
    print('所有IO任务总耗时%.5f秒' % float(time.perf_counter() - start))
