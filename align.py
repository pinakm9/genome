from init import *
from search import *
from utility import * 

@timer  # Aligns reads
def align(n = 3066720):
	print('\nRead alignment has begun....')
	with open(p2_align, 'w+') as algn, open(p2_reads, 'r') as reads:
		for i, read in enumerate(reads):
			read = read[:-1].replace('N','A')
			loc, mismatch = search_(read, col1, bwt, ranks, bands, seq_file, maps)
			algn.write('{} {}\n'.format(loc, mismatch))
			if i == n-1:
				break
	print('Read alignment finished')

# Sets weight for a read given its location, length and number of mismatches
def weight(left, length, mismatch):
	right = left + length - 1
	if mismatch <= 2:
		for gene in exons:
			for i, ex in enumerate(exons[gene]):
				if ex[0] <= left and right <= ex[1] and mismatch == 0:
					return [gene, i, 1]	
				elif ex[0] <= left <= ex[1]: #and ex[1]-left >= length/2:
					return [gene, i, 0.5]
	return ['red', 0, 0]

@timer # Counts reads mapping to red/green genes
def count_reads():
	print('\nCounting reads mapping to red/green genes....')
	read_count = {'red':[0]*6, 'green':[0]*6}
	with open(p2_align, 'r') as algn, open(p2_len, 'r') as length, open(p2_rg, 'w+') as rg:
		l = length.readlines() 
		for i, line in enumerate(algn):
			left, mismatch = load_int(line.split())
			gene, ex, w = weight(left, int(l[i]), mismatch)
			read_count[gene][ex] = read_count[gene][ex] + w
		rg.write('{}\n'.format(read_count['red']))
		rg.write('{}\n'.format(read_count['green']))
	print('Counting finished')

align()
#calc_len(p2_reads, p2_len)
count_reads()
