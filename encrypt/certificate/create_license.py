# -*- coding: UTF-8 -*-
import os
import sys
import base64
import datetime

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

SeperateKey = "d#~0^38J^"
SeperateKeyTwo = "$deadline"
AesKey = "b#a@&o23hw%sq&7z@9z-ooc&znd&nkw@"  # 加密与解密所使用的密钥，长度必须是16的倍数
AesIv = "wkn&dnz&32o&@a#b"  # initial Vector,长度要16位
AesMode = AES.MODE_CBC  # 使用CBC模式


def encrypt(text):
    cryptor = AES.new(AesKey, AesMode, AesIv)

    # padding
    add, length = 0, 16
    count = len(text)
    if count % length != 0:
        add = length - (count % length)
    text = text + ('\0' * add)  # '\0'*add 表示add个空格,即填充add个直至符合16的倍数

    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串 ,当然也可以转换为base64加密的内容，可以使用b2a_base64(self.ciphertext)
    return b2a_hex(ciphertext).upper().decode()


if __name__ == "__main__":
    arg_len = len(sys.argv)
    # 无参数输入则退出
    if arg_len < 2:
        print("usage: python {} host_info".format(sys.argv[0]))
        sys.exit(0)

    host_info = sys.argv[1]  # host_info是运行此脚本时传入的mac地址
    lifetime = int(sys.argv[2]) if arg_len == 3 else 30

    encrypt_text = encrypt(host_info)  # 将mac地址第一次加密

    deadline = datetime.datetime.now() + datetime.timedelta(days=lifetime)
    encrypt_text = f"{encrypt_text}{SeperateKey}{deadline.strftime('%Y-%m-%d %H:%M:%S')}{SeperateKeyTwo}Valid"
    encrypt_text = encrypt(encrypt_text)  # 将加密之后的密文再次加密

    with open("./license.lic", "w+") as licfile:
        licfile.write(encrypt_text)

    print("license已生成")
