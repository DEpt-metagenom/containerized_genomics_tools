FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

WORKDIR /app

RUN apt-get update && apt-get install -y wget bash procps && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh
RUN bash /tmp/miniconda.sh -b -p /app/miniconda
RUN rm /tmp/miniconda.sh

# Add Conda to PATH
ENV PATH=/app/miniconda/bin:$PATH

# Initialize Conda
RUN conda init

# Accept Anaconda TOS for required channels
RUN conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Configure conda channels
RUN conda config --add channels bioconda && \
    conda config --add channels conda-forge

# Creating environment for BUSCO and Quast
RUN conda create -n basicqc python=3.9 busco=5.6.1 quast=5.3.0 -y

SHELL ["/bin/bash", "-c"]
ENV CONDA_DEFAULT_ENV=basicqc
ENV PATH=/app/miniconda/envs/basicqc/bin:$PATH

RUN pip install scikit-learn numpy pandas

RUN quast --help
RUN busco --help

WORKDIR /data

CMD ["bash"]
