#!/bin/bash

# Make sure the output key is reasonable
echo Output location is $2
aws s3 ls $2

# Download input file from S3
echo Downloading input file from S3
echo Provided input path is $1

aws s3 cp "$1" /share

# Get the filename
filename=${1##*/}
echo Filename is $filename

# Make sure the file exists
[[ -s /share/$filename ]]

# Run FastQC
echo Running FastQC
fastqc -f fastq /share/$filename

# Return the output
zip_file=$(find /share -name "*zip")
aws s3 cp "$zip_file" "$2"

# Clean up temp files
echo Removing temporary files
rm /share/$filename $(find /share -name "*zip")

echo Done
