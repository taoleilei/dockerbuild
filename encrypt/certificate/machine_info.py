# -*- coding: UTF-8 -*-
# 获取计算机的物理地址

import fcntl
import socket
import struct
import subprocess

import psutil


def get_mac_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,
                       struct.pack('256s', ifname[:15])).decode('utf-8')
    # print(info.decode('utf-8'))
    return ''.join(['%02x' % ord(char) for char in info[18:24]])


def get_manufacturer_info():
    # 制造商信息
    result = {}
    cmd = "/usr/sbin/dmidecode | grep -A6 'System Information'"
    data = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in data.stdout.readlines():
        line = str(line, encoding='utf8')
        if 'Manufacturer' in line:
            result['manufacturer'] = line.split(':')[1].strip()
        elif 'Product Name' in line:
            result['product name'] = line.split(':')[1].strip()
        elif 'Serial Number' in line:
            result['serial number'] = line.split(
                ':')[1].strip().replace(' ', '')
        elif 'UUID' in line:
            result['uuid'] = line.split(':')[1].strip()
        elif 'Version' in line:
            result['version'] = line.split(':')[1].strip()
    return result


def get_device_info():
    # 获取网卡ip与mac
    include_device = ('eth0', 'ens33')
    result = []
    for device, device_info in psutil.net_if_addrs().items():
        if device in include_device:
            tmp_device = {}
            for sinc in device_info:
                if sinc.family == 2:
                    # 获取Ipv4
                    tmp_device['ip'] = sinc.address
                if sinc.family == 17:
                    tmp_device['mac'] = sinc.address
            tmp_device["device"] = device
            result.append(tmp_device)
    return result


def get_machine_code():
    """
    docstring
    """
    try:
        man_info = get_manufacturer_info()
        dev_info = get_device_info()
        serial_number = man_info["serial number"]
        device_mac = f"{dev_info[0]['mac'].replace(':', '')}"
        return dev_info[0]['device'], f"{serial_number}:{device_mac}"
    except Exception as e:
        raise IOError


if __name__ == '__main__':
    # try:
    #     print(get_mac_addr(b'ens33'))
    # except IOError:
    #     print(get_mac_addr(b'eth0'))
    print(get_machine_code())
