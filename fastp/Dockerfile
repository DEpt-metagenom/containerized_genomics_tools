# Dockerfile borrowed from: https://github.com/maol-corteva/fastp
# Modified slightly to use alpine:3.14 as base image
############# 
# Dockerfile to build container image for fastp : a bionformatics NGS QC/adapter-trim  tool
# See Docs and Source code at:  https://github.com/OpenGene/fastp
# Example unix cmdline and parameters:
#      fastp -i raw.fq -o ./clean.fq  -h "<samplename>-fastp_report" -w12 -e 25 -l 40 -y -5 -3 -W4 -M20  \ 
#                --overrepresentation_analysis -P 100 --dont_eval_duplication -x 
# Build Image with (and specify tagged version):
#    docker build --build-arg FP_VERSION=0.23.4  -t fastp:0.23.4  -f ./Dockerfile.fastp .
#
# OR to change the build user id to run as yourself, do this:
#    export myUID=$(id -u) ; export myGID=$(id -g)     # See below for details setting the user
#    docker build --build-arg USER=$myUID:$myGID  FP_VERSION=0.23.4 -t fastp:0.23.4  -f ./Dockerfile.fastp .
# Run in iteractive mode like:
#    docker run -it --rm --network="host" --cpus=2 -m 64000m -v ${PWD}:${PWD} -w ${PWD}  --entrypoint /bin/ash   my_image  
#    ... where "my_image" is the full length image name (i.e: fastp:latest) or the specific "IMAGE ID" in your docker setup (docker image ls)
# OR run as default and it will use the internal entrypoint: 
#    docker run -it --rm --network="host" -v ${PWD}:${PWD} -w ${PWD}  my_image  --flags
#    Here is a full example with flags, running within the Docker:
#     /app/fastp -i testsample-pairsR1.fq.gz -I testsample-pairsR2.fq.gz -R testsample_fastP -h testsample.fastp_report.html 
#      --thread 12 --detect_adapter_for_pe --dedup --dup_calc_accuracy 4 -e 25 -l 35 --trim_poly_g --trim_poly_x -p -P 100
#############

# FROM scratch
FROM alpine:3.14
LABEL org.opencontainers.image.authors="mauricio.larota@corteva.com"

ARG DEBIAN_FRONTEND="noninteractive"
ARG TZ="UTC"
ENV TZ="${TZ}"

# Update the repository sources list
RUN apk update && apk add --no-cache wget

# Verified version of 'fastp' to use.   0.23.4 as of Q3 2023.  Provide as cmdline argument to override. Assumes a Linux 64bit ELF binary
ARG FP_VERSION=0.23.4

# Get the precompiled package version wanted
#  fastp v0.23.4
WORKDIR /app
RUN  wget http://opengene.org/fastp/fastp.${FP_VERSION} \
    && mv fastp.${FP_VERSION} fastp \
    && chmod a+x ./fastp  

# Set run user/group as myUID 2000 myGID 3000 for use in Kubernetes (and avoid running as root)
ARG USER=appuser
ARG USERGROUP=appgroup
ARG myUID=2000
ARG myGID=3000
RUN addgroup -g ${myGID} -S ${USERGROUP} && \
    adduser -u ${myUID} -G ${USERGROUP} -S ${USER}
# USER appuser:appgroup
USER ${myUID}:${myGID}
ENTRYPOINT ["/app/fastp"]