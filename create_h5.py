### This scrip creates .h5 files needed for WASP mapping
### Make sure that vcf and mm10.autosomal.chrom.sizes files are in the same directory as this script
### snp2h5 should point to location of 2np2h5 file in the WASP (see step 1 https://github.com/bmvdgeijn/WASP/tree/master/mapping )

import subprocess as sp

dataset_name = [DATASET_NAME] ## RH625 or RH635
vcf = "F123.vcf"
snp2h5 ="/WASP/snp2h5/snp2h5"

dn = dataset_name+'\n'
f = open('samples.txt','w')
f.write(dn)
f.close()

chroms = ['chr1', 'chr2','chr3','chr4','chr5','chr6','chr7', 'chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21']
header = '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'+dataset_name+'\n'
f = open('header.txt','w')
f.write(header)
f.close()

for chrom in chroms:
    c1 = 'cat header.txt > '+chrom+'.'+dataset_name+'.txt'
    c2 = 'grep \'' + chrom + '\t\'' + vcf + ' >> '+chrom + '.' + dataset_name + '.txt' 
    print ('doing ' + c1)
    sp.call(c1, shell=True)
    print ('doing ' + c2)
    sp.call(c2, shell=True)
    c3 = snp2h5 + '--chrom mm10.autosomal.chrom.sizes --format vcf --haplotype h.h5 --snp_index snp_index.h5 --snp_tab snp_tab.h5 '+\
'chr*.'+dataset_name+'.txt'
    sp.call(c3, shell=True)

