FROM mambaorg/micromamba:1.5.8

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        procps \
    && rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER

# Install Metax and the MA aligner via the Conda/Mamba route described in the project README.
RUN micromamba install -y -n base \
    -c conda-forge \
    -c bioconda \
    -c zldeng \
    metax==0.9.23 ma=1.1.4 && \
    micromamba clean --all --yes

ENV PATH=/opt/conda/bin:/opt/conda/envs/base/bin:$PATH

WORKDIR /data
ENTRYPOINT ["metax"]
CMD ["--help"]
