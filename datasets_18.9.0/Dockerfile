# Use the official Miniconda3 image as base
FROM continuumio/miniconda3:latest

# Set timezone and install mamba, ncbi-datasets-cli
RUN TZ=Europe/Budapest \
    && ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime \
    && echo $TZ > /etc/timezone \
    && conda install -y -c conda-forge mamba \
    && mamba install -y -c bioconda -c conda-forge ncbi-datasets-cli=18.9.0 unzip

# Set environment variables
ENV LC_ALL=C
ENV PATH="/opt/conda/bin:$PATH"

# Labels
LABEL Author="Your Name"
LABEL Version="devel"
LABEL Description="NCBI datasets CLI 18.9.0 installed with mamba"

# Test command
CMD ["datasets", "version"]
