# Define version
VERSION := 1.25.1

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:latest

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := test/in
OUTPUT_DIR := test/out

# Pull the Docker image 
pull:
	@docker pull $(DOCKER_IMAGE)

# Run MultiQC in Docker
run:
	@docker run -it --rm \
		-v $(PWD)/$(INPUT_DIR):/data \
		-v $(PWD)/$(OUTPUT_DIR):/output \
		$(DOCKER_IMAGE) /data -o /output

# Build Apptainer image from Docker
build_apptainer:
	@singularity build $(APPTAINER_IMAGE) docker-daemon://$(DOCKER_IMAGE)

# Test the Docker and Apptainer outputs
test: 
	@echo "Running MultiQC tests..."
	# Add your test comparison logic here (diff/grep)

