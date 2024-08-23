# docker-fastqc

The content of this directory was copied from https://github.com/FredHutch/docker-fastqc

Docker image running FASTQC

[![Docker Repository on Quay](https://quay.io/repository/fhcrc-microbiome/fastqc/status "Docker Repository on Quay")](https://quay.io/repository/fhcrc-microbiome/fastqc)

Image contains FastQC as well as a wrapper script to make it easy to run on files in AWS S3

### Wrapper script

`run_fastqc.sh`

Executable script is in the PATH

Arguments are <INPUT_FASTQ> and <OUTPUT>

<OUTPUT> can be a file or a folder on S3

The output file is in ZIP format.

Example:

```
run_fastqc.sh s3://bucket-name/folder1/reads/file.fastq.gz s3://bucket-name/folder1/fastqc/file.fastqc.zip
```
