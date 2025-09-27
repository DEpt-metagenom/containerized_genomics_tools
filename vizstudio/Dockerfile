FROM rocker/rstudio:4.5.1

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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Install CRAN packages
RUN R -e "install.packages(c( \
  'devtools', 'rmarkdown', 'stats', 'tidyr', 'dplyr', 'DT', 'parallel', 'foreach', 'doParallel', 'doSNOW', \
  'ape', 'phytools', 'vegan', 'psych', 'knitr', 'kableExtra', \
  'ggplot2', 'ggpubr', 'ggforce', 'ggfortify', 'ggExtra', 'ggvenn', 'ggcorrplot', 'ggrepel', 'GGally', \
  'patchwork', 'ComplexUpset', 'Rtsne', 'umap', 'plotly', \
  'multcomp', 'multcompView', 'emmeans', \
  'survival', 'gggenes', 'gggenomes', 'circlize' \
), repos = 'https://cloud.r-project.org')"

## Install Github packages
RUN R -e "devtools::install_github('omarwagih/ggseqlogo')" \
    && R -e "devtools::install_github('vragh/seqvisr', build_manual = TRUE, build_vignettes = TRUE)" \
    && R -e "devtools::install_github('AlsammanAlsamman/alignstatplot')"

RUN R -e "install.packages('BiocManager')"

RUN R -e "BiocManager::install('DESeq2')"

RUN R -e "devtools::install_github('haleyjeppson/ggmosaic')"

RUN R -e "devtools::install_github('ricardo-bion/ggradar', dependencies = TRUE)"

RUN R -e "BiocManager::install('ComplexHeatmap')"

RUN R -e "install.packages('survminer')"

RUN R -e "BiocManager::install('ggmsa')"

## Expose RStudio Server port
EXPOSE 8787

## Optionally, set a default password for quick testing (change in production!)
ENV USER=rstudio
ENV PASSWORD=rstudio

## RStudio Server starts on launch (from rocker/rstudio base image)
