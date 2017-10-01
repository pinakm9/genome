
@timer
def next_band(band, char, map_file, ref_seq_file):
	start, end, start_found = -1, -1, False
	for i in islice(map_file, *band):
		if i == 0:
			continue
		ref_seq_file.seek(i-1)
		if ref_seq_file.read(1) == char:
			if start_found is False:
				start = i
				start_found = True
			else
				end = i
		elif start_found is True:
			break
	return [start, end]


 