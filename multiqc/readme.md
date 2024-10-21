# MultiQC Containerized Workflow

This subdirectory contains the necessary files to build and manage Docker and Apptainer containers for the **MultiQC** tool.

## Usage

### Running MultiQC from the Docker Container

1. First, pull the Docker container using `make pull`. You need Docker installed and appropriate permissions to pull and run the container.

2. To check the version or run **MultiQC**, use:
    ```bash
    docker run multiqc/multiqc --version
    ```

3. To run **MultiQC** on input files, mount the input directory and output directory on the Docker container using the `-v` switch. Here’s an example command that assumes your input files are in the `test/in/` subdirectory:

    ```bash
    docker run -it --rm -v $PWD/test/in:/data -v $PWD/test/out:/output multiqc/multiqc /data -o /output
    ```

    This will:
    - Use files in `test/in` as the input
    - Generate the output in `test/out`
   
    **Note**: The container will need write permissions for the mounted directory to write the output. Use the `--user $(id -u):$(id -g)` flag to give the container the same permissions as your current user.

### Running MultiQC from the Apptainer Container

You don't need special permissions to run **MultiQC** from **Apptainer**. Here’s how to run it:

```bash
apptainer run multiqc_1.25.1.sif /data -o /output

