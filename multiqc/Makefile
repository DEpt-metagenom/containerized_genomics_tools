# Define version
VERSION := v1.25.1

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:$(VERSION)

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := whole_genom_seq/data
OUTPUT_DIR := test/output/multiqc_data
REF_DIR := whole_genom_seq/ref/multiqc_data

.PHONY: pull run build_apptainer run_apptainer test

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
	apptainer pull $(APPTAINER_IMAGE) docker://$(DOCKER_IMAGE)

# Run MultiQC using Apptainer
run_apptainer:
	@python3 docker_tag.py
	apptainer run $(APPTAINER_IMAGE) multiqc $(ARGS)

# Test the Docker and Apptainer outputs
test: 
	@echo "Running MultiQC tests..."
	# Run tests for each file and compare using Python script
	@set -e; \
	for file in `ls multiqc_data/*.txt | cut -f2-2 -d/`; do \
		echo "Comparing $(OUTPUT_DIR)/$$file with $(REF_DIR)/$$file..."; \
		python test.py $(OUTPUT_DIR)/$$file $(REF_DIR)/$$file || (echo "Error: $(OUTPUT_DIR)/$$file differs from $(REF_DIR)/$$file" && exit 1); \
	done ;
	@echo "All tests passed!"
