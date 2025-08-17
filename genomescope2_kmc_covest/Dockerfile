FROM debian:bullseye-slim

MAINTAINER marijadoneva14
MAINTAINER laczkol

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    bash \
    bzip2 \
    python3-pip \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /app/miniconda \
    && rm /tmp/miniconda.sh

ENV PATH=/app/miniconda/bin:$PATH

RUN conda config --add channels defaults \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

RUN conda create -n bio_env genomescope2 kmc -y

RUN pip install covest

SHELL ["/bin/bash", "-c"]
ENV PATH="/app/miniconda/envs/bio_env/bin:$PATH"
ENV CONDA_DEFAULT_ENV="bio_env"

RUN kmc --help 
RUN genomescope2 --help 
RUN sed -i "s/scipy.misc/scipy.special/" /app/miniconda/lib/python3.13/site-packages/covest/models.py
RUN covest --help

WORKDIR /data

CMD ["bash"]