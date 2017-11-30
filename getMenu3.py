# 23 Nov 2017
# extract origin restaurant info from vivacity API
# Install HTTrack: 
# sudo apt-get install httrack
# And you will need to have wget and lynx installed:
# sudo apt-get install wget lynx
# sudo apt-get install python3-bs4

from urllib import request
from urllib.parse import quote, unquote
import urllib3
import re
import os
import json
from vivacityList import restaurantList
from vivacityDetail import restaurantDetail
from random import shuffle

class WebsiteDownloader:

	def __init__(self):
		self.listIndex = 0
		self.user_agent = 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52'
		self.endpoint = 'https://www.google.co.uk/search?q=restaurant+'
		self.url = ''
		self.headers = {
			'User-Agent' : self.user_agent,
		}

	# To get the whole page
	def getPage(self, name):
		lists = name.split('_')
		list = ''
		for l in lists:
			isascii = lambda l: len(l) == len(l.encode())
			if not isascii(l):
				l = quote(l)
				# print(l)
			list += l + '+'

		self.url = self.endpoint + list.strip('+')
		http = urllib3.PoolManager()
		r = http.request('GET', self.url, headers = self.headers)
		page = r.data.decode('utf-8')
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
		self.id = ''
		self.folder_name = ''
		self.cwd = os.getcwd()
		self.directDownloadNum = 0
		self.listIndex = 0

	def webpageDownload(self):
		files_folder_name = self.folder_name + 'Menu-' + self.name + '_files/'
		if not os.path.exists(files_folder_name):
		    os.makedirs(files_folder_name)
		os.chdir(files_folder_name)
		os.system('httrack --depth=1 ' + self.url + ' -s0')
		os.chdir(self.folder_name)
		os.system('ln -sf ' + 'Menu-' + self.name + '_files/index.html Menu-' + self.name)


	def directDownload(self):
		os.system("wget -r --level 0 -nH -nd -A '*.pdf' %s -e robots=off -U mozilla --random-wait -P %s" % (self.url, self.folder_name))

	def prepareFolder(self):
		self.folder_name = self.cwd + '/Menus/%s_%s/' % (self.id, self.name)
		if not os.path.exists(self.folder_name):
		    os.makedirs(self.folder_name)


if __name__ == "__main__":
	
	# city = 'London'
	city = 'Edinburgh'
	limit = '10'

	menuDownloader = MenuDownloader()
	webpageDownloader = WebsiteDownloader()
	
	# get lists of restaurant
	# restaurantListAPI = restaurantList(limit, city)
	# restaurant = restaurantListAPI.extract()

	# get one specific restaurant
	id = '583a5a2824e2ccd022eeb9c0'
	restaurantDetailAPI = restaurantDetail(id)
	restaurant = restaurantDetailAPI.extract()

	# shuffle(restaurant)
	# print(restaurant)

	print(str(len(restaurant)) + ' restaurants in ' + city)

	urlRecord = open('Menus/urlRecord.csv','w')
	urlRecord.write("%s,%s,%s,%s\n" % ('note', 'id', 'name', 'url'))

	for l in restaurant:
		
		menuDownloader.listIndex += 1

		# if menuDownloader.listIndex > 5:
			# continue

		menuDownloader.name = l[1]
		menuDownloader.name = ''.join([i for i in menuDownloader.name if i.isalpha() or i==' ' or i.isdigit()]).replace(' ','_')
		menuDownloader.id = l[0]
		menuDownloader.url = l[2]
		
		if menuDownloader.url is not None:
			print(str(menuDownloader.listIndex) + ': ' + menuDownloader.name)			
			menuDownloader.prepareFolder()
			urlRecord.write("%s,%s,%s,%s\n" % ('Existing', menuDownloader.id, menuDownloader.name, menuDownloader.url))
		else:
			page = webpageDownloader.getPage(menuDownloader.name)
			website = webpageDownloader.getWebsite(page)
			if website:
				print(str(menuDownloader.listIndex) + ': ' + website[0])
				menuDownloader.url = website[0]
				menuDownloader.prepareFolder()
				urlRecord.write("%s,%s,%s,%s\n" % ('Added', menuDownloader.id, menuDownloader.name, menuDownloader.url))
			else:
				print(str(menuDownloader.listIndex) + ': ' + 'Failed find url!')
				urlRecord.write("%s,%s,%s,%s\n" % ('Not Found', menuDownloader.id, menuDownloader.name, ''))
		
		try:
			menuDownloader.directDownload()
			menuDownloader.directDownloadNum += 1
		except Exception as e:
			print(e)
		
		# if not os.listdir(menuDownloader.folder_name):
		# 	menuDownloader.webpageDownload()

		# break

	urlRecord.close()

	print('OK\n' + '='*50 + '\n')
	# print('Num of Directly Downloaded PDF files: ' + str(menuDownloader.directDownloadNum))
