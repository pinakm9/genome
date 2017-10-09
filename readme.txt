++++++++++++++++++++++ Various files in  program_data folder +++++++++++++++++++++++

# Band files

The program precomputes the bands corresponding to short sequences and used these bands while searching for a read. For example band8.txt containds band corresponding to every 8-character long sequence. First line of band8.txt is '0 209096\n' which implies in the first column of BWT matrix from row 0 to row 209096 start with the prefix 'AAAAAAAA'. The third line is '227222 258112\n' which implies in the 1st column of the BWT matrix from row 227222 to row 258112 begin with 'AAAAAAAG' and so on. The reference sequence contains all possible 8-character strings but does not contain all possible 9-character strings. Therefore our lookup files stop at band8.txt. Band files can be constructed using create_band_files in prepband.py or de-commenting '#create_band_files(col1, bwt, ranks)' in init.py.


# Rank files

Rank (or B-rank) lookup files are created at the start and rank file corresponding to 'A' is 'A_B_rank100.txt'. Ranks are computed 100 characters apart.

# length.txt

Contains lengths of reads. Can be constructed by de-commenting the line '#calc_len(p2_reads, p2_len)' in align.py.

# chrX_1st_col.txt

Contains compressed version of 1st column of BWT matrix. Can be constructed using count_char in rank.py.

# red_green.txt

Contains two arrays of length 6. 1st array correspond to red gene and 2nd one corresponds to green gene. Array elements denote the number of reads that have mapped to the corresponding exon. 


++++++++++++++++++ Search algorithm ++++++++++++++++++
Given a read 'GAGGACAGCACCCAGTCCAGCATCTTCACCTACACCAACAGCAACTCCACCAGAGGTGAGCCAGCAGGCCCGTGGAGGCTGGGTGGCTGCACTGGGGGCCA'  
search would first look up the band corresponding to 'GGGGGCCA' in band8.txt and then shorten the band adding more characters using next_band until the band has at most 5 locations or until we hit a mismatch. Then it compares the reads at the locations indicated by the band.

++++++++++++++++++ Execution +++++++++++++++++++++
Reads are aligned by executing align.py. On my i5 system with 8GB RAM the program takes ~10 mins to finish computation.
