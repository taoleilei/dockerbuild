# coding:utf-8
import socket
import fcntl
import datetime
import os
import struct
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import time


class VerifyLicense:
    def __init__(self):
        self.seperateKey = "d#~0^38J^"
        self.seperateKeyTwo = "$deadline"
        self.aesKey = "b#a@&o23hw%sq&7z@9z-ooc&znd&nkw@"
        self.aesIv = "wkn&dnz&32o&@a#b"
        self.aesMode = AES.MODE_CBC

    @staticmethod
    def getHwAddr(ifname):
        """
        获取主机物理地址
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack(
            '256s', ifname[:15])).decode('utf-8')
        return ''.join(['%02x' % ord(char) for char in info[18:24]])

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

    def getLicenseInfo(self, dev='ens33', filePath="./license.lic"):
        """
        反解证书信息
        """
        if not os.path.exists(filePath):
            print("检查当前路径下是否存在license.lic证书文件")
            return False, 'Invalid'

        encryptText = ""
        with open(filePath, "r") as licfile:
            encryptText = licfile.read()
        if not encryptText:
            print(f"检查证书是否损坏")
            return False, "Invalid"

        try:
            hostInfo = self.getHwAddr(bytes(dev, encoding='utf-8'))
        except IOError:
            print(f"检查设备{dev}是否正常工作")
            return False, "Invalid"

        decryptText = self.decrypt(encryptText)
        pos = decryptText.find(self.seperateKey)
        end = decryptText.find(self.seperateKeyTwo)
        if pos == -1 or end == -1:
            print("证书已损坏或不合法")
            return False, "Invalid"

        deadline = decryptText[pos + len(self.seperateKey): end]
        if datetime.datetime.now() > datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S'):
            print("证书已过期，请重新申请")
            return False, "Invalid"

        licHostInfo = self.decrypt(decryptText[0:pos])
        licenseStr = decryptText[end + len(self.seperateKeyTwo):]

        return (True, licenseStr) if licHostInfo == hostInfo else (False, 'Invalid')


License = VerifyLicense()
Condition, LicInfo = License.getLicenseInfo()


class Varification:
    def __init__(self, fc):
        self._func = fc
        self.condition = Condition
        self.licinfo = LicInfo

    def __call__(self, *args, **kwargs):
        if self.condition and self.licinfo == "Valid":
            self._func(*args, **kwargs)
        else:
            print('未获取权授！')


class Decrator:
    def __init__(self, func):
        self._func = func
        self.condition = Condition
        self.licinfo = LicInfo

    def __get__(self, instance, owner):
        '''
        instance:代表实例，被装饰的方法中的self
        owner：代表类本身，被装饰的类
        '''
        if self.condition and self.licinfo == "Valid":
            self._func(instance)
        else:
            print('未获取权授！')


class Today:
    @Decrator
    def get_time(self):
        print(datetime.datetime.now())

    @Decrator
    def say(self):
        print('hello world!')
        localtime = time.asctime(time.localtime(time.time()))
        print("The local time is now:", localtime)
