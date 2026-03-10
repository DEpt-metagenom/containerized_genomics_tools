#!/usr/bin/env python

import argparse
import os
import gzip
import subprocess
import shutil
from Bio import SeqIO
import pandas as pd
from pandas.errors import EmptyDataError
import sys

def write_DNA_CS():
    """
    seq from:
    DNA_CS:
    https://raw.githubusercontent.com/wdecoster/nanolyse/refs/heads/master/reference/DNA_CS.fasta
    alternative: https://assets.ctfassets.net/hkzaxo8a05x5/2IX56YmF5ug0kAQYoAg2Uk/159523e326b1b791e3b842c4791420a6/DNA_CS.txt
    whole lambda phage genome:
    https://github.com/wdecoster/nanolyse/raw/refs/heads/master/reference/lambda.fasta.gz

    """
    id = "DNA_CS"
    seq = ("GCCATCAGATTGTGTTTGTTAGTCGCTTTTTTTTTTTGGAATTTTTTTTTTGGAATTTTTTTTTTGCGCTAACAACCTCCTGCCGTTTTGCCCGTGCATATCGGTCACGAACAAATCTGATTACTAAACACAGTAGCCTGGATTTGTTCTATCAGTAATCGACCTTATTCCTAATTAAATAGAGCAAATCCCCTTATTGGGGGTAAGACATGAAGATGCCAGAAAAACATGACCTGTTGGCCGCCATTCTCGCGGCAAAGGAACAAGGCATCGGGGCAATCCTTGCGTTTGCAATGGCGTACCTTCGCGGCAGATATAATGGCGGTGCGTTTACAAAAACAGTAATCGACGCAACGATGTGCGCCATTATCGCCTAGTTCATTCGTGACCTTCTCGACTTCGCCGGACTAAGTAGCAATCTCGCTTATATAACGAGCGTGTTTATCGGCTACATCGGTACTGACTCGATTGGTTCGCTTATCAAACGCTTCGCTGCTAAAAAAGCCGGAGTAGAAGATGGTAGAAATCAATAATCAACGTAAGGCGTTCCTCGATATGCTGGCGTGGTCGGAGGGAACTGATAACGGACGTCAGAAAACCAGAAATCATGGTTATGACGTCATTGTAGGCGGAGAGCTATTTACTGATTACTCCGATCACCCTCGCAAACTTGTCACGCTAAACCCAAAACTCAAATCAACAGGCGCCGGACGCTACCAGCTTCTTTCCCGTTGGTGGGATGCCTACCGCAAGCAGCTTGGCCTGAAAGACTTCTCTCCGAAAAGTCAGGACGCTGTGGCATTGCAGCAGATTAAGGAGCGTGGCGCTTTACCTATGATTGATCGTGGTGATATCCGTCAGGCAATCGACCGTTGCAGCAATATCTGGGCTTCACTGCCGGGCGCTGGTTATGGTCAGTTCGAGCATAAGGCTGACAGCCTGATTGCAAAATTCAAAGAAGCGGGCGGAACGGTCAGAGAGATTGATGTATGAGCAGAGTCACCGCGATTATCTCCGCTCTGGTTATCTGCATCATCGTCTGCCTGTCATGGGCTGTTAATCATTACCGTGATAACGCCATTACCTACAAAGCCCAGCGCGACAAAAATGCCAGAGAACTGAAGCTGGCGAACGCGGCAATTACTGACATGCAGATGCGTCAGCGTGATGTTGCTGCGCTCGATGCAAAATACACGAAGGAGTTAGCTGATGCTAAAGCTGAAAATGATGCTCTGCGTGATGATGTTGCCGCTGGTCGTCGTCGGTTGCACATCAAAGCAGTCTGTCAGTCAGTGCGTGAAGCCACCACCGCCTCCGGCGTGGATAATGCAGCCTCCCCCCGACTGGCAGACACCGCTGAACGGGATTATTTCACCCTCAGAGAGAGGCTGATCACTATGCAAAAACAACTGGAAGGAACCCAGAAGTATATTAATGAGCAGTGCAGATAGAGTTGCCCATATCGATGGGCAACTCATGCAATTATTGTGAGCAATACACACGCGCTTCCAGCGGAGTATAAATGCCTAAAGTAATAAAACCGAGCAATCCATTTACGAATGTTTGCTGGGTTTCTGTTTTAACAACATTTTCTGCGCCGCCACAAATTTTGGCTGCATCGACAGTTTTCTTCTGCCCAATTCCAGAAACGAAGAAATGATGGGTGATGGTTTCCTTTGGTGCTACTGCTGCCGGTTTGTTTTGAACAGTAAACGTCTGTTGAGCACATCCTGTAATAAGCAGGGCCAGCGCAGTAGCGAGTAGCATTTTTTTCATGGTGTTATTCCCGATGCTTTTTGAAGTTCGCAGAATCGTATGTGTAGAAAATTAAACAAACCCTAAACAATGAGTTGAAATTTCATATTGTTAATATTTATTAATGTATGTCAGGTGCGATGAATCGTCATTGTATTCCCGGATTAACTATGTCCACAGCCCTGACGGGGAACTTCTCTGCGGGAGTGTCCGGGAATAATTAAAACGATGCACACAGGGTTTAGCGCGTACACGTATTGCATTATGCCAACGCCCCGGTGCTGACACGGAAGAAACCGGACGTTATGATTTAGCGTGGAAAGATTTGTGTAGTGTTCTGAATGCTCTCAGTAAATAGTAATGAATTATCAAAGGTATAGTAATATCTTTTATGTTCATGGATATTTGTAACCCATCGGAAAACTCCTGCTTTAGCAAGATTTTCCCTGTATTGCTGAAATGTGATTTCTCTTGATTTCAACCTATCATAGGACGTTTCTATAAGATGCGTGTTTCTTGAGAATTTAACATTTACAACCTTTTTAAGTCCTTTTATTAACACGGTGTTATCGTTTTCTAACACGATGTGAATATTATCTGTGGCTAGATAGTAAATATAATGTGAGACGTTGTGACGTTTTAGTTCAGAATAAAACAATTCACAGTCTAAATCTTTTCGCACTTGATCGAATATTTCTTTAAAAATGGCAACCTGAGCCATTGGTAAAACCTTCCATGTGATACGAGGGCGCGTAGTTTGCATTATCGTTTTTATCGTTTCAATCTGGTCTGACCTCCTTGTGTTTTGTTGATGATTTATGTCAAATATTAGGAATGTTTTCACTTAATAGTATTGGTTGCGTAACAAAGTGCGGTCCTGCTGGCATTCTGGAGGGAAATACAACCGACAGATGTATGTAAGGCCAACGTGCTCAAATCTTCATACAGAAAGATTTGAAGTAATATTTTAACCGCTAGATGAAGAGCAAGCGCATGGAGCGACAAAATGAATAAAGAACAATCTGCTGATGATCCCTCCGTGGATCTGATTCGTGTAAAAAATATGCTTAATAGCACCATTTCTATGAGTTACCCTGATGTTGTAATTGCATGTATAGAACATAAGGTGTCTCTGGAAGCATTCAGAGCAATTGAGGCAGCGTTGGTGAAGCACGATAATAATATGAAGGATTATTCCCTGGTGGTTGACTGATCACCATAACTGCTAATCATTCAAACTATTTAGTCTGTGACAGAGCCAACACGCAGTCTGTCACTGTCAGGAAAGTGGTAAAACTGCAACTCAATTACTGCAATGCCCTCGTAATTAAGTGAATTTACAATATCGTCCTGTTCGGAGGGAAGAACGCGGGATGTTCATTCTTCATCACTTTTAATTGATGTATATGCTCTCTTTTCTGACGTTAGTCTCCGACGGCAGGCTTCAATGACCCAGGCTGAGAAATTCCCGGACCCTTTTTGCTCAAGAGCGATGTTAATTTGTTCAATCATTTGGTTAGGAAAGCGGATGTTGCGGGTTGTTGTTCTGCGGGTTCTGTTCTTCGTTGACATGAGGTTGCCCCGTATTCAGTGTCGCTGATTTGTATTGTCTGAAGTTGTTTTTACGTTAAGTTGATGCAGATCAATTAATACGATACCTGCGTCATAATTGATTATTTGACGTGGTTTGATGGCCTCCACGCACGTTGTGATATGTAGATGATAATCATTATCACTTTACGGGTCCTTTCCGGTGAAAAAAAAGGTACCAAAAAAAACATCGTCGTGAGTAGTGAACCGTAAGC")
    with open("DNA_CS.fasta", "w") as f:
        f.write(f">{id}\n{seq}")

