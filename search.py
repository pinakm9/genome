# Contains various search functions

from utility import *
from rank import rank, index

red_exons =[[149249757, 149249868],\
			[149256127, 149256423],\
			[149258412, 149258580],\
			[149260048, 149260213],\
			[149261768, 149262007],\
			[149264290, 149264400]]

green_exons=[[149288166, 149288277],\
			[149293258, 149293554],\
			[149295542, 149295710],\
			[149297178, 149297343],\
			[149298898, 149299137],\
			[149301420, 149301530]]

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

#@timer # Returns loaction in the reference sequence and the number of mismatches(not greater than 3)
# given a location i in 1st column and a pattern
# l = len(pattern), k = number of characters counted from the end that will surely match
def match(pattern, i, l, k, seq_file, maps):
	count, l1 = 0, l-k
	i = maps[i]-l1
	text = fetch(seq_file, i, l1, 6)
	print(text)
	for r in range(l1):
		if pattern[r] != text[r]:
			count = count + 1
			if count > 2:
				break
	return [i, count]

@timer # Searches for a pattern using bands and in the eSnd matches the pattern at 
# locations suggested by band calculation 
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

	for i in range(b[0], b[1]+1):
		loc, count = match(pattern, i, l, k, seq_file, maps)
		if count > 2:
			print('Read doesn\'t match at {}'.format(loc))
		else:
			print('Read matches at {}'.format(loc))

# Checks if a location is in reg/green zones, returns exon-number and gene-color
def rg_check(loc):
	for i, ex in enumerate(red_exons):
		if ex[0] <= loc <= ex[1]:
			return [i, 0]
	for i, ex in enumerate(green_exons):
		if ex[0] <= loc <= ex[1]:
			return [i, 1]
	return [-1, -1]

#@timer # Rejects locations not in red/green zones
def match_(pattern, i, l, k, seq_file):
	count, l1 = 0, l-k
	i = i-l1
	ex, color = rg_check(i)
	if color == -1:
		return [-1, -1, -1, 3]
	text = fetch(seq_file, i, l1, 6)
	#print(text)
	for r in range(l1):
		if pattern[r] != text[r]:
			count = count + 1
			if count > 2:
				break
	return [ex, color, i, count]

@timer # Finds the first location where the pattern matches taking reverse complement into account
def search_(pattern, col1, bwt, ranks, bands, seq_file, maps):
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
	locs = maps[b[0]: b[1]+1]
	locs.sort()
	print(locs)
	res, min_mismatch = [], 4
	for j, i in enumerate(locs):
		res.append(match_(pattern, i, l, k, seq_file))
		print res[j]
		if res[j][3] == 0:
			return res[j]
		if min_mismatch > res[j][3]:
			min_mismatch = res[j][3]
			k = j
	return res[k]