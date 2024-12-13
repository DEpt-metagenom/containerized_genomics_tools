# Define version
VERSION := latest

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:latest

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := whole_genom_seq/data
OUTPUT_DIR := test/output

# Pull the Docker image 
pull:
	@docker pull $(DOCKER_IMAGE)

# Run MultiQC in Docker
run:
	docker run -it --rm \
		-v $(PWD)/$(INPUT_DIR):/data \
		-v $(PWD)/$(OUTPUT_DIR):/output \
		$(DOCKER_IMAGE) /data -o /output

# Build Apptainer image from Docker
build_apptainer:
	@singularity build $(APPTAINER_IMAGE) docker-daemon://$(DOCKER_IMAGE)

#Run MultiQC using Apptainer
run_apptainer:
	@python3 docker_tag.py
	apptainer run multiqc_1.25.1.sif multiqc $(ARGS)

# Test the Docker and Apptainer outputs
test: 
	@echo "Running MultiQC tests..."
	# Add your test comparison logic here (diff/grep)

