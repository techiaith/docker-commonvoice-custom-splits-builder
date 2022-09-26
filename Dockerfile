FROM ubuntu:22.04

LABEL maintainer="techiaith"
LABEL repository="commonvoice-custom-splits-builder"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt update -q \
 && apt install -y -qq tzdata bash build-essential git curl wget software-properties-common \
    vim ca-certificates libffi-dev libssl-dev libsndfile1 libbz2-dev liblzma-dev locales \
    libboost-all-dev libboost-tools-dev libboost-thread-dev cmake  \
    python3 python3-pip python3-setuptools python3-dev curl zip zlib1g-dev vim \
    ffmpeg sox alsa-utils \
 && python3 -m pip install --upgrade pip

# Install corporacreator
RUN mkdir -p /CorporaCreator

WORKDIR /CorporaCreator

COPY CorporaCreator /CorporaCreator
COPY patches/CorporaCreator/* /CorporaCreator/src/

RUN python3 setup.py install

# Install local Python files and dependencies..
RUN mkdir -p /custom-commonvoice

WORKDIR /custom-commonvoice

COPY python/requirements.txt /custom-commonvoice/
RUN pip3 install -r requirements.txt 

#COPY python /custom-commonvoice/