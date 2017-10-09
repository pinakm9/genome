from utility import *

@timer # Counts number of specific characters in a file i.e. prepares rank calculation on 1st column
def count_char(charset, chars, file_in, file_out):
	count, length = {}, 0
	for char in charset:
		count[char] = 0
	with open(file_in, 'r') as file:
		for line in file:
			for char in line:
				count[char] = count[char] + 1
	with open(file_out, 'w+') as out:
		for char in chars:
			out.write('{} {}\n'.format(char, count[char]))

# Returns name of rank file given a character
def rank_file(char):
	return 'program_data/' + char + '_B_rank' + '100' + '.txt'

@timer # Computes B-ranks at milestones (distance between consecutive milestones = 100)
def prep_B_rank(bwt_file, ref_len): 
	rank, files = {}, []
	for char in 'ACGT':
		files.append(open(rank_file(char), 'w+'))
		files[len(files)-1].write('0\n')
	for char in 'ACGT$':	
		rank[char] = 0
	bwt_file.seek(0)
	for mile in range(ref_len/100): 
		for char in bwt_file.read(100):
			rank[char] = rank[char] + 1
		for i, char in enumerate('ACGT'):
			files[i].write('{}\n'.format(rank[char]))
		bwt_file.seek(1,1) # Ignore newline
	for file in files:
		file.close()

#@timer # Computes B-rank
def rank(i, bwt, rank_table):
	miles = i/100
	char = bwt[i]
	r = rank_table[char][miles]
	for ch in bwt[miles*100: i]:
		if ch == char:
			r = r + 1
	return r

#@timer # Computes B-rank
def rank(i, char, bwt, rank_table):
	miles = i/100
	r = rank_table[char][miles]
	for ch in bwt[miles*100: i]:
		if ch == char:
			r = r + 1
	return r

@timer # Loads rank arrays into a dictionary
def load_rank():
	d = {}
	for char in 'ACGT':
		with open(rank_file(char), 'r') as file:
			d[char] = load_int(file.read().split())
	return d

# Computes index of char in the first column given rank
def index(char, r, column1):
	s = 0
	for ch in 'ACGT':
		if ch != char:
			s = s + column1[ch]
		else:
			break
	return s + r
