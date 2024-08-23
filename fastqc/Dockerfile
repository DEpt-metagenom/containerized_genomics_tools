FROM openjdk:8-jdk-slim
MAINTAINER sminot@fredhutch.org

# Install AWS CLI
RUN apt update && apt install -y groff awscli

# Set the default langage to C
ENV LC_ALL C

# Try to fix something odd
RUN sed -i 's/assistive_technologies/#assistive_technologies/' /etc/java-8-openjdk/accessibility.properties

# Download FastQC
ADD http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.8.zip /usr/local/bin/
RUN cd /usr/local/bin/ && \
    unzip fastqc_v0.11.8.zip && \
    chmod 755 FastQC/fastqc && \
    ln -s $PWD/FastQC/fastqc /usr/local/bin/

# Use /share as the working directory
RUN mkdir /share
WORKDIR /share

# AWS CLI is installed
RUN aws --version

# FastQC is installed
RUN fastqc --version

# Add the wrapper script
ADD run_fastqc.sh /usr/local/bin/
