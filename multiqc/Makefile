# Define version
VERSION := v1.28

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:$(VERSION)

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := test/in/data
OUTPUT_DIR := test/output
REF_DIR := test/ref
SCRIPT = test.py
FILES_1 = $(wildcard $(OUTPUT_DIR)/multiqc_data/*.txt)
FILES_2 = $(wildcard $(REF_DIR)/multiqc_data/*.txt)

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
	apptainer run $(APPTAINER_IMAGE) multiqc $(ARGS) $(INPUT_DIR) -o $(OUTPUT_DIR)

# Test the Docker and Apptainer outputs
test: 
	@echo "Running MultiQC tests in Apptainer..."
	multiqc -c config.yaml $(INPUT_DIR) -o $(REF_DIR)
	make run_apptainer ARGS="-c config.yaml"

	$(FILES_1)
	@echo "Comparing matching files in $(OUTPUT_DIR)/multiqc_data and $(REF_DIR)/multiqc_data..."
	@all_success=true; \
	for file1 in $(FILES_1); do \
		file2=$(REF_DIR)/multiqc_data/$(notdir $$file1); \
		if [ -f $$file2 ]; then \
			echo "Comparing $$file1 and $$file2..."; \
			if python3 $(SCRIPT) $$file1 $$file2; then \
				echo "Successfully compared $$file1 and $$file2"; \
			else \
				echo "Test failed for $$file1 and $$file2"; \
				all_success=false; \
			fi; \
		fi; \
	done; \
	if [ $$all_success = true ]; then \
		echo "All tests were successful!"; \
	else \
		echo "Some comparisons failed."; \
	fi
