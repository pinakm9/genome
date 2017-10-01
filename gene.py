import os, time
from itertools import islice

p2_last_col = './../data/chrX_last_col.txt'   # Path to last column of BWT
p2_1st_col = 'program_data/chrX_1st_col.txt'  # Path to first column of BWT
p2_ref = './../data/chrX.fa'				  # Path to reference sequence
p2_map = './../data/chrX_map.txt'             # Path to suffix array of the reference sequence
p2_gen_data = 'program_data/'				  # Path to program generated data
char_set = 'ACGT$\n'						  # Set of characters in file containing BWT column 
milestone_gap = 100							  # Distance between consecutive milestones
line_len = 100                                # Length of a regular line in reference  file and BWT file
offset = len('>chrX\n')                       # Index where reference sequence starts in the file
ref_len = 0									  # Length of the reference sequence (to be computed by init)
col1 = {}									  # First column of BWT (to be computed by init)
ranks = {}									  # Dictionary that stores rank arrays (to be computed by init)
map_file = open(p2_map, 'r')				  # File object corresponding to suffix array
ref_file = open(p2_ref, 'r')				  # File object corresponding to reference sequence
arr = []									  # Suffix array

# Returns rank filename given a chracter
def rank_file(char):
	return p2_gen_data + char + '_B_rank' + str(milestone_gap) + '.txt'

# Reads an appropriate file into a Python dictionary
def file_2_dict(file):
	d = {}
	with open(file, 'r') as file: 
		for line in file:
			key, val = line.split()
			d[key] = int(val)
	return d

# Timing wrapper
def timer(func):
	def new_func(*args,**kwargs):
		start = time.time()
		val = func(*args,**kwargs)
		end = time.time()
		print('Time taken by function {} is {} seconds'.format(func.__name__, end-start))
		return val
	return new_func

@timer # Counts number of specific characters in a file
def count_char(chars = char_set, file_in = p2_last_col, file_out = p2_1st_col):
	count, length = {}, 0
	for char in chars:
		count[char] = 0
	with open(file_in, 'r') as file:
		for line in file:
			for char in line:
				count[char] = count[char] + 1
	with open(file_out, 'w+') as out:
		for char in chars[:-2]:
			out.write('{} {}\n'.format(char, count[char]))
	
@timer # Computes B-ranks at milestones (prep_B_rank won't work if milestone_gap is not equal to line_len)
def prep_B_rank(chars = char_set[:-1], bwt_file = p2_last_col):
	rank, files = {}, []
	for char in chars[:-1]:
		files.append(open(rank_file(char), 'w+'))
		files[len(files)-1].write('0\n')
	for char in chars:	
		rank[char] = 0
	with open(bwt_file, 'r') as bwt:
		for mile in range(ref_len/milestone_gap): 
			for char in bwt.read(milestone_gap):
				rank[char] = rank[char] + 1
			for i, char in enumerate(chars[:-1]):
				files[i].write('{}\n'.format(rank[char]))
			bwt.seek(1,1) # Ignore newline
	for file in files:
		file.close()

@timer # Loads rank arrays into a dictionary
def load_rank(chars = char_set[:-2]):
	d = {}
	for char in chars:
		with open(rank_file(char), 'r') as file:
			d[char] = list(map(int, file.read().split()))
	return d

# Loads first column of BWT matrix into RAM
def load_1st_col():
	d = file_2_dict(p2_1st_col) 
	rl = sum(d[char] for char in char_set[:-2]) + 1 # Adding 1 to account for '$'
	return [d, rl]

@timer # Creates various objects required for the program to function
def init():
	try: 
		os.makedirs('program_data')
	except:
		pass
	if not os.path.isfile(p2_1st_col):
		count_char()
	for char in char_set[:-2]:
		if not os.path.isfile(rank_file(char)):
			prep_B_rank()
			break
	global col1, ref_len, ranks, arr 
	col1, ref_len = load_1st_col()
	ranks = load_rank()
	arr = [None]*(ref_len)
	for i, line in enumerate(map_file):
		arr[i] = int(line)


# Prepares closure of the program
def end():
	map_file.close()
	ref_file.close()

#@timer # Computes B-rank
def rank(i, bwt_file = p2_last_col):
	miles, correction = i/milestone_gap, i/line_len
	position = i + correction # Correction for ignoring newlines
	with open(p2_last_col, 'r') as bwt:
		bwt.seek(position)
		char = bwt.read(1)
		start = miles*milestone_gap + correction # Correction for ignoring newlines
		bwt.seek(start)
		r = ranks[char][miles]
		for ch in bwt.read(position - start):
			if ch == char:
				r = r + 1
	return r

# Computes index of char in the first column given rank
def index(char, r):
	s = 0
	for ch in char_set[:-2]:
		if ch != char:
			s = s + col1[ch]
		else:
			break
	return s + r

# Computes index of char in first column given 
# index corresponding to same-rank char in last column
def index2(char, i):
	return index(char, rank(i))

@timer # Computes band for string char+x given the band for string x
def next_band(band, char):
	start, end = -1, -1
	for j,i in enumerate(arr[band[0]:band[1]]):
		i = int(i)
		ref_file.seek(offset + i + i/line_len -1)
		#print(ch,c)
		if ref_file.read(1) == char:
			if start == -1:
				start = j
			end = j
	return list(map(lambda x: index2(char, x+band[0]), [start, end]))

@timer # Returns a chunk of reference sequence from starting index
def get_chunk(start, length):
	ref_file.seek(offset + start + start/line_len)
	end =  start + length
	l = length + end/line_len - start/line_len
	return ref_file.read(l).replace('\n', '')

@timer # Binary serach in suffix array
def search(pattern):
	m, l, p, found =  ref_len/2, len(pattern), 2, False
	while p < ref_len:
		p = 2*p
		s = arr[m]	
		text = get_chunk(s, l)
		if pattern == text:
			found = True
			break 
		elif pattern > text:
			m = m + ref_len/p
		else:
			m = m - ref_len/p
	return s if found is True else -1

