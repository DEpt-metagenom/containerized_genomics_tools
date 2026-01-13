FROM condaforge/mambaforge:23.11.0-0

# System deps for Nextflow (procps) and cleaning
RUN apt-get update && \
    apt-get install -y --no-install-recommends procps && \
    rm -rf /var/lib/apt/lists/*

# Copy ToxCodAn-Genome repo into container
WORKDIR /opt/ToxCodAn-Genome
COPY . /opt/ToxCodAn-Genome

# Install dependencies via mamba and prepare PATH + databases
RUN mamba install -y -c conda-forge -c bioconda \
        python=3.10 \
        biopython \
        pandas \
        blast \
        exonerate \
        miniprot \
        gffread \
        hisat2 \
        samtools \
        stringtie \
        trinity \
        spades \
    && mamba clean -afy \
    && chmod +x /opt/ToxCodAn-Genome/bin/* || true \
    && ln -sf /opt/ToxCodAn-Genome/bin/toxcodan-genome.py /usr/local/bin/toxcodan-genome.py \
    && mkdir -p /Databases \
    && cp -r /opt/ToxCodAn-Genome/Databases/* /Databases/ 2>/dev/null || true

# Environment for tool & databases
ENV PATH=/opt/ToxCodAn-Genome/bin:/usr/local/bin:/opt/conda/bin:${PATH}
ENV TOXCODAN_DB=/Databases

# Default command (Nextflow will override with its own)
CMD ["toxcodan-genome.py", "--help"]