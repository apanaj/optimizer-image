# --------------------------------------------------------------------
# | Usage Rec:
# |
# |   docker run -v $PWD:/img mozjpeg sh -c "/mozjpeg/cjpeg -quality 80 /img/photo.jpg > /img/photo_small.jpg"
# |
# |
FROM python:3.6.2-alpine3.6

MAINTAINER Payam Naderi <naderi.payam@gmail.com>

RUN apk --update add autoconf automake build-base libtool nasm wget
RUN wget --no-check-certificate \
    https://github.com/mozilla/mozjpeg/releases/download/v3.2/mozjpeg-3.2-release-source.tar.gz -O - | tar -xz \
    && ( \
        cd ./mozjpeg/ \
        && autoreconf -fiv \
        && ./configure --prefix=/opt/mozjpeg \
        && make install \
    )

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app
COPY  ./app/ .

CMD [ "python", "./app.py" ]