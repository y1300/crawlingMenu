
#  Install HTTrack: 
# sudo apt-get install httrack
# And you will need to have wget and lynx installed:
# sudo apt-get install wget lynx

from urllib import request
from urllib.parse import quote, unquote
import urllib3
import re
import os
import json

class Website:

	def __init__(self):
		self.listIndex = 0
		self.user_agent = 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'
		self.endpoint = 'https://www.google.co.uk/search?q=restaurant+'
		self.url = ''
		# self.referer = self.url
		self.headers = {
			'User-Agent' : self.user_agent,
			# 'Referer' : self.referer, 
			# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, image/webp, */*;q=0.8',
			# 'Accept-Language': "en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
			# 'Accept-Encoding' : 'gzip, deflate, br',
			# 'Connection' : 'close',
			# 'Content-Type' : 'text/html; charset=utf-8'
		}

	# To get the whole page
	def getPage(self,list):
		lists = list.split(' ')
		list = ''
		for l in lists:
			isascii = lambda l: len(l) == len(l.encode())
			if not isascii(l):
				l = quote(l)
				# print(l)
			list += l + '+'

		self.url = self.endpoint + list.strip('+')
		# print(self.url)
		http = urllib3.PoolManager()
		r = http.request('GET', self.url, headers = self.headers)
		page = r.data.decode('utf-8')
		# print(page)
		# request = urllib2.Request(url='http://www.google.com', data = None, headers = self.headers) #self.url
		# response = urllib2.urlopen(request)
		# page = response.read()
		return page

			
	def getWebsite(self,page):
		pattern = re.compile('href="http://www.google.co.uk/url\?url=(.*?)&amp.*?Website')
		website = re.findall(pattern, page)
		return website

class MenuDownloader:
	def __init__(self):
		self.link = []
		self.url = ''
		self.name = ''
		# self.file_name = ''
		self.folder_name = ''
		self.cwd = os.getcwd()
		self.directDownloadNum = 0
		self.listIndex = 0
		# print(self.cwd)

	def webpageDownload(self):
		files_folder_name = self.folder_name + 'Menu-' + self.name + '_files/'
		if not os.path.exists(files_folder_name):
		    os.makedirs(files_folder_name)
		os.chdir(files_folder_name)
		# print(os.getcwd())
		os.system('httrack --depth=1 ' + self.url + ' -s0')
		# os.system('cd ..')
		os.chdir(self.folder_name)
		os.system('ln -sf ' + 'Menu-' + self.name + '_files/index.html Menu-' + self.name)


	def directDownload(self):
		# print(self.url)
		# print(self.file_name)
		# request.urlretrieve(self.url, self.file_name)
		os.system("wget -r -np -nH -nd -A '*.pdf' %s -e robots=off --spider -U mozilla --random-wait -P %s" % (self.url, self.folder_name))
		# os.system('''lynx -cache=0 -dump -listonly %s | grep ".*\.pdf$" | awk '{print $2}' | tee pdflinks.txt''' % self.url)

	def prepareFolder(self, url, name):
		self.url = url
		self.name = name
		self.name = ''.join([i for i in self.name if i.isalpha() or i==' ' or i.isdigit()]).replace(' ','_')
		self.folder_name = self.cwd + '/Menus/%s_%s/' % (self.listIndex, self.name)
		# self.file_name = self.folder_name + '%s.pdf' % self.name
		if not os.path.exists(self.folder_name):
		    os.makedirs(self.folder_name)


if __name__ == "__main__":
	self = MenuDownloader()
	spider = Website()

	data = json.load(open('restaurantURL.json'))

	for l in data['list']:
		
		self.listIndex += 1

		if self.listIndex > 1:
			break

		try:
			# url = l['socialMedia']['url']
			url = 'http://www.1lombardstreet.com/the-brasserie'
			name = l['name']
			print(str(self.listIndex) + ': ' + self.name)			
			self.prepareFolder(url, name)
		except:
			page = spider.getPage(l['name'])
			website = spider.getWebsite(page)
			if website:
				print(str(self.listIndex) + ': ' + website[0])
				self.prepareFolder(website[0], l['name'])
			else:
				print('Failed find url!')
		
		try:
			self.directDownload()
			self.directDownloadNum += 1
		except Exception as e:
			print(e)
		
		if not os.listdir(self.folder_name):
			self.webpageDownload()

		# break


	print('OK' + '='*50 + '\n')
	# print('Num of Directly Downloaded PDF files: ' + str(self.directDownloadNum))
