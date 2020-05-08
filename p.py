import json

def inRWI(rwi, key):
	key = key.lower()
	if key in rwi:
		print('{} : {}'.format(key, rwi[key]))
		return True
	return False

def pairInRWI(rwi, key1, key2):
	if not inRWI(rwi, key1) or not inRWI(rwi, key2):
		return False
	for pos in rwi[key1]:
		if pos + 1 in rwi[key2]:
			return True
	return False

def containsKeywords(rwi):
	return  inRWI(rwi, 'excavator') or \
			pairInRWI(rwi, 'civil', 'construction') or \
			pairInRWI(rwi, 'site', 'development') or \
			pairInRWI(rwi, 'heavy', 'equipment')

def main():
	with open('data_dump.txt', 'r') as ifs, open('results.txt', 'w') as ofs:
		lines = ifs.readlines()
		i = 0
		urlcount = 0
		while i < len(lines):
			url = lines[i]
			print('#{} {}'.format(urlcount, url), end='', flush=True)
			urlcount += 1
			rwi = lines[i + 1].rstrip('\n')
			rwi = json.loads(rwi)
			for key in rwi:
				rwi[key] = set(rwi[key])
			if containsKeywords(rwi):
				ofs.write(url)
				ofs.flush()
			i += 2

if __name__ == '__main__':
	main()