# -*- coding: UTF-8 -*-
import base64
import datetime
import fcntl
import os
import socket
import struct
import sys
from binascii import a2b_hex, b2a_hex
from pathlib import Path

from Crypto.Cipher import AES

from . import machine_info

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


class VerifyLicense:
    def __init__(self):
        self.seperateKey = "d#~0^38J^"
        self.seperateKeyTwo = "$deadline"
        self.aesKey = "b#a@&o23hw%sq&7z@9z-ooc&znd&nkw@"
        self.aesIv = "wkn&dnz&32o&@a#b"
        self.aesMode = AES.MODE_CBC

    def decrypt(self, text):
        """
        从.lic中解密出主机地址
        """
        result = ""
        try:
            cryptor = AES.new(self.aesKey, self.aesMode, self.aesIv)
            plain_text = cryptor.decrypt(a2b_hex(text)).decode('utf-8')
            result = plain_text.rstrip('\0')
        except Exception as ex:
            pass

        return result

    def get_license_info(self, filename="license.lic"):
        """
        反解证书信息
        """
        file_path = Path(BASE_DIR, filename)
        if not os.path.exists(file_path):
            print("检查当前路径下是否存在license.lic证书文件")
            return False, 'Invalid'

        encrypt_text = ""
        with open(file_path, "r") as licfile:
            encrypt_text = licfile.read()
        if not encrypt_text:
            print(f"检查证书是否损坏")
            return False, "Invalid"

        try:
            host_key = machine_info.get_machine_code()[1]
        except IOError:
            print("检查设备是否正常工作")
            return False, "Invalid"

        decrypt_text = self.decrypt(encrypt_text)
        pos = decrypt_text.find(self.seperateKey)
        end = decrypt_text.find(self.seperateKeyTwo)
        if pos == -1 or end == -1:
            print("证书已损坏或不合法")
            return False, "Invalid"

        deadline = decrypt_text[pos + len(self.seperateKey): end]
        if datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S'):
            print("证书已过期，请重新申请")
            return False, "Invalid"

        lic_host_info = self.decrypt(decrypt_text[0:pos])
        license_status = decrypt_text[end + len(self.seperateKeyTwo):]

        return (True, license_status, deadline) if lic_host_info == host_key else (False, 'Invalid', "")


if __name__ == "__main__":
    License = VerifyLicense()
    print(License.get_license_info())
