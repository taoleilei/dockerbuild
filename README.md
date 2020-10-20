# dockerbuild
### dockercloud

### novnc 
#### docker-compose up -d
#### http://192.168.119.12:32768/vnc.html?path=websockify/?token=31394248

### www  

### updog  

### docker-ngrok
#### 内网主机运行ngrok客户端，公网服务器（有域名）运行服务端
#### docker启动服务端程序 docker run -it -d --name ngrok-server -p 80:80 -p 443:443 -p 2222:2222 -p 4443:4443 -v /root/media/ngrok:/myfiles -e DOMAIN='ngrok.iiebc.com' hteen/ngrok /bin/sh /server.sh 
#### 客户端配置
```
http https
ngrok.cfg
    - server_addr: "ngrok.iiebc.com:4443"
    - trust_host_root_certs: false
start.bat
    - ngrok.exe -config ngrok.cfg -log ngrok.log -subdomain test 8000
访问test.ngrok.iiebc.com
```
```
tunnel
ngrok.cfg
    server_addr: "ngrok.iiebc.com:4443"
    trust_host_root_certs: false
    tunnels:
        webapp:
            proto:
                http: 8000
                https: 8000
            subdomain: test
        tcp2222:
            remote_port: 2222
            proto:
                tcp: 2222
start.bat
    ngrok.exe -config ngrok.cfg start webapp tcp2222
```