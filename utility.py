from time import time

# Timing wrapper
def timer(func):
	def new_func(*args,**kwargs):
		start = time()
		val = func(*args,**kwargs)
		end = time()
		print('Time taken by function {} is {} seconds'.format(func.__name__, end-start))
		return val
	return new_func

@timer # Reads an appropriate file into a Python dictionary
def file_2_dict(file):
	d = {}
	with open(file, 'r') as file: 
		for line in file:
			key, val = line.split()
			d[key] = int(val)
	return d

@timer # Loads a file into a string removing newlines
def load_file(file, offset):
	return file.read()[offset:].replace('\n', '')

@timer 
def load_int(text_arr):
	return list(map(int, text_arr))

#@timer # Fetches length l text from a file given a starting position
def fetch(file, start, l, offset):
	cor1, cor2 = start/100, (start+l)/100
	file.seek(start + cor1 + offset)
	return file.read(cor2-cor1+l).replace('\n', '')

#@timer # Converts each string to a natural number in one-to-one fashion
def base4(text):
	num, d = 0, {'A':0, 'C':1, 'G':2, 'T':3}
	for i, c in enumerate(text[::-1]):
		num = num + d[c]*4**i
	return num

@timer
def band(text, file):
	return list(map(int, file[base4(text)].split()))

# Returns reverse complement of a string
def rev_comp(text):
	d, s = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}, ''
	for c in text[::-1]:
		s = s + d[c]
	return s
