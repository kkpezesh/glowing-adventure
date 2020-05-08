import json
import requests
import sys
from bs4 import BeautifulSoup

def getURL():
	if len(sys.argv) != 2:
		sys.stderr.write('usage: dl.py <url>\n')
		exit(0)
	url = sys.argv[1]
	pos = url.find('http')
	if pos == -1:
		url = 'http://{}'.format(url)
	elif pos > 0:
		sys.stderr.write('URL incorrectly formatted\n')
		exit(0)
	# else pos == 0, well formated already
	return url

def getHTML(url):
	try:
		
		res = requests.get(url, allow_redirects=True,timeout=5)
	except:
		sys.stderr.write('Failed to fetch: ' + url + '\n')
		exit(0)

	html_page = res.content
	soup = BeautifulSoup(html_page, 'html.parser')
	return soup.find_all(text=True)

def getTextList(text):
	output = ''
	blacklist = [
		'[document]',
		'noscript',
		'header',
		'html',
		'meta',
		'head', 
		'input',
		'script',
		'style'
	]
	for t in text:
		if t.parent.name not in blacklist:
			output += '{} '.format(t)
	return output.lower().split()

def getRWI(textList):
	rwi = {}
	wordPos = 0
	for word in textList:
		if word in rwi:
			rwi[word].append(wordPos)
		else:
			rwi[word] = [wordPos]
		wordPos += 1
	return rwi

def main():
	url = getURL()
	text = getHTML(url)
	textList = getTextList(text)
	rwi = getRWI(textList)
	rwiJSON = json.dumps(rwi)
	print(url)
	print(rwiJSON)

if __name__ == '__main__':
	main()