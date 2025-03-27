# Define version
VERSION := latest

# Docker image name
DOCKER_IMAGE := multiqc/multiqc:latest

# Apptainer image name
APPTAINER_IMAGE := multiqc_$(VERSION).sif

# Default paths for input/output
INPUT_DIR := test/in/data
OUTPUT_DIR := test/out
REF_DIR := test/outmultiqc

# List of files to compare in the test
FILES := fastq_screen_plot.txt fastqc_adapter_content_plot.txt fastqc_overrepresented_sequences_plot.txt fastqc_per_base_n_content_plot.txt \
         fastqc_per_base_sequence_quality_plot.txt fastqc_per_sequence_gc_content_plot_Counts.txt fastqc_per_sequence_gc_content_plot_Percentages.txt \
         fastqc_per_sequence_quality_scores_plot.txt fastqc_sequence_counts_plot.txt fastqc_sequence_duplication_levels_plot.txt \
         fastqc_top_overrepresented_sequences_table.txt fastqc-status-check-heatmap.txt gatk_varianteval_variant_plot.txt \
         gatk_compare_overlap.txt multiqc_citations.txt multiqc_fastq_screen.txt multiqc_fastqc.txt multiqc_gatk_varianteval.txt multiqc_general_stats.txt \
         multiqc_picard_dups.txt multiqc_qualimap_bamqc_genome_results.txt multiqc_snpeff.txt multiqc_software_versions.txt multiqc_sources.txt \
         picard_deduplication.txt picard_MarkIlluminaAdapters_histogram.txt picard_MeanQualityByCycle_histogram.txt picard_QualityScoreDistribution_histogram.txt qualimap_coverage_histogram.txt \
         qualimap_gc_content.txt qualimap_genome_fraction.txt qualimap_insert_size.txt snpeff_effects.txt snpeff_qualities.txt \
         snpeff_variant_effects_class.txt snpeff_variant_effects_impact.txt snpeff_variant_effects_region.txt

# Pull the Docker image 
pull:
	@docker pull $(DOCKER_IMAGE)

# Run MultiQC in Docker
run:
	docker run -it --rm \
		-v "$(PWD)/$(INPUT_DIR)":/data \
		-v "$(PWD)/$(OUTPUT_DIR)":/output \
		$(DOCKER_IMAGE) multiqc -c config.yaml /data -o /output

# Build Apptainer image from Docker
build_apptainer:
	@singularity build $(APPTAINER_IMAGE) docker-daemon://$(DOCKER_IMAGE)

# Run MultiQC using Apptainer
run_apptainer:
	@python3 docker_tag.py
	apptainer run $(APPTAINER_IMAGE) multiqc $(ARGS) $(INPUT_DIR) -o $(OUTPUT_DIR)

# Test the Docker and Apptainer outputs
.PHONY: test clean

SCRIPT = test.py

FILES_1 = $(wildcard $(OUTPUT_DIR)/multiqc_data/*.txt)
FILES_2 = $(wildcard $(REF_DIR)/multiqc_data/*.txt)

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

clean:
	@echo "Cleaning temporary files..."
	rm -rf $(OUTPUT_DIR) $(REF_DIR)
