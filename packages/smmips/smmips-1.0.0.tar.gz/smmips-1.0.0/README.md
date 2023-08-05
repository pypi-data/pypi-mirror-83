# smMIPs #

smMIPs is tool for analyzing Single Molecule Molecular Inversion Probes libraries.

## Installation ##
### From PyPi ###
smmips is available from PyPi

```pip install smmips```

## smMIP assignment ##

The first step is to assign smMIPs to reads.
Paired fastqs containing UMI sequences are aligned with bwa mem to a reference genome.
Each aligned read pair is then assigned to a smMIP listed in the input panel.
The panel should be designed with [MIPGEN](http://shendurelab.github.io/MIPGEN/) and have the same columns and header. 
The main output is a coordinate-sorted and indexed bam with reads assigned to smMIPs and tagged with the smMIP name and the UMI sequence.

This step also generates two other bams:
- bam with reads assigned to smMips but lacking the capture target
- bam with unassigned reads

QC metrics with read counts are reported in two json files:
- read counts, including total reads, assigned and unassigned reads, empty smMIPs
- read counts without and with target for each smMIP in the panel

## Nucleotide counts ##

The second step is taking the aligned reads assigned to smMIPs from step 1 as input to generate a table with nucleotide and indel counts at each unique position of the target regions in the panel. It also uses annotation for coding point mutations from [COSMIC](https://cancer.sanger.ac.uk/cosmic).
