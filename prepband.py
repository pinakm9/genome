from utility import *
from search import *
import os

def band_file_name(i):
	return 'program_data/band' + str(i) + '.txt'

@timer # Creates band5.txt without using lookup
def prep_band5(col1, bwt, ranks):
	with open(band_file_name(5), 'w+') as file: 
		for a in 'ACGT':
			for b in 'ACGT':
				for c in 'ACGT':
					for d in 'ACGT':
						for e in 'ACGT':
							pattern = a+b+c+d+e
							ba = search1(pattern, col1, bwt, ranks)[1]
							file.write('{} {}\n'.format(ba[0], ba[1]))

@timer # Creates band6.txt using band5.txt
def prep_band6(col1, bwt, ranks):
	with open(band_file_name(6), 'w+') as file, open(band_file_name(5), 'r') as prev:
		lines = prev.readlines() 
		for a in 'ACGT':
			for b in 'ACGT':
				for c in 'ACGT':
					for d in 'ACGT':
						for e in 'ACGT':
							for f in 'ACGT':
								s = b+c+d+e+f
								ba = next_band(band(s, lines), a, col1, bwt, ranks)
								file.write('{} {}\n'.format(ba[0], ba[1]))

@timer # Creates band7.txt using band6.txt
def prep_band7(col1, bwt, ranks):
	with open(band_file_name(7), 'w+') as file, open(band_file_name(6), 'r') as prev:
		lines = prev.readlines() 
		for a in 'ACGT':
			for b in 'ACGT':
				for c in 'ACGT':
					for d in 'ACGT':
						for e in 'ACGT':
							for f in 'ACGT':
								for g in 'ACGT':
									s = b+c+d+e+f+g
									ba = next_band(band(s, lines), a, col1, bwt, ranks)
									file.write('{} {}\n'.format(ba[0], ba[1]))

@timer # Creates band8.txt using band7.txt
def prep_band8(col1, bwt, ranks):
	with open(band_file_name(8), 'w+') as file, open(band_file_name(7), 'r') as prev:
		lines = prev.readlines() 
		for a in 'ACGT':
			for b in 'ACGT':
				for c in 'ACGT':
					for d in 'ACGT':
						for e in 'ACGT':
							for f in 'ACGT':
								for g in 'ACGT':
									for h in 'ACGT':
										s = b+c+d+e+f+g+h
										ba = next_band(band(s, lines), a, col1, bwt, ranks)
										file.write('{} {}\n'.format(ba[0], ba[1]))

@timer # Creates band9.txt using band8.txt
def prep_band9(col1, bwt, ranks):
	with open(band_file_name(9), 'w+') as file, open(band_file_name(8), 'r') as prev:
		lines = prev.readlines() 
		for a in 'ACGT':
			for b in 'ACGT':
				for c in 'ACGT':
					for d in 'ACGT':
						for e in 'ACGT':
							for f in 'ACGT':
								for g in 'ACGT':
									for h in 'ACGT':
										for i in 'ACGT':
											s = b+c+d+e+f+g+h+i
											ba = next_band(band(s, lines), a, col1, bwt, ranks)
											file.write('{} {}\n'.format(ba[0], ba[1]))

@timer # Check if two consecutive band files have identical bands at the same position
# If they do, the bigger file not usable. Turns out band8.txt is usable but not band9.txt
def check_band(i, I):
	corrupt = False
	with open(band_file_name(i), 'r') as small, open(band_file_name(I), 'r') as big:
		lines = big.readlines()
		for i, line in enumerate(small):
			if line == lines[i]:
				corrupt = True
				break
	if corrupt is False:
		print('{} is okay'.format(band_file_name(I)))
	else:
		print('{} is corrupt'.format(band_file_name(I)))

@timer # Creates the necessary band files 
def create_band_files(col1, bwt, ranks):
	for i in range(5, 10):
		if not os.path.isfile(band_file_name(i)):
			if i == 5:
				prep_band5(col1, bwt, ranks)
			elif i == 6:
				prep_band6(col1, bwt, ranks)
			elif i == 7:
				prep_band7(col1, bwt, ranks)
			elif i == 8:
				prep_band8(col1, bwt, ranks)