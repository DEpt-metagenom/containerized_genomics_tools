FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

WORKDIR /app

RUN apt-get update && apt-get install -y wget bash procps pigz && rm -rf /var/lib/apt/lists/*

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

# Creating python environment with minimap2
RUN conda create -n antiCS python=3.9 minimap2=2.28

SHELL ["/bin/bash", "-c"]
ENV CONDA_DEFAULT_ENV=antiCS
ENV PATH=/app/miniconda/envs/antiCS/bin:$PATH

RUN pip install biopython pandas

COPY antiCS.py /usr/local/bin/antiCS.py

RUN chmod +x /usr/local/bin/antiCS.py

RUN pigz --help && minimap2 --help && antiCS.py --help

WORKDIR /data

CMD ["bash"]
