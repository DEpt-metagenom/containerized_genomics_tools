# Use the official Ubuntu base image
FROM ubuntu:20.04

# Install required packages
RUN apt-get update && apt-get install -y \
    procps \
    wget \
    bzip2 \
    build-essential \
    libssl-dev \
    libffi-dev \
    build-essential \
    git \
    make \
    parallel \
    && apt-get clean

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -b -p /opt/miniconda && \
    rm /tmp/miniconda.sh

# Add Conda to PATH
ENV PATH=/opt/miniconda/bin:$PATH

# Initialize Conda
RUN /opt/miniconda/bin/conda init

# Configure conda channels
RUN /opt/miniconda/bin/conda config --add channels bioconda && \
    /opt/miniconda/bin/conda config --add channels conda-forge

# Create bedtools environment to install dependencies and bedtools
RUN /opt/miniconda/bin/conda create --name bedtools python=3.5 -y && \
    /opt/miniconda/bin/conda run -n bedtools /opt/miniconda/bin/conda install bioconda::bedtools -y && \
    /opt/miniconda/bin/conda clean -a -y

# Add bedtools to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Set environment variables to activate the bedtools environment by default
SHELL ["/bin/bash", "-c"]
RUN echo 'source /opt/miniconda/bin/activate bedtools' >> ~/.bashrc

# Activate the bedtools environment
ENV CONDA_DEFAULT_ENV=bedtools
ENV PATH=/opt/miniconda/envs/bedtools/bin:$PATH

# Verify installation
RUN bedtools -version && ps --version