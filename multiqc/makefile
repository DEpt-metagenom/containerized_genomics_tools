# Define version
VERSION := latest

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:latest

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := whole_genom_seq/data
OUTPUT_DIR := test/output/multiqc_data
REF_DIR := whole_genom_seq/ref/multiqc_data

# List of files to compare in the test
FILES := fastq_screen_plot.txt fastqc_adapter_content_plot.txt fastqc_overrepresented_sequences_plot.txt fastqc_per_base_n_content_plot.txt \
         fastqc_per_base_sequence_quality_plot.txt fastqc_per_sequence_gc_content_plot_Counts.txt fastqc_per_sequence_gc_content_plot_Percentages.txt \
         fastqc_per_sequence_quality_scores_plot.txt fastqc_sequence_counts_plot.txt fastqc_sequence_duplication_levels_plot.txt \
         fastqc_top_overrepresented_sequences_table.txt fastqc-status-check-heatmap.txt gatk_varianteval_variant_plot.txt \
         gatk_compare_overlap.txt multiqc_citations.txt multiqc_fastq_screen.txt multiqc_fastqc.txt multiqc_gatk_varianteval.txt multiqc_general_stats.txt \
         multiqc_picard_dups.txt multiqc_qualimap_bamqc_genome_results.txt multiqc_snpeff.txt multiqc_software_versions.txt multiqc_sources.txt \
         picard_deduplication.txt picard_histogram_1.txt picard_histogram_2.txt picard_histogram.txt qualimap_coverage_histogram.txt \
         qualimap_gc_content.txt qualimap_genome_fraction.txt qualimap_insert_size.txt snpeff_effects.txt snpeff_qualities.txt \
         snpeff_variant_effects_class.txt snpeff_variant_effects_impact.txt snpeff_variant_effects_region.txt

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

# Run MultiQC using Apptainer
run_apptainer:
	@python3 docker_tag.py
	apptainer run $(APPTAINER_IMAGE) multiqc $(ARGS)

# Test the Docker and Apptainer outputs
test: 
	@echo "Running MultiQC tests..."
	# Run tests for each file and compare using Python script
	@set -e; \
	for file in $(FILES); do \
		echo "Comparing $(OUTPUT_DIR)/$$file with $(REF_DIR)/$$file..."; \
		python test.py $(OUTPUT_DIR)/$$file $(REF_DIR)/$$file || (echo "Error: $(OUTPUT_DIR)/$$file differs from $(REF_DIR)/$$file" && exit 1); \
	done ;
	@echo "All tests passed!"
