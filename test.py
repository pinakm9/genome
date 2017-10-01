from gene import *

def count_lines(file):
	count = 0
	with open(file, 'r') as data:
		for line in data:
			count = count + 1
	print('Number of lines = {}'.format(count))
	with open('test.txt', 'a+') as out:
		out.write('\nNumber of lines in {} is {}\n'.format(file, count))

@timer
def zero_line(file):
	i = 0
	with open(file, 'r') as f:
		for line in f:
			if line  == '0\n':
				print('{} found at line {} !!!'.format(line, i))
				break
			i=i+1

@timer
def fread(map_file = p2_map, ref_file = p2_ref):
	i=0
	with open(map_file, 'r') as mf, open(ref_file, 'r') as rf:
		for line in mf:
			line = int(line.rstrip())
			rf.seek(6+line/100+line)
			if rf.read(1) == 'A':
				i = i+1
			else:
				break
	print(i)

init()


#count_lines(p2_map)
search('TATAAAAGCAGACTGCCTGAGCCAGCAGTGGCAACCCAATGGGGTCCCTTTCCATACTGTGGAA')
end()