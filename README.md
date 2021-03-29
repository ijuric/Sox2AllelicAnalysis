# Sox2AllelicAnalysis
Analysis files for Sox2 gene

This repository contains scripts used to create and run modified WASP (https://github.com/bmvdgeijn/WASP) pipeline to analyze PLAC-Seq data.
Instead of regular bowtie2 mapping, we use mapping and preprocessing as implemented in MAPS (https://github.com/ijuric/MAPS).

**Step1:**

WASP checks if reads have 'is proper' cigar tag. This tag is set to 0 if two read ends map too far (useful for ChIP-seq data, but not useful for 
PLAC-seq data where reads can map to very distant areas).
After cloning WASP from github, in mapping/rmdup_pe.py comment out this:
if not read.is_proper_pair:
    read_stats.discard_improper_pair += 1
continue
and save it as mapping/rmdup_pe_long_range.py

In mapping/filter_remapped_reads.py comment out this:
if not read.is_proper_pair:
    bad_reads.add(orig_name)
continue
and save it as mapping/filter_remapped_reads_long_range.py

**Step 2:**

Create .h5 files by running create_h5.py [DATASET] where [DATASET] is the name of your dataset. This is equivalent of doing step 1 in WASP pipeline,
but also splits data by chromosome because otherwise analysis doesn't work.

**Step 3:**

Run MAPS. How to set up MAPS run files is explained here: https://github.com/ijuric/MAPS

**Step 4:**

Run make_WASP_runfiles.py script. This will create two .sh files. First .sh file (part1) will create some subdirectories in the folder where
you run it and it will then perform steps 3 of WASP pipeline using appropriate .bam files from MAPS feather_output subdirectory in your MAPS folder

**Step 5:**

Run MAPS again using .fq.gz files that need to be remapped (this is equivalent of step 4, but using bwa mem and MAPS feather preprocessing 
instead of bowtie2). The easiest way to do this is to make a copy of your MAPS runfile (used in step 3) and modify the following lines:
maps=0
dataset_name="[DATASET_NAME].remap"
fastq_format=".fq.gz"
fastq_dir="[DATASET_WASP_ANALYSIS_DIR]/find_intersecting_snps_ALL/"
Where [DATASET_NAME] is the name of your dataset and [DATASET_WASP_ANALYSIS_DIR] is directory where you are performing your WASP mapping
(The directory with .h5 files in Step 2). This directory already has find_intersecting_snps_ALL subdirectory in it (it was created by part1 script)

**Step 6:**

Run part2 script. This one performs steps 5,6 and 7 of WASP pipeline. It will create rmdup_feather_full/[DATASET_NAME].FINAL.bam file. This is .bam
file that contains mapped reads.

**Step 7:**

This part extracts and labels allelic reads from /bam file in previous step. Run make_pair.py like this:
python make_pair.py -b rmdup_feather_full/[DATASET_NAME].FINAL.bam -v F123.vcf -o [DATASET_NAME].FINAL.feather_full.txt.gz
The result is a table with all pair-end reads. Those that are allelic will be labeled 0 or 1, depending if they're from CAST of 129S genomes

