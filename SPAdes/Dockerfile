#The Dockerfile is based on STaPH-B groups docker build,
#modified to run utilize alpin 3.20.3 instead of ubuntu
FROM alpine:3.20.3 as app

# ARG variables to facilitate version upgrades
ARG SPADES_VER="4.0.0"

# Labels for metadata
LABEL base.image="alpine:3.20.3"
LABEL dockerfile.version="1"
LABEL software="SPAdes"
LABEL software.version="${SPADES_VER}"
LABEL description="de novo DBG genome assembler"
LABEL website="https://github.com/ablab/spades"
LABEL license="https://github.com/ablab/spades/blob/v3.15.3/assembler/LICENSE"
LABEL maintainer="Curtis Kapsak"
LABEL maintainer.email="kapsakcj@gmail.com"

# Install dependencies using apk, cleanup after installation
RUN apk update && apk add --no-cache \
  python3 \
  py3-distutils-extra \
  wget \
  pigz \
  ca-certificates \
  libgomp && \
  ln -s /usr/bin/python3 /usr/bin/python

# Install SPAdes binary and create /data directory
RUN wget -q https://github.com/ablab/spades/releases/download/v${SPADES_VER}/SPAdes-${SPADES_VER}-Linux.tar.gz && \
  tar -xzf SPAdes-${SPADES_VER}-Linux.tar.gz && \
  rm -r SPAdes-${SPADES_VER}-Linux.tar.gz && \
  mkdir /data

# Set PATH and locale settings
ENV LC_ALL=C.UTF-8 \
  PATH="${PATH}:/SPAdes-${SPADES_VER}-Linux/bin"

CMD spades.py --help

WORKDIR /data

# Testing layer
FROM app as test

# Verify installation by checking version and running test
RUN spades.py --version && spades.py --help

# Run the SPAdes test
RUN spades.py --test
