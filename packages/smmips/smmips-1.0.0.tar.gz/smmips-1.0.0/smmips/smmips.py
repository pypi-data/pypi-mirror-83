# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:54:35 2020

@author: rjovelin
"""

import argparse
import os
import json
from smmips.smmips_libs import align_fastqs, assign_reads_to_smmips, create_tree, read_panel, \
count_alleles_across_panel, write_table_variants, parse_cosmic, get_genomic_positions


def assign_smmips(outdir, fastq1, fastq2, reference, bwa, prefix, remove, panel, upstream_nucleotides,
                  umi_length, max_subs, match, mismatch, gap_opening, gap_extension,
                  alignment_overlap_threshold, matches_threshold):
    '''
    (str, str, str, str, str, str, bool, str, int, int, int, float | int, float | int, float | int
    float | int, float | int, float | int) -> None
     
    Parameters
    ----------
    - outdir (str): Path to directory where directory structure is created
    - fastq1 (str): Path to Fastq1
    - fastq2 (str): Path to Fastq2
    - reference (str): Path to the reference genome
    - bwa (str): Path to the bwa script
    - prefix (str): Prefix used to name the output files
    - remove (bool): Remove intermediate files if True                     
    - panel (str): Path to file with smmip information
    - upstream_nucleotides (int): Maximum number of nucleotides upstream the UMI sequence
    - umi_length (int): Length of the UMI    
    - max_subs (int): Maximum number of substitutions allowed in the probe sequence
    - match (float or int): Score of identical characters
    - mismatch (float or int): Score of non-identical characters
    - gap_opening (float or int): Score for opening a gap
    - gap_extension (float or int): Score for extending an open gap
    - alignment_overlap_threshold (float or int): Cut-off value for the length of the de-gapped overlap between read1 and read2 
    - matches_threshold (flot or int): Cut-off value for the number of matching positions within the de-gapped overlap between read1 and read2 
 
    Align fastq1 and fastq2 using bwa mem into coordinate-sorted and indexed bam
    in outdir/out. Write assigned reads, assigned but empty smmips and unassigned
    reads to 3 separate output bams. Assigned reads are tagged with the smMip name
    and the extracted UMI sequence. Also write 2 json files in outdir/stats for QC
    with counts of total, assigned and unassigned read along with empty smmips,
    and read count for each smmip in the panel
    '''
    
    # use current directory if outdir not provided
    if outdir is None:
        outdir = os.getcwd()
    else:
        outdir = outdir
    # create directory structure within outdir, including outdir if doesn't exist
    finaldir, statsdir, aligndir = create_tree(outdir)
    
    # align fastqs
    prefix = os.path.basename(prefix)
    sortedbam = align_fastqs(fastq1, fastq2, reference, outdir, bwa, prefix, remove)
    # assign reads to smmips
    metrics, smmip_counts = assign_reads_to_smmips(sortedbam, read_panel(panel), upstream_nucleotides, umi_length, max_subs, match, mismatch, gap_opening, gap_extension, alignment_overlap_threshold, matches_threshold, remove)
    
    # write json to files
    with open(os.path.join(statsdir, '{0}_extraction_metrics.json'.format(prefix)), 'w') as newfile:
        json.dump(metrics, newfile, indent=4)
    with open(os.path.join(statsdir, '{0}_smmip_counts.json'.format(prefix)), 'w') as newfile:
        json.dump(smmip_counts, newfile, indent=4)
   
   
def count_variants(bamfile, panel, outdir, max_depth, truncate, ignore_orphans,
                   stepper, prefix, reference, cosmicfile):
    '''
    (str, str, str, int, bool, bool, str, str, str) -> None
   
    Parameters
    ----------
    - bamfile (str): Path to the coordinate-sorted and indexed bam file with annotated reads with smMIP and UMI tags
    - panel (str): Path to panel file with smMIP information
    - outdir (str): Path to output directory where out directory is written
    - max_depth (int): Maximum read depth
    - truncate: Consider only pileup columns within interval defined by region start and end if True
    - ignore_orphans: Ignore orphan reads (paired reads not in proper pair) if True
    - stepper: Controls how the iterator advances. Accepted values:
               'all': skip reads with following flags: BAM_FUNMAP, BAM_FSECONDARY, BAM_FQCFAIL, BAM_FDUP
               'nofilter': uses every single read turning off any filtering
    - prefix (str): Prefix used to name the output bam file
    - reference (str): Reference genome. Must be the same reference used in panel. Accepted values: 37 or 38
    - cosmicfile (str): Cosmic file. Tab separated table of all COSMIC coding
                        point mutations from targeted and genome wide screens
    
    Write a summary table with nucleotide and indel counts at each unique position of
    the target regions in panel.
    '''
    
    # use current directory if outdir not provided
    if outdir == None:
        outdir = os.getcwd()
    else:
        outdir = outdir
    # create directory structure within outdir, including outdir if doesn't exist
    finaldir, statsdir, aligndir = create_tree(outdir)

    # get the allele counts at each position across all target regions
    Counts = count_alleles_across_panel(bamfile, read_panel(panel), max_depth, truncate, ignore_orphans, stepper)
    # get positions at each chromosome with variant information
    positions = get_genomic_positions(Counts)
    # get cosmic mutation information
    mutations = parse_cosmic(reference, cosmicfile, positions)

    # write base counts to file
    outputfile = os.path.join(finaldir, '{0}_Variant_Counts.txt'.format(prefix))
    write_table_variants(Counts, outputfile, mutations)


def main():
    '''
    main function to run the smmips script
    '''
    
    # create main parser    
    parser = argparse.ArgumentParser(prog='smmip.py', description="A tool to analyse smMIP libraries")
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
       		
    # assign smMips to reads
    a_parser = subparsers.add_parser('assign', help='Extract UMIs from reads and assign reads to smmips')
    a_parser.add_argument('-f1', '--Fastq1', dest='fastq1', help = 'Path to Fastq1', required=True)
    a_parser.add_argument('-f2', '--Fastq2', dest='fastq2', help = 'Path to Fastq2', required=True)
    a_parser.add_argument('-pa', '--Panel', dest='panel', help = 'Path to panel file with smmip information', required=True)
    a_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    a_parser.add_argument('-r', '--Reference', dest='reference', help = 'Path to the reference genome', required=True)
    a_parser.add_argument('-bwa', '--Bwa', dest='bwa', help = 'Path to the bwa script', required=True)
    a_parser.add_argument('--remove', dest='remove', action='store_true', help = 'Remove intermediate files. Default is False, becomes True if used')
    a_parser.add_argument('-pf', '--Prefix', dest='prefix', help = 'Prefix used to name the output files', required=True)
    a_parser.add_argument('-s', '--Subs', dest='max_subs', type=int, default=0, help = 'Maximum number of substitutions allowed in the probe sequence. Default is 0')
    a_parser.add_argument('-up', '--Upstream', dest='upstream_nucleotides', type=int, default=0, help = 'Maximum number of nucleotides upstream the UMI sequence. Default is 0')
    a_parser.add_argument('-umi', '--Umi', dest='umi_length', type=int, default=4, help = 'Length of the UMI sequence in bp. Default is 4')
    a_parser.add_argument('-m', '--Matches', dest='match', type=float, default=2, \
                          help = 'Score of identical characters during local alignment. Used only if report is True. Default is 2')
    a_parser.add_argument('-mm', '--Mismatches', dest='mismatch', type=float, default=-1, \
                          help = 'Score of non-identical characters during local alignment. Used only if report is True. Default is -1')
    a_parser.add_argument('-go', '--Gap_opening', dest='gap_opening', type=float, default=-5, \
                          help = 'Score for opening a gap during local alignment. Used only if report is True. Default is -5')
    a_parser.add_argument('-ge', '--Gap_extension', dest='gap_extension', type=float, default=-1, \
                          help = 'Score for extending an open gap during local alignment. Used only if report is True. Default is -1')
    a_parser.add_argument('-ao', '--Alignment_overlap', dest='alignment_overlap_threshold', type=int, default=60, \
                          help = 'Cut-off value for the length of the de-gapped overlap between read1 and read2. Default is 60bp')
    a_parser.add_argument('-mt', '--Matches_threshold', dest='matches_threshold', type=float, default=0.7, \
                          help = 'Cut-off value for the number of matching positions within the de-gapped overlap between read1 and read2. Used only if report is True. Default is 0.7')
        
    ## Variant counts command
    v_parser = subparsers.add_parser('variant', help='Write table with variant counts across target regions')
    v_parser.add_argument('-b', '--Bam', dest='bamfile', help = 'Path to the coordinate-sorted and indexed input bam with UMI and smmip tags', required=True)
    v_parser.add_argument('-p', '--Panel', dest='panel', help = 'Path to panel file with smmip information', required=True)
    v_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    v_parser.add_argument('-m', '--MaxDepth', dest='max_depth', default=1000000, type=int, help = 'Maximum read depth. Default is 1000000')
    v_parser.add_argument('-io', '--IgnoreOrphans', dest='ignore_orphans', action='store_true', help='Ignore orphans (paired reads that are not in a proper pair). Default is False, becomes True if used')
    v_parser.add_argument('-t', '--Truncate', dest='truncate', action='store_true', help='Only pileup columns in the exact region specificied are returned. Default is False, becomes True is used')
    v_parser.add_argument('-stp', '--Stepper', dest='stepper', choices=['all', 'nofilter'], default='nofilter',
                          help='Filter or include reads in the pileup. See pysam doc for behavior of the all or nofilter options. Default is nofilter')
    v_parser.add_argument('-pf', '--Prefix', dest='prefix', help = 'Prefix used to name the variant count table', required=True)
    v_parser.add_argument('-rf', '--Reference', dest='reference', type=str, choices=['37', '38'], help = 'Reference genome. Must be the same reference used in panel. Accepted values: 37 or 38', required=True)
    v_parser.add_argument('-c', '--Cosmic', dest='cosmicfile', help = 'Tab separated table of all COSMIC coding point mutations from targeted and genome wide screens', required=True)
    v_parser.set_defaults(func=count_variants)

    args = parser.parse_args()

    if args.subparser_name == 'assign':
        try:
            assign_smmips(args.outdir, args.fastq1, args.fastq2, args.reference, args.bwa, args.prefix, args.remove,
                          args.panel, args.upstream_nucleotides, args.umi_length, args.max_subs,
                          args.match, args.mismatch, args.gap_opening, args.gap_extension,
                          args.alignment_overlap_threshold, args.matches_threshold)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name == 'variant':
        try:
            count_variants(args.bamfile, args.panel, args.outdir, args.max_depth, args.truncate, args.ignore_orphans,
                   args.stepper, args.prefix, args.reference, args.cosmicfile)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name is None:
        print(parser.format_help())

