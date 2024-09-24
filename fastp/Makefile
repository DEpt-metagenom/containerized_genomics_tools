# Variables
VERSION ?= 0.23.4
TOOL ?= fastp
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
	mkdir test/out
	chmod a+w test/out

	@echo "Running fastp in Docker on test files: $(TESTFILES)..."
	@set -e; \
	for file in $(TESTFILES); do \
		echo "Processing $$file.fq..."; \
		docker run -it --rm -v $${PWD}:$${PWD} -w $${PWD} $(TOOL):$(VERSION) \
			-i test/in/$$file.fq -o test/out/$$file.fq -h test/out/$$file.html -j test/out/$$file.json; \
		echo "Comparing test/out/$$file.fq with test/ref/$$file.fq..."; \
		diff -q test/out/$$file.fq test/ref/$$file.fq || (echo "Error: test/out/$$file.fq differs from test/ref/$$file.fq" && exit 1); \
		echo "Comparing test/out/$$file.json with test/ref/$$file.json..."; \
		diff -q test/out/$$file.json test/ref/$$file.json || (echo "Error: test/out/$$file.json differs from test/ref/$$file.json" && exit 1); \
		rm -f test/out/* ; \
	done ; \
	TESTFILES="R1 R2"; \
	FIRST=`echo $$TESTFILES | awk '{print $$1}'`; \
	SECOND=`echo $$TESTFILES | awk '{print $$2}'`; \
	echo "Processing $$FIRST.fq and $$SECOND.fq as paired-end input in Docker..."; \
	docker run -it --rm -v $${PWD}:$${PWD} -w $${PWD} $(TOOL):$(VERSION) \
		-i test/in/$$FIRST.fq -I test/in/$$SECOND.fq -o test/out/$${FIRST}p.fq -O test/out/$${SECOND}p.fq \
		-h test/out/$$FIRST$$SECOND.html -j test/out/$$FIRST$$SECOND.json; \
	\
	echo "Comparing test/out/$${FIRST}p.fq with test/ref/$${FIRST}p.fq..."; \
	diff -q test/out/$${FIRST}p.fq test/ref/$${FIRST}p.fq || (echo "Error: test/out/$${FIRST}p.fq differs from test/ref/$${FIRST}p.fq" && exit 1); \
	echo "Comparing test/out/$${SECOND}p.fq with test/ref/$${SECOND}p.fq..."; \
	diff -q test/out/$${SECOND}p.fq test/ref/$${SECOND}p.fq || (echo "Error: test/out/$${SECOND}p.fq differs from test/ref/$${SECOND}p.fq" && exit 1); \
	echo "Comparing test/out/$$FIRST$$SECOND.json with test/ref/$$FIRST$$SECOND.json..."; \
	diff -q test/out/$$FIRST$$SECOND.json test/ref/$$FIRST$$SECOND.json || (echo "Error: test/out/$$FIRST$$SECOND.json differs from test/ref/$$FIRST$$SECOND.json" && exit 1); \
	rm -f test/out/* ;

	@echo "Running fastp in Apptainer on test files: $(TESTFILES)..."
	@set -e; \
	for file in $(TESTFILES); do \
		echo "Processing $$file.fq..."; \
		apptainer run $(SIF_FILE) -i test/in/$$file.fq -o test/out/$$file.fq -h test/out/$$file.html -j test/out/$$file.json; \
		echo "Comparing test/out/$$file.fq with test/ref/$$file.fq..."; \
		diff -q test/out/$$file.fq test/ref/$$file.fq || (echo "Error: test/out/$$file.fq differs from test/ref/$$file.fq" && exit 1); \
		echo "Comparing test/out/$$file.json with test/ref/$$file.json..."; \
		diff -q test/out/$$file.json test/ref/$$file.json || (echo "Error: test/out/$$file.json differs from test/ref/$$file.json" && exit 1); \
		rm -f test/out/* ; \
	done ; \
	TESTFILES="R1 R2"; \
	FIRST=`echo $$TESTFILES | awk '{print $$1}'`; \
	SECOND=`echo $$TESTFILES | awk '{print $$2}'`; \
	echo "Processing $$FIRST.fq and $$SECOND.fq as paired-end input in Apptainer..."; \
	apptainer run $(SIF_FILE) -i test/in/$$FIRST.fq -I test/in/$$SECOND.fq -o test/out/$${FIRST}p.fq -O test/out/$${SECOND}p.fq \
		-h test/out/$$FIRST$$SECOND.html -j test/out/$$FIRST$$SECOND.json; \
	\
	echo "Comparing test/out/$${FIRST}p.fq with test/ref/$${FIRST}p.fq..."; \
	diff -q test/out/$${FIRST}p.fq test/ref/$${FIRST}p.fq || (echo "Error: test/out/$${FIRST}p.fq differs from test/ref/$${FIRST}p.fq" && exit 1); \
	echo "Comparing test/out/$${SECOND}p.fq with test/ref/$${SECOND}p.fq..."; \
	diff -q test/out/$${SECOND}p.fq test/ref/$${SECOND}p.fq || (echo "Error: test/out/$${SECOND}p.fq differs from test/ref/$${SECOND}p.fq" && exit 1); \
	echo "Comparing test/out/$$FIRST$$SECOND.json with test/ref/$$FIRST$$SECOND.json..."; \
	diff -q test/out/$$FIRST$$SECOND.json test/ref/$$FIRST$$SECOND.json || (echo "Error: test/out/$$FIRST$$SECOND.json differs from test/ref/$$FIRST$$SECOND.json" && exit 1); \
	rm -f test/out/* ;

	@echo "All tests passed!"
