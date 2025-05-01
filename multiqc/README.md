# MultiQC Containerized Workflow

This subdirectory contains the necessary files to build and manage Docker and Apptainer containers for the **MultiQC** tool.

## Usage

### Running MultiQC from the Docker Container

First, pull the Docker container using `make pull`. You need Docker installed and **appropriate permissions** to pull and run the container.


The command below runs the tool and displays its command-line parameters:

```bash
docker run --rm multiqc/multiqc
```
To get the current version of **MultiQC** use following line:
```bash
docker run multiqc/multiqc multiqc --version
```

Alternatively, if you don't have other `multiqc` Docker images on the local machine, tag `multiqc/multiqc` as `multiqc` to save typing

```bash
docker tag multiqc/multiqc multiqc
```

To run **MultiQC** on input files, mount the input directory and output directory on the Docker container using the `-v` switch. Here’s an example command that assumes your input files are in the `test/in/` subdirectory:

```bash
docker run --rm -v "$PWD/test/in:/data" -v "$PWD/test/out:/output" multiqc multiqc /data -o /output
```
where
- **`docker run --rm`**: Creates and runs a container from the image (`multiqc` in this case) and automatically removes it (`--rm`) once it finishes.
- **`-v "$PWD/test/in:/data"`**: Mounts a local directory (`test/in` within the current directory) to the container's `/data` directory. This allows `MultiQC` to access input files.
- **`-v "$PWD/test/out:/output"`**: Mounts another local directory (`test/out`) as `/output` in the container, where `MultiQC` will save the output.
- **`multiqc`**: Specifies the image name to run.
- **`multiqc /data -o /output`**: This is the command executed within the container.

   
This command will use files in `test/in` to create a `multiqc_data` directory and **multiqc_report.html** report in `/test/out`.

**Note**: The container will need write permissions for the mounted directory to write the output. Use the `--user $(id -u):$(id -g)` flag to give the container the same permissions as your current user.

### Running MultiQC from the Apptainer Container

You don't need special permissions to run **MultiQC** from **Apptainer**. Here’s how to run it if you already mounted `/data` and `/output` directories:

```bash
apptainer run multiqc_{VERSION}.sif multiqc /data -o /output
```

## Make commands

### `make pull`
Pulls docker image of MultiQC of specified version from their official DockerHub. If you want to pull the image of different version, use `make pull VERSION=[your desired version]`.

### `make run`
Runs docker image of MultiQC.

### `make build_apptainer`

Creates an Apptainer image by converting the Docker image.

### `make run_apptainer ARGS="{your input}"`
Runs an Apptainer image. As it is being invoked, `apptainer run multiqc_$(VERSION).sif multiqc $(INPUT_DIRECTORY) -o $(OUTPUT_DIRECTORY)` command is used. Specify your flags inside ARGS = "".

Example use: 
``` bash
make run_apptainer ARGS='-c multiqc_config.yaml'
```

### `make generate_test_ref`
This command installs MultiQC tool and generates a reference report in test/ref_$(REF_VERSION) directory. Generate the reference report every time it is needed. You can specify which version report you need by using `REF_VERSION=[your version]`

Example use:
``` bash
make generate_ref_report REF_VERSION=v1.27.1
```

### `make check_docker_version`
Runs a python script that checks if the version of MultiQC in Makefile is the same as the latest version on MultiQC DockerHub.

### `make test`
Runs both docker and apptainer tests comparing the generated reports to the **reference report**. To run it successfully, you need to have both docker and apptainer image installed.

### `make test_apptainer`
Generates a MultiQC report in the test/output folder using apptainer.sif and then compares its contents to the reference report generated earlier.


### `make test_docker`
Generates a MultiQC report in the test/output folder using docker image and then compares its contents to the reference report generated earlier.


### `make clean` 
Removes the contents of test/output folder after testing.
