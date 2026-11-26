FROM mambaorg/micromamba:2.3.2

USER root

ARG MUMMER_VERSION=4.0.1

ENV DEBIAN_FRONTEND=noninteractive

# Build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        perl \
    && rm -rf /var/lib/apt/lists/*

# Install Python in the micromamba base environment
RUN micromamba install -y -n base \
        -c conda-forge \
        python=3.12 \
    && micromamba clean --all --yes

# Build MUMmer 4
RUN mkdir -p /tmp/mummer /opt/mummer && \
    curl -fsSL \
        "https://github.com/mummer4/mummer/releases/download/v${MUMMER_VERSION}/mummer-${MUMMER_VERSION}.tar.gz" \
        -o /tmp/mummer.tar.gz && \
    tar -xzf /tmp/mummer.tar.gz \
        --strip-components=1 \
        -C /tmp/mummer && \
    cd /tmp/mummer && \
    ./configure --prefix=/opt/mummer && \
    make -j"$(nproc)" && \
    make install && \
    rm -rf /tmp/mummer /tmp/mummer.tar.gz

# Add MUMmer executables to PATH
ENV PATH="/opt/mummer/bin:${PATH}"

# Copy the Quickmerge source checkout
WORKDIR /opt/quickmerge
COPY . /opt/quickmerge/

# Compile Quickmerge
RUN make -C merger -j"$(nproc)" && \
    install -m 755 merger/quickmerge /usr/local/bin/quickmerge && \
    install -m 755 merge_wrapper.py /usr/local/bin/merge_wrapper.py

# Default working directory for input/output files
WORKDIR /work

# Make sure the micromamba base environment is active
ENV MAMBA_DOCKERFILE_ACTIVATE=1

USER mambauser

CMD ["/bin/bash"]
