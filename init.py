from utility import *
from rank import load_rank, prep_B_rank, count_char
import os 

# Loads first column of BWT matrix into RAM
def load_1st_col():
	d = file_2_dict(p2_1st_col) 
	rl = sum(d[char] for char in 'ACGT') + 1 # Adding 1 to account for '$'
	return [d, rl]

p2_bwt = './../data/chrX_last_col.txt'   	  # Path to last column of BWT
p2_1st_col = 'program_data/chrX_1st_col.txt'  # Path to first column of BWT
p2_seq = './../data/chrX.fa'				  # Path to reference sequence
p2_map = './../data/chrX_map.txt'             # Path to suffix array of the reference sequence
p2_reads = './../data/reads'				  # Path to reads
p2_band = 'program_data/band8.txt'			  # Path to precalculated bands for all 8-character strings
p2_out = 'program_data/output.txt' 			  # Stores number of reads that map to some red/green exon 
											  # 1st line corresponds to red, 2nd line corresponds to green

bands = [None]*(4**8)						  # Array of precomputed bands
bwt_file = open(p2_bwt, 'r')
seq_file = open(p2_seq, 'r')
map_file = open(p2_map, 'r')
band_file = open(p2_band, 'r')
bwt = load_file(bwt_file, 0)				  # Last column of BWT matrix
maps = load_int(map_file.readlines())   	  # Suffix array
col1, ref_len = load_1st_col()				  # 1st column of BWT matrix(compressed) and
											  # length of reference sequence	
ranks = load_rank()							  # Array of precomputed ranks
for i, line in enumerate(band_file):
	bands[i] = load_int(line.split())


@timer # Creates various objects required for the program to function
def init():
	try: 
		os.makedirs('program_data')
	except:
		pass
	if not os.path.isfile(p2_1st_col):
		count_char('ACGT$\n', 'ACGT', p2_bwt, p2_1st_col)
	for char in 'ACGT':
		if not os.path.isfile(rank_file(char)):
			prep_B_rank(bwt_file)
			break