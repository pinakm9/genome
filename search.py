# Contains various search functions

from utility import *
from rank import *

exons = {'red':[[149249757, 149249868],\
				[149256127, 149256423],\
				[149258412, 149258580],\
				[149260048, 149260213],\
				[149261768, 149262007],\
				[149264290, 149264400]],\

		'green':[[149288166, 149288277],\
				[149293258, 149293554],\
				[149295542, 149295710],\
				[149297178, 149297343],\
				[149298898, 149299137],\
				[149301420, 149301530]]}

# Returns band in the 1st column given a character 
def first_band(char):
	if char == 'A':
		return [0, 45648951]
	elif char == 'C':
		return [45648952, 75462304]
	elif char == 'G':
		return [75462305, 105328135]
	else:
		return [105328136, 151100559]


#@timer # Updates current band 
def next_band(band, next_char, col1, bwt, ranks):
	start, end = -1, -1
	text = bwt[band[0]:band[1]+1]
	for i, c in enumerate(text):
		if c == next_char:
			start = band[0]+i
			break
	if start == -1:
		return band
	for i, c in enumerate(text[::-1]):
		if c == next_char:
			end = band[1]-i
			break
	return list(map(lambda x: index(next_char, rank(x, next_char, bwt, ranks), col1), [start, end]))


# Returns number of matched characters and the smallest band without using band lookup
def search1(pattern, col1, bwt, ranks):
	l, k = len(pattern), 1 # k = number of matched characters from the right
	b, nb = [0, 0], first_band(pattern[l-k])
	while nb != b:
		b = nb
		k = k+1
		if k > l:
			k = l
			break
		nb = next_band(b, pattern[l-k], col1, bwt, ranks)
	if k != l:
		k = k-1
		print('Partial match: matched {} characters'.format(k))
	return [k, b]

@timer # Returns number of matched characters and the smallest band using bandN.txt
def searchN(pattern, col1, bwt, ranks, bands, N):
	l, k = len(pattern), N # k = number of matched characters from the right
	b, nb = [0, 0], bands[base4(pattern[-N:])]
	while nb != b:
		b = nb
		k = k+1
		if k > l:
			k = l
			break
		nb = next_band(b, pattern[l-k], col1, bwt, ranks)
	if k != l:
		k = k-1
	return [k, b]

#@timer # Returns number of mismatches given a location i in the reference sequence and a pattern
# l = number of characters from the left that we want to match
def match(pattern, i, l, seq_file, maps):
	mismatch, text = 0, fetch(seq_file, i, l, 6)
	# print(text)
	for r in range(l):
		if pattern[r] != text[r]:
			mismatch = mismatch + 1
	return mismatch

#@timer # Finds read in the sequence, returns best matching location and number of mismatches
def search(pattern, col1, bwt, ranks, bands, seq_file, maps):
	l, k, short = len(pattern), 8, False # k = number of matched characters from the right
	b, nb = [0, 0], bands[base4(pattern[-8:])]
	while nb != b:
		b = nb
		if b[1]-b[0] < 5:
			short = True
			break
		k = k+1
		if k > l:
			k = l
			break
		nb = next_band(b, pattern[l-k], col1, bwt, ranks)
	if k != l and short != True:
		k = k-1
	l, locs = l-k, []
	for i in maps[b[0]:b[1]+1]:
		if i >= l:
			locs.append(i-l)
	locs.sort()
	min_mismatch, mmi, res = 4, -1, []
	for j, i in enumerate(locs):
		res.append([i, match(pattern, i, l, seq_file, maps)])
		#print(res[j])
		if res[j][1] == 0:
			return res[j]	
		elif min_mismatch > res[j][1]:
			min_mismatch = res[j][1]
			mmi = j
	return res[mmi]

#@timer # search that takes reverse complements into account
def search_(pattern, col1, bwt, ranks, bands, seq_file, maps):
	loc, mismatch = search(pattern, col1, bwt, ranks, bands, seq_file, maps)
	if mismatch != 0:
		loc1, mismatch1 = search(rev_comp(pattern), col1, bwt, ranks, bands, seq_file, maps)
		if mismatch < mismatch1:
			return [loc, mismatch]
		else:
			return [loc1, mismatch1]
	return [loc, mismatch]
