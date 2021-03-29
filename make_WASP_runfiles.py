### Script that creates shell scripst to run WASP. This will create two files: .ALL.run_WAP.txt and .ALL.run_WASP.part2.txt
### File .ALL.run_WASP.txt will run steps 2 and 3 of WASP pipeline and move files in appropriate directory
### The result of this script are two .fq.gz files which contain reads that need to be remapped with MAPS
### To remap them, one can use the same MAPS script as before with following changes:
### dataset_name="[DATASET_NAME].remap"
### fastq_format=".fq.gz"
### fastq_dir="[DATASET_WASP_ANALYSIS_DIR]/find_intersecting_snps_ALL/"
### Where [DATASET_NAME] is the name of your dataset (RH625 or RH635) and [DATASET_WASP_ANALYSIS_DIR] is directory
### where your WASP mapping outputs will be.
### After you run the .ALL.run_WASP.txt scrpit and remapping, run .ALL.run_WASP.part2.txt script. That will
### complete steps 5,6 and 7 of WASP and create rmdup_feather_full/[DATASET_NAME].FINAL.bam file
### Last step is to use make_pair.py script to extract allelic reads by running:
### python make_pair.py -b rmdup_feather_full/[DATASET_NAME].FINAL.bam -v F123.vcf -o [DATASET_NAME].FINAL.feather_full.txt.gz


import sys
import subprocess as sp

dataset = sys.argv[1] ## dataset name (RH625 or RH635)
DATASET_WASP_ANALYSIS_DIR = sys.argv[2] ## Directory where your .h5 files are. This will be directory where youe WASP analysis will be done.
MAPS_DIR = sys.argv[3] ## your MAPS project directory. That is the directory that you ran MAPS in. It includes feather_output subdirectory.

chroms = ['ALL']
indir = DATASET_WASP_ANALYSIS_DIR
map1 = MAPS_DIR + '/' + dataset + '_current/' + dataset + '.paired.srt.bam'
feather_dir_in = indir + '/feather_output/'

## step1
for chrom in chroms:
    outstr0 = 'samtools index ' + map1 + ' ' + map1 + '.bai\n'
    out_dir = indir + 'find_intersecting_snps_' + chrom
    outstr1 = 'mkdir ' + out_dir + '\n'
    command_call = 'python /home/jurici/WASP/WASP/mapping/find_intersecting_snps_long_range.py --is_paired_end --is_sorted '
    output_dir = '--output_dir ' + out_dir + ' '
    h5 = dataset + '.h.h5'
    snp_tab = dataset + '.snp_tab.h5'
    snp_index = dataset + '.snp_index.h5'
    h5_files = '--snp_tab ' + indir + snp_tab + ' --snp_index ' + indir + snp_index + ' --haplotype ' + indir + h5 + ' '
    sample_name = 'samples_' + dataset + '.txt'
    samples = '--samples ' + indir + sample_name + ' ' + map1 + ' > ' + indir + dataset + 'map1.nohup 2> ' + indir + dataset + '.map1.log'
    outstr2 = command_call + output_dir + h5_files + samples + '\n'
    map2 = indir + 'map2_' + chrom + '/'
    outstr3 = 'mkdir ' + map2 + '\n'
    outstr4 = 'mv ' + out_dir + '/' + dataset + '.paired.srt.remap.fq1.gz ' + out_dir + '/' + dataset + '.remap_R1.fq.gz\n'  
    outstr5 = 'mv ' + out_dir + '/' + dataset + '.paired.srt.remap.fq2.gz ' + out_dir + '/' + dataset +  '.remap_R2.fq.gz\n'
    fname = dataset + '.' + chrom + '.run_WASP.part1.sh'
    f = open(fname, 'w+')
    f.write(outstr0)
    f.write(outstr1)
    f.write(outstr2)
    f.write(outstr3)
    f.write(outstr4)
    f.write(outstr5)
    f.close()
    ### run feather
    
    feather_dir = feather_dir_in + dataset +'.remap_current/'
    feather_bam = dataset + '.remap.paired.srt.bam'
    outstr6 = 'cp ' + feather_dir + feather_bam + ' ' + map2 + dataset + '.sort.bam\n'
    outstr7 = 'samtools index ' + map2 + dataset + '.sort.bam\n'
    filter_remapped_reads = indir + 'filter_remapped_reads_' + chrom + '/' 
    outstr8 = 'mkdir ' + filter_remapped_reads + '\n'
    outstr9 = 'python /home/jurici/WASP/WASP/mapping/filter_remapped_reads_long_range.py ' + out_dir + '/' + dataset + '.paired.srt.to.remap.bam ' +\
 map2 + dataset + '.sort.bam ' + filter_remapped_reads + dataset + '.keep.bam\n'
    fmerge = indir + 'merge_' + chrom + '/'
    outstr10 = 'mkdir ' + fmerge + '\n'
    outstr11 = 'samtools merge ' + fmerge + dataset + '.paired.srt.keep.merge.bam ' + filter_remapped_reads + dataset + '.keep.bam ' +\
out_dir + '/' + dataset + '.paired.srt.keep.bam\n'
    outstr12 = 'samtools sort -o ' + fmerge + dataset + '.keep.merge.sort.bam ' + fmerge + dataset + '.paired.srt.keep.merge.bam\n'
    outstr13 = 'samtools index ' + fmerge + dataset + '.keep.merge.sort.bam\n'
    rmdup = indir + 'rmdup_' + chrom + '/'
    outstr14 = 'mkdir ' + rmdup + '\n'
    outstr15 = 'python /home/jurici/WASP/WASP/mapping/rmdup_pe_long_range.py ' + fmerge + dataset + '.keep.merge.sort.bam ' + rmdup + dataset + '.FINAL.bam\n'
    full_outstr = outstr6 + outstr7 + outstr8 + outstr9 + outstr10 + outstr11 + outstr12 + outstr13 + outstr14 + outstr15
    fname = dataset + '.' + chrom + '.run_WASP.part2.sh'
    f = open(fname, 'w+')
    f.write(full_outstr)
    f.close()



    

