from utility import *
from rank import *
from prepband import *
import os 

# Loads first column of BWT matrix into RAM
def load_1st_col():
	d = file_2_dict(p2_1st_col) 
	rl = sum(d[char] for char in 'ACGT') + 1  # Adding 1 to account for '$'
	return [d, rl]

p2_bwt = './../data/chrX_last_col.txt'   	  # Path to last column of BWT
p2_1st_col = 'program_data/chrX_1st_col.txt'  # Path to first column of BWT
p2_seq = './../data/chrX.fa'				  # Path to reference sequence
p2_map = './../data/chrX_map.txt'             # Path to suffix array of the reference sequence
p2_reads = './../data/reads'				  # Path to reads
p2_band = 'program_data/band8.txt'			  # Path to precalculated bands for all 8-character strings
p2_rg = 'program_data/red_green.txt' 		  # Stores number of reads that map to some red/green exon 

p2_align = 'program_data/align.txt'			  # Stores read alignments in 'location mismatch\n' format
p2_len = 'program_data/length.txt'			  # Stores read-lengths
bands = [None]*(4**8)						  # Array for band lookup
bwt_file = open(p2_bwt, 'r')				  # File object corresponding to last column of BWT matrix
seq_file = open(p2_seq, 'r')				  # File object corresponding to reference sequence
map_file = open(p2_map, 'r')				  # File object corresponding to suffix array
col1, ref_len = load_1st_col()				  # 1st column of BWT matrix(compressed) and
											  # length of reference sequence
print('Loading last column of BWT matrix....')
bwt = load_file(bwt_file, 0)				  # Last column of BWT matrix
print('Last column of BWT matrx has loaded\n\nLoading suffix array....')
maps = load_int(map_file.readlines())   	  # Suffix array
print('Suffix array has loaded')
prep_B_rank(bwt_file, ref_len)
print('\nLoading rank lookup table...')
ranks = load_rank()						 	  # Array of precomputed ranks
print('Rank lookup table has loaded')
print('\nLoading band lookup file....')
#create_band_files(col1, bwt, ranks)
for i, line in enumerate(open(p2_band, 'r')):		  
	bands[i] = load_int(line.split())
print('Band lookup file has loaded\n')
