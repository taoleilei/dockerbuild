FROM python:3.7-alpine
LABEL maintainer="taoleilei <taoleilei6176@163.com>"

RUN apk update \
    && apk add --no-cache ca-certificates \
    && apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add git

ENV NOVNC /var/noVNC

WORKDIR /var/

COPY requirements.txt /var/

RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/novnc/noVNC \
    && git clone https://github.com/novnc/websockify ${NOVNC}/utils/websockify \
    && chmod +x ${NOVNC}/utils -R

RUN rm -rf /var/cache/apk/* \
    && apk del .build-deps gcc musl-dev git

WORKDIR ${NOVNC}/utils/

EXPOSE 6080