def run_minimap2(fastq_file, threads, rna):
    if rna:
        minimap2_cmd = f"minimap2 -x splice -t {threads} DNA_CS.fasta {fastq_file} > {fastq_file}.paf 2> /dev/null"
    else:
        minimap2_cmd = f"minimap2 -x map-ont -t {threads} DNA_CS.fasta {fastq_file} > {fastq_file}.paf 2> /dev/null"
    subprocess.run(minimap2_cmd, shell=True, check=True)

def parse_paf(paf_file):
    try:
        return pd.read_csv(paf_file, sep="\t", header=None)
    except EmptyDataError:
        return pd.DataFrame()

def filter_paf(paf, lower_tolerance):
    required_columns = [1, 10]
    if all(col in paf.columns for col in required_columns):
        paf['aln_ratio'] = paf[1] / paf[10]
        paf_subset = paf[paf['aln_ratio'] > (1 - lower_tolerance)]
        return set(paf_subset[0].tolist())
    else:
        return set()

def write_fastq_filtered_pigz(fastq_file, CS_ids, batch_size, threads):
    """Write filtered FASTQ using pigz for compression"""
    os.makedirs("lysed_fastq", exist_ok=True)
    
    if fastq_file.endswith(".gz"):
        output_file = f"lysed_fastq/{os.path.basename(fastq_file)}"
    else:
        output_file = f"lysed_fastq/{os.path.basename(fastq_file)}.gz"
    
    open_func_input = gzip.open if fastq_file.endswith(".gz") else open
    
    records_written = 0
    records_filtered = 0
    
    pigz_cmd = ["pigz", "-p", str(threads), "-c"]
    
    with open_func_input(fastq_file, "rt") as input_handle:
        with subprocess.Popen(pigz_cmd, stdin=subprocess.PIPE, 
                            stdout=open(output_file, 'wb'), 
                            stderr=subprocess.PIPE,
                            text=True) as pigz_process:
            
            batch_lines = []
            
            try:
                for record in SeqIO.parse(input_handle, "fastq"):
                    if record.id not in CS_ids:
                        batch_lines.extend([
                            f"@{record.id}",
                            str(record.seq),
                            "+",
                            "".join([chr(q + 33) for q in record.letter_annotations['phred_quality']])
                        ])
                        records_written += 1
                    else:
                        records_filtered += 1
                    
                    # Write batch when it reaches batch_size
                    if len(batch_lines) >= batch_size * 4:  # 4 lines per record
                        batch_data = '\n'.join(batch_lines) + '\n'
                        pigz_process.stdin.write(batch_data)
                        batch_lines = []
                
                # Write remaining records in the batch
                if batch_lines:
                    batch_data = '\n'.join(batch_lines) + '\n'
                    pigz_process.stdin.write(batch_data)
                
                pigz_process.stdin.close()
                
                return_code = pigz_process.wait()
                
                if return_code != 0:
                    stderr_output = pigz_process.stderr.read()
                    print(f"Warning: pigz returned non-zero exit code: {return_code}")
                    if stderr_output:
                        print(f"pigz stderr: {stderr_output}")
                
            except BrokenPipeError:
                # Handle case where pigz process terminates early
                print("Warning: pigz process terminated unexpectedly")
            except Exception as e:
                print(f"Error during compression: {e}")
                # Terminate pigz process if still running
                if pigz_process.poll() is None:
                    pigz_process.terminate()
                    pigz_process.wait()
                raise
    
    print(f"Records written: {records_written}")
    print(f"Records filtered out: {records_filtered}")
    return records_written, records_filtered

