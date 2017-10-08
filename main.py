from init import *
from search import search_
from time import time
from utility import rev_comp

red = [0]*6
green = [0]*6

with open(p2_reads, 'r') as reads: 
	r = reads.readlines()
	s = time()
	for i, read in enumerate(r):
		read = read[:-1].replace('N','A')
		ex, color, loc, mismatch = search_(read, col1, bwt, ranks, bands, seq_file, maps)
		if mismatch <3:
			if color == 0:
				red[ex] = red[ex] + (1 if mismatch == 0 else 0.5)
			elif color == 1:
				green[ex] = green[ex] + (1 if mismatch == 0 else 0.5)
		else:
			ex, color, loc, mismatch = search_(rev_comp(read), col1, bwt, ranks, bands, seq_file, maps)
			if mismatch <3:
				if color == 0:
					red[ex] = red[ex] + (1 if mismatch == 0 else 0.5)
				elif color == 1:
					green[ex] = green[ex] + (1 if mismatch == 0 else 0.5)
	e = time()
with open(p2_out, 'w') as out:
	for ex in range(6):
		out.write('{} '.format(red[ex]))
	out.write('\n')
	for ex in range(6):
		out.write('{} '.format(green[ex]))
print('Time taken by main.py is {} seconds'.format(e-s))
