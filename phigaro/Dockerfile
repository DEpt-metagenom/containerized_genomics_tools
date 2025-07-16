FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

WORKDIR /app

RUN apt-get update && apt-get install -y wget bash

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
RUN bash /tmp/miniconda.sh -b -p /app/miniconda
RUN rm /tmp/miniconda.sh

# Add Conda to PATH
ENV PATH=/app/miniconda/bin:$PATH

# Initialize Conda
RUN /app/miniconda/bin/conda init

RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Configure conda channels
RUN /app/miniconda/bin/conda config --add channels bioconda && \
    /app/miniconda/bin/conda config --add channels conda-forge

RUN wget https://raw.githubusercontent.com/bobeobibo/phigaro/refs/heads/master/environment.yml -O /tmp/environment.yml

RUN /app/miniconda/bin/conda env create -f /tmp/environment.yml

# Set environment variables to activate the plasflow environment by default
SHELL ["/bin/bash", "-c"]

# Activate the plasflow environment
ENV CONDA_DEFAULT_ENV=phigaro_env
ENV PATH=/app/miniconda/envs/phigaro_env/bin:$PATH

# The environment is now available for all subsequent RUN/CMD/ENTRYPOINT steps

#RUN phigaro-setup --no-updatedb -f

# config created manually
# pvogs downloaded with phigaro-setup are copied from ./phigaro (ZFS/Databases/phigaro/pvog)
COPY ./phigaro /root/.phigaro
