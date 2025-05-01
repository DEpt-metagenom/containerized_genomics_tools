# Define version
VERSION := v1.28
REF_VERSION := v1.28

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:$(VERSION)

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

#config file name
CONFIG_NAME = config.yaml

# Default paths for input/output
INPUT_DIR := test/in/data
OUTPUT_DIR := test/out
REF_DIR := test/ref
SCRIPT = test.py
FILES_1 = $(wildcard $(OUTPUT_DIR)/multiqc_data/*.txt)
FILES_2 = $(wildcard $(REF_DIR)/multiqc_data/*.txt)

.PHONY: pull run build_apptainer run_apptainer test generate_test_ref test_apptainer test_docker

# Pull the Docker image 
pull:
	@docker pull $(DOCKER_IMAGE)

check_version:
	@python3 check_makefile_version.py

# Run MultiQC in Docker
run: check_docker_version
	chmod a+w test/out
	docker run --rm \
  		-v $(PWD)/$(INPUT_DIR):/data \
  		-v $(PWD)/$(OUTPUT_DIR):/output \
  		-v $(PWD)/$(CONFIG_NAME):/config.yaml \
		--user $(UID):$(GID) \
  		$(DOCKER_IMAGE) multiqc -c /config.yaml /data -o /out

# Build Apptainer image from Docker
build_apptainer:
	apptainer pull $(APPTAINER_IMAGE) docker://$(DOCKER_IMAGE)

# Run MultiQC using Apptainer
run_apptainer: check_version
	apptainer run $(APPTAINER_IMAGE) multiqc $(ARGS) $(INPUT_DIR) -o $(OUTPUT_DIR)

generate_test_ref:
	mkdir $(REF_DIR)_$(REF_VERSION)
	@echo "Creating and activating virtual environment..."
	python3 -m venv .venv
	. .venv/bin/activate 
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install git+https://github.com/MultiQC/MultiQC.git@$(REF_VERSION)
	.venv/bin/multiqc -c ${CONFIG_NAME} $(PWD)/$(INPUT_DIR) -o $(PWD)/$(REF_DIR)_$(REF_VERSION)
	@echo "Removing virtual environment..."
	deactivate
	rm -rf .venv

# original test
test: test_docker clean test_apptainer clean

test_apptainer:
	@echo "Running MultiQC with Apptainer..."
	mkdir -p $(OUTPUT_DIR)
	make run_apptainer ARGS="-c ${CONFIG_NAME}"

	@echo "Generating reference output with baseline MultiQC (venv)..."
	.venv/bin/multiqc -c config.yaml $(INPUT_DIR) -o $(REF_DIR)

	@echo "Comparing Apptainer output with reference..."
	@all_success=true; \
	for file1 in $(FILES_1); do \
		file2="$(REF_DIR)/multiqc_data/$$(basename $$file1)"; \
		if [ -f "$$file2" ]; then \
			echo "Comparing $$file1 with $$file2..."; \
			if python3 $(SCRIPT) "$$file1" "$$file2"; then \
				echo "PASS: $$file1"; \
			else \
				echo "FAIL: $$file1"; \
				all_success=false; \
			fi; \
		else \
			echo "Reference file $$file2 not found!"; \
			all_success=false; \
		fi; \
	done; \
	if [ "$$all_success" = true ]; then \
		echo "All Apptainer tests passed."; \
	else \
		echo "Some Apptainer tests failed."; \
	fi
	@$(MAKE) clean


test_docker:
	@echo "Running MultiQC with Docker..."
	chmod a+w test/out
	mkdir -p $(OUTPUT_DIR)
	make run

	@echo "Generating reference output with baseline MultiQC (venv)..."
	.venv/bin/multiqc -c config.yaml $(INPUT_DIR) -o $(REF_DIR)

	@echo "Comparing Docker output with reference..."
	@all_success=true; \
	for file1 in $(FILES_1); do \
		file2="$(REF_DIR)/multiqc_data/$$(basename $$file1)"; \
		if [ -f "$$file2" ]; then \
			echo "Comparing $$file1 with $$file2..."; \
			if python3 $(SCRIPT) "$$file1" "$$file2"; then \
				echo "PASS: $$file1"; \
			else \
				echo "FAIL: $$file1"; \
				all_success=false; \
			fi; \
		else \
			echo "Reference file $$file2 not found!"; \
			all_success=false; \
		fi; \
	done; \
	if [ "$$all_success" = true ]; then \
		echo "All Docker tests passed."; \
	else \
		echo "Some Docker tests failed."; \
	fi
	@$(MAKE) clean

clean:
	@echo "Cleaning output and reference directories..."
	rm -rf $(OUTPUT_DIR)/*