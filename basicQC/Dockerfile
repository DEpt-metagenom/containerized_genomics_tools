# STAGE 1: BUILDER
FROM debian:bullseye-slim AS builder

ARG DEBIAN_FRONTEND="noninteractive"
WORKDIR /app

# Install build-time dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        bzip2 \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Download and install Micromamba
RUN ARCH=$(uname -m | sed 's/x86_64/linux-64/;s/aarch64/linux-aarch64/') && \
    wget -qO- "https://micro.mamba.pm/api/micromamba/${ARCH}/latest" | \
    tar -xj -C /usr/local bin/micromamba && \
    chmod +x /usr/local/bin/micromamba

# Set environment variables
ENV MAMBA_ROOT_PREFIX=/opt/conda
ENV PATH=/opt/conda/envs/basicqc/bin:/usr/local/bin:$PATH

SHELL ["/bin/bash", "-c"]

# Create environment with all packages
RUN micromamba create -n basicqc -y \
        -c conda-forge \
        -c bioconda \
        python=3.9 \
        busco=5.6.1 \
        quast=5.3.0 \
        scikit-learn=1.6.1 \
        numpy=2.0.2 \
        pandas=2.3.1 && \
    micromamba clean -afy


# STAGE 2: RUNTIME
FROM debian:bullseye-slim

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

WORKDIR /app

# Install ONLY runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        procps \
        libgomp1 \
        libgfortran5 \
        perl \
        && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the conda environment from builder
COPY --from=builder /opt/conda/envs/basicqc /opt/conda/envs/basicqc

# Set up environment
ENV PATH=/opt/conda/envs/basicqc/bin:$PATH
ENV CONDA_DEFAULT_ENV=basicqc

# Copy and setup your script
COPY scaler.py /usr/local/bin/scaler.py
RUN chmod +x /usr/local/bin/scaler.py

# Verify installations
RUN quast --help && busco --help && scaler.py --help

WORKDIR /data

CMD ["bash"]