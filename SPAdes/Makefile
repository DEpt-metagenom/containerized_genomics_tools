# Variables
VERSION ?= 4.0.0
TOOL ?= spades
DOCKER_USER ?= deptmetagenom
DOCKER_IMAGE = $(DOCKER_USER)/$(TOOL):$(VERSION)
DOCKER_LATEST = $(DOCKER_USER)/$(TOOL):latest
SIF_FILE = $(TOOL)_$(VERSION).sif
APPTAINER_DEF = Apptainer.def
REFERENCE_OUTPUT = reference/scaffolds.fasta  # Path to the reference output file

.PHONY: pull build push build_apptainer test

# Pull the image from Docker Hub
pull:
        docker pull $(DOCKER_LATEST)

# Build the Docker image using a specified version
build:
        @echo "Building Docker image for $(TOOL) version $(VERSION)..."
        docker build --build-arg SPADES_VER=$(VERSION) -t $(TOOL):$(VERSION) -f ./Dockerfile .

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
        apptainer build $(SIF_FILE) $(APPTAINER_DEF)

# Run test using SPAdes tool and compare output
test:
        @echo "Running SPAdes test with $(TOOL) version $(VERSION)..."
        # Ensure output directory exists
        mkdir -p output/
        # Run SPAdes on the specified test files
        docker run --rm -v $(PWD)/test/input:/input -v $(PWD)/output:/output $(DOCKER_IMAGE) \
                -c /input/ecoli_1K_1.fq.gz -p /input/ecoli_1K_2.fq.gz -o /output/
        # Compare output scaffold file to reference scaffold file
        @echo "Comparing generated scaffold file with reference output..."
        diff output/scaffolds.fasta reference/scaffolds.fasta \
                && echo "Test passed: Outputs are identical." \
                || (echo "Test failed: Outputs do not match." && exit 1)
