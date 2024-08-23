# Docker and Apptainer image of PlasFlow

This directory contains the Docker (`dockerfile`) and Apptainer definition files (`plasflow.def`) to create the container for PlasFlow, a software that uses neural networks to identify plasmids in bacterial (meta)genomes. The Docker image containing all dependencies is hosted at https://hub.docker.com/r/deptmetagenom/plasflow. The entrypoint is set to `PlasFlow.py`.

## Building the container

The container can be built four ways:

Using Docker:

1. Run `docker pull deptmetagenom/plasflow`, then `docker run --rm plasflow --help` to read the help menu.

2. Clone the repository, navigate to this directory and build the Docker container locally by running `docker build -t plasflow .` `docker run --rm plasflow --help` should display the help menu.

Using Apptainer (formerly Singularity):

3. Run `apptainer pull docker://deptmetagenom/plasflow:latest`. Running `apptainer run plasflow_latest.sif --help` should show the help menu again.

4. Clone the repository, navigate to this directory and build the Docker container locally by running: `sudo apptainer build plasflow.sif plasflow.def`. You need superuser rights for this. PlasFlow can be started by executing `apptainer run plasflow.sif --help`

Apptainer `.sif` containers can be built on any computer and simply copied to another computer. The container should always function in the same way, regardless of whether it was created on the computer on which it is running. Superuser permissions are only required to build the container locally using the `.def` file (i.e. containers can be built from images hosted at DockerHub without superuser privileges). Running the container does not require such privileges. On all servers of the Institute the `.sif` container is linked to `/mnt/containers/plasflow.sif` and is thus ready for use.


#> PARAGRAPHS BELOW ARE COPIED FROM THE [ORIGINAL REPOSITORY OF PLASFLOW](https://github.com/smaegol/PlasFlow)

## Test dataset

Test dataset is located in the `test` folder (file `Citrobacter_freundii_strain_CAV1321_scaffolds.fasta`). It is the SPAdes 3.9.1 assembly of Citrobacter freundii strain CAV1321 genome (NCBI assembly ID: GCA_001022155.1), which contains 1 chromosome and 9 plasmids. In the same folder the results of classification can be found in the form of tsv file (`Citrobacter_freundii_strain_CAV1321_scaffolds.fasta.PlasFlow.tsv`) and fasta files containing identified bins (`Citrobacter_freundii_strain_CAV1321_scaffolds.fasta.PlasFlow.tsv_chromosomes.fasta`, `Citrobacter_freundii_strain_CAV1321_scaffolds.fasta.PlasFlow.tsv_plasmids.fasta` and `Citrobacter_freundii_strain_CAV1321_scaffolds.fasta.PlasFlow.tsv_unclassified.fasta`).

To invoke PlasFlow on the test dataset please copy the `test/Citrobacter_freundii_strain_CAV1321_scaffolds.fasta` file to you current working directory and type:

```
PlasFlow.py --input Citrobacter_freundii_strain_CAV1321_scaffolds.fasta --output test.plasflow_predictions.tsv --threshold 0.7
```
The predictions will be located in the `test.plasflow_predictions.tsv` file and can be compared to results available in the `test/Citrobacter_freundii_strain_CAV1321_scaffolds.fasta.PlasFlow.tsv`.

