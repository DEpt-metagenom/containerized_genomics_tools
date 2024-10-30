# Variables
VERSION ?= 4.0.0
TOOL ?= SPAdes
DOCKER_USER ?= deptmetagenom
DOCKER_IMAGE = $(DOCKER_USER)/$(TOOL):$(VERSION)
DOCKER_LATEST = $(DOCKER_USER)/$(TOOL):latest
SIF_FILE = $(TOOL)_$(VERSION).sif
APPTAINER_DEF = Apptainer.def
TESTFILES ?= R1 R2  # List of test files without extensions (default: "R1 R2")

.PHONY: pull build push build_apptainer test

# Pull the image from Docker Hub
pull:
	docker pull $(DOCKER_LATEST)

# Build the Docker image using a specified version
build:
	@echo "Building Docker image for $(TOOL) version $(VERSION)..."
	docker build --build-arg FP_VERSION=$(VERSION) -t $(TOOL):$(VERSION) -f ./Dockerfile .

# Push the image to Docker Hub
push: build
	@echo "Logging in to Docker Hub..."
	docker login
	docker tag $(TOOL):$(VERSION) $(DOCKER_IMAGE)
	docker tag $(TOOL):$(VERSION) $(DOCKER_LATEST)
	docker push $(DOCKER_IMAGE)
	docker push $(DOCKER_LATEST)

# Build the Apptainer image
build_apptainer: push
	@echo "Building Apptainer image from Docker image..."
	apptainer pull $(SIF_FILE) docker://$(DOCKER_IMAGE)

# Test the Docker container with multiple test files
test:
	mkdir test/output
	chmod a+w test/output

	@echo "Running SPAdes tests with $(TOOL) version $(VERSION)..."
	# Run SPAdes for each test file
	docker run --rm -v $(PWD)/data:/data -v $(PWD)/output:/output $(DOCKER_IMAGE) \
		-c /data/$(TESTFILES)_1.fastq -p /data/$(TESTFILES)_2.fastq -o /output/
	# Compare output to reference output
	@echo "Comparing generated output with reference output..."
	diff -r output/ $(REFERENCE_OUTPUT) || (echo "Test failed: Outputs do not match." && exit 1)
	@echo "Test passed: Outputs match the reference."