def main():
    parser = argparse.ArgumentParser(description="Process FASTQ files with minimap2 and filter based on PAF using pigz compression.")
    parser.add_argument("-f", "--fastq_file", required=True, help="Input FASTQ file")
    parser.add_argument("-p", "--paf_file", nargs="?", help="Optional PAF file: if not provided, minimap2 will be run. If provided, the paf file will be for filtering.")
    parser.add_argument("-lt", "--lower_tolerance", nargs="?", type=float, default=0.1, help="Lower tolerance for alignment ratio")
    parser.add_argument("-t", "--threads", type=int, default=8, help="Number of threads for minimap2 and pigz (default: 8)")
    parser.add_argument("-b", "--batch_size", type=int, default=10000, help="Batch size for streaming processing (default: 10000)")
    parser.add_argument("--rna", action="store_true", help="Use for RNA data")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.4")
    args = parser.parse_args()

    if not os.path.exists("DNA_CS.fasta"):
        write_DNA_CS()

    if not args.paf_file or not os.path.exists(args.paf_file):
        print(f"Running minimap2 with {args.threads} threads...")
        run_minimap2(args.fastq_file, args.threads, args.rna)
        paf_file = f"{args.fastq_file}.paf"
    else:
        paf_file = args.paf_file

    print("Parsing PAF file...")
    paf = parse_paf(paf_file)
    CS_ids = filter_paf(paf, args.lower_tolerance)
    
    print(f"Found {len(CS_ids)} sequences to filter out")
    
    write_fastq_filtered_pigz(args.fastq_file, CS_ids, args.batch_size, args.threads)
    
    print("Processing complete!")

if __name__ == "__main__":
    main()
