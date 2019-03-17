FROM python:3.7-alpine
COPY . /app
WORKDIR /app
# install openssl
RUN apk add --no-cache --virtual .build-deps build-base curl-dev && \
    rm -rf /var/cache/apk/*
ENV PYCURL_SSL_LIBRARY=openssl
RUN pip install pycurl --compile --no-cache-dir && pip install -r requirements.txt
