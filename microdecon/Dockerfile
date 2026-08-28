FROM rocker/rstudio:4.5.1

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

WORKDIR /app

## Install system dependencies for R packages
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgit2-dev \
    libfftw3-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    libudunits2-dev \
    libfontconfig1-dev \
    libfreetype6-dev \
    libhdf5-dev \
    libtbb-dev \
    libgdal-dev \
    libproj-dev \
    libglpk-dev \
    libv8-dev \
    libgeos-dev \
    build-essential \
    git \
    make \
    g++ \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libgit2-dev \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN R -e 'install.packages(c("devtools", "remotes"), repos="https://cloud.r-project.org")' \
    && R -e 'devtools::install_github("donaldtmcknight/microDecon")'

RUN R -e 'install.packages(c("dplyr","tidyr","foreach"))'

CMD ["R"]
