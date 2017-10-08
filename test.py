from init import *
from search import *
#from gene import *
#from utility import *
#from prepband import *

#init()


#prep_band9(col1,bwt, ranks)
def verify(s = 'AGCGCT'):
		ba = band(s, lines_in_band)
		for i in range(ba[0], ba[1]):
			b = int(lines_in_map[i])
			print(fetch(seq_file, b, len(s),6))

s = 'GAGGACAGCACCCAGTCCAGCATCTTCACCTACACCAACAGCAACTCCACCAGAGGTGAGCCAGCAGGCCCGTGGAGGCTGGGTGGCTGCACTGGGGGCCA'
l = len(s)

print search(s, col1, bwt, ranks, bands, seq_file, maps)

def verify_search(band, pattern, k):
	i = band[0]
	while i <= band[1]:
		text = fetch(seq_file, int(lines_in_map[i]), k, 6)
		if text == pattern[-k:]:
			print('match found at {}, {}'.format(i, text, pattern[-k:]))
		else:
			print('mismatch at {}, {}'.format(i, text))
		i = i+1	

#verify_search(b,s,k)
#verify()
"""for b in red_exons:
	print(b, fetch(seq_file, b[0], b[1]-b[0]+1, 6))
print('__________________________________')
for b in green_exons:
	print(b, fetch(seq_file, b[0], b[1]-b[0]+1, 6))"""
#print fetch(seq_file, 149325341, 101, 6)
"""with open('program_data/progress_log.txt', 'r') as log, open('program_data/output.txt', 'r') as out:
	completed = int(log.read().split()[0])
	print(completed)
	lines = out.readlines()
	red = list(map(float, lines[0].split()))
	green = list(map(float, lines[1].split()))
	print(red, green)"""