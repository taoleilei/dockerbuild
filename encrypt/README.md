# Overview
- python代码加密：将python代码编译成c/c++，然后再编译成python的扩展模块，即`.os`文件，起到保护python代码的目的，防止别修改/查看你的Python源码。
- License控制：为你的Python代码指定运行的主机，即只有获得你授权的计算机才能运行你的python代码，同时也可以为python代码设置有效期，过期后无法运行。


# Requirement
```
apt-get install autoconf gcc g++ python3-dev
```

```
pip install pycrypto Cython
```
- `pycrypto`（注意：在win10环境下安装这个包可能会报错，解决办法见[这里](<https://blog.csdn.net/woay2008/article/details/79905627>) ）
  
# Usage

### Step 0: Preparation
- 安装依赖包: `sudo apt-get install python3-dev gcc autoconf g++`, `pip install Cython pycrypto`
- 准备好你的加密秘钥和解密秘钥
密钥的格式参考`certificate/create_license.py`里的`seperateKey`, `SeperateKeyTwo`, `aesKey `,`aesIv`
- 准备好你待权授的计算机的序列号及MAC地址

### Step 1: 加密python代码
将`example/get_time.py`加密
- 加密后会删除原文件，根据需要备份待加密的代码。

```
cp certificate/setup.py example/
cd example/
python setup.py build_ext --inplace
```
程序运行成功的话会生成与`.py`文件同名的`.os`文件，加密完成

### Step 2: 授权给用户主机
- 获取目标主机的序列号及MAC地址
用`/certificate/machine_info.py`这个脚本获取目标主机的序列号及MAC地址
```python
cd ../certificate
python machine_info.py
```

- 指定`create_license.py`中的密钥：`seperateKey`, `SeperateKeyTwo`, `aesKey`, `aesIv`
```python
python create_license.py <序列号及MAC地址> <证书有效期>
```

- 验证证书
```python
python verify_license.py
```

### Step 3: 测试
```
cd ../example/
python main.py
```