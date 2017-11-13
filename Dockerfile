# --------------------------------------------------------------------
# | Usage Rec:
# |
# |   docker run -v $PWD:/img mozjpeg sh -c "/mozjpeg/cjpeg -quality 80 /img/photo.jpg > /img/photo_small.jpg"
# |
# |
FROM python:3.6

RUN apt-get update \
	&& apt-get install -yq --fix-missing ca-certificates nginx gettext-base supervisor


RUN apt-get install -yq --fix-missing autoconf automake libtool nasm make pkg-config exiv2 wget \
    && wget --no-check-certificate \
        https://github.com/mozilla/mozjpeg/releases/download/v3.2/mozjpeg-3.2-release-source.tar.gz -O - | tar -xz \
    && ( \
        cd ./mozjpeg/ \
        && autoreconf -fiv \
        && ./configure --prefix=/opt/mozjpeg \
        && make install \
    )


RUN pip install uwsgi

## #################
##      Nginx
## #################

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log \
	&& echo "daemon off;" >> /etc/nginx/nginx.conf \
	&& rm /etc/nginx/sites-enabled/default

# Copy the modified Nginx conf
COPY ./docker/nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./docker/uwsgi.ini /etc/uwsgi/


## #################
##   Supervisord
## #################

# Custom Supervisord config
COPY ./docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf


## #################
##     Project
## #################

RUN mkdir /store \
    && mkdir /store/source \
    && mkdir /store/convert \
    && mkdir /store/optimized

COPY  ./project/ /project/
WORKDIR /project

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80 443
CMD ["/usr/bin/supervisord"]