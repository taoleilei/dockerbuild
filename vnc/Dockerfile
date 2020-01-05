FROM python:2.7
MAINTAINER taoleilei <taoleilei6176@163.com>

RUN apt-get update

RUN apt-get -y install build-essential

COPY noVNC /var/noVNC/

WORKDIR /var/noVNC/utils/

RUN pip install -r requirements.txt

RUN chmod +x /var/noVNC/utils -R

EXPOSE 6081