FROM python:3.7
MAINTAINER taoleilei <taoleilei6176@163.com>

RUN apt-get update

RUN apt-get -y install git build-essential \
    && pip install numpy

RUN cd /var/ \
    && git clone https://github.com/novnc/noVNC.git \
    && cd /var/noVNC/utils/ \
    && git clone https://github.com/novnc/websockify.git

RUN chmod +x /var/noVNC/utils -R

WORKDIR /var/noVNC/utils/

EXPOSE 6080