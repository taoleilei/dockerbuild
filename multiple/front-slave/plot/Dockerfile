FROM python:3.8
LABEL maintainer=" taoleilei <taoleilei@iie.ac.cn>"

COPY sources.list /etc/apt

# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5 && \
#     apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32

RUN apt-get update

RUN apt-get -y install default-libmysqlclient-dev build-essential

COPY requirements.txt /var/www/

WORKDIR /var/www/

RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

RUN rm -rf /var/lib/apt/lists/*

EXPOSE 8000