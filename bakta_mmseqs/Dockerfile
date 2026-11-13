FROM mambaorg/micromamba:2-debian13-slim

ARG BAKTA_REPOSITORY=https://github.com/DEpt-metagenom/bakta.git
ARG BAKTA_REF=mmseqs_search

USER root

RUN apt-get update && \
    apt-get install --yes --no-install-recommends git procps && \
    if git ls-remote --exit-code --heads "${BAKTA_REPOSITORY}" "${BAKTA_REF}" >/dev/null 2>&1; then \
        git clone --depth 1 --branch "${BAKTA_REF}" "${BAKTA_REPOSITORY}" /opt/bakta; \
    else \
        git clone --depth 1 --branch main "${BAKTA_REPOSITORY}" /opt/bakta; \
    fi && \
    rm -rf /var/lib/apt/lists/*

RUN if grep -q '^  - mmseqs2' /opt/bakta/environment.yml; then \
        sed -i 's/^  - mmseqs2.*/  - mmseqs2=18.8cc5c/' /opt/bakta/environment.yml; \
    else \
        sed -i '/^dependencies:/a\  - mmseqs2=18.8cc5c' /opt/bakta/environment.yml; \
    fi && \
    micromamba create --yes --name bakta --file /opt/bakta/environment.yml && \
    micromamba install --yes --name bakta pip && \
    micromamba run --name bakta python -m pip install --no-cache-dir --no-deps /opt/bakta/ && \
    micromamba clean --all --force-pkgs-dirs --yes

ENV PATH=/opt/conda/envs/bakta/bin:/opt/conda/bin:$PATH \
    CONDA_PREFIX=/opt/conda/envs/bakta \
    MAMBA_ROOT_PREFIX=/opt/conda \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    MPLCONFIGDIR=/tmp/matplotlib

ENTRYPOINT ["bakta"]
