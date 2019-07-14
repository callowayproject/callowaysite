FROM python:2.7

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y


RUN apt-get install -y \
# Misc system utils
    apt-utils \
    python-dev \
    git-core \
    nano \
    wget \

# XML libraries
    libxml2-dev \
    libxslt-dev \

# For some Python Extensions
    libffi-dev \

# Pillow Image Libs
    zlib1g-dev \
    libjpeg62-turbo-dev \
    libtiff5-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev

ADD . /var/www/callowaysite
WORKDIR /var/www/callowaysite
COPY requirements.txt /var/www/callowaysite
RUN pip install -r requirements.txt

COPY . /var/www/callowaysite

ENTRYPOINT ["/bin/bash", "/var/www/callowaysite/docker_run.sh"]

EXPOSE 8000