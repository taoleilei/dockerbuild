FROM python:3.8-alpine
LABEL maintainer="taoleilei <taoleilei6176@163.com>"

RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.12/main/ > /etc/apk/repositories

RUN apk update \
    && apk add --no-cache ca-certificates \
    && apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add git

ENV NOVNC /var/noVNC

WORKDIR /var/

COPY requirements.txt /var/

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.douban.com/simple/

RUN git clone https://github.com/novnc/noVNC \
    && git clone https://github.com/novnc/websockify ${NOVNC}/utils/websockify \
    && chmod +x ${NOVNC}/utils -R

RUN rm -rf /var/cache/apk/* \
    && apk del .build-deps gcc musl-dev git

WORKDIR ${NOVNC}/utils/

EXPOSE 6080