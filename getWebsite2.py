# Crawling restaurants' websites

from urllib.parse import quote, unquote
import urllib3

import re

url = 'https://www.google.co.uk/search?q=restaurant+'


class Website:

	def __init__(self):
		self.listIndex = 0
		self.user_agent = 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'
		self.url = url
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

		self.url = url + list.strip('+')
		# print(self.url)
		http = urllib3.PoolManager()
		r = http.request('GET', self.url, headers = self.headers)
		# pageCode = r.data
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


if __name__ == "__main__":

	spider = Website()
	f = open('list.txt','r',encoding='utf-8')
	f2 = open('website.txt','w',encoding='utf-8')
	l = f.readline()
	

	# for li in l:
	websiteIndex = 0
	while l:
		spider.listIndex += 1
		page = spider.getPage(l)

		website = spider.getWebsite(page)
		if website:
			print(str(spider.listIndex) + '. ' + website[0])
			websiteIndex += 1
			f2.write(str(websiteIndex) + '*' + str(spider.listIndex) + '*' + l.strip('\n') + '*' + unquote(('').join(website[0])) + '\n')
		# f2.writelines(page)

		l = f.readline()
		# website = spider.getwebsite(page)
		# f2.write(str(page))
		# f2.write('%d. ' % (spider.listIndex) + li + '\n')
		

		time.sleep( 3 + random.uniform(-1,1) )
	

	f.close()
	f2.close()

