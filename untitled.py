TCATAGGTAACTACACACAGGTAACAGCTTCCTAAGGAATAGCACATTGATGATCTCATCCAGTCTGATTAAACCCTAAGTCAATGCAGCTTTCAGTGTT


@timer # Computes band given a suffix
def search(pattern):
	m, l, p =  ref_len/2, len(pattern), 2
	while p < ref_len:
		p = 2*p
		text = get_chunk(m, l)
		if pattern == text
			print('WE FOUND IT CAPTAIN !!!')
			break
		elif pattern > text:
			m = m + ref_len/p
		else:
			m = m - ref_len/p

