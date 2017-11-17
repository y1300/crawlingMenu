
#  Install HTTrack: sudo apt-get install httrack

from urllib import request
import os 
# import pdfkit

class MenuDownloader:
	def __init__(self):
		self.link = []
		self.url = ''
		self.name = ''
		self.file_name = ''
		self.folder_name = ''
		self.cwd = os.getcwd()
		self.directDownloadNum = 0
		self.listIndex = 0
		# print(self.cwd)

	def webpageDownload(self):
		# pdfkit.from_url(self.url, self.file_name)
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
		request.urlretrieve(self.url, self.file_name)

if __name__ == "__main__":
	self = MenuDownloader()

	f = open('website.txt','r')
	l = f.readline()

	while l:
		self.listIndex += 1
		self.link = l.split('*')
		self.url = self.link[3].strip('\n')
		self.name = self.link[2]
		self.name = ''.join([i for i in self.name if i.isalpha() or i==' ']).replace(' ','_')
		self.folder_name = self.cwd + '/Menus/%s_%s_%s/' % (self.link[0], self.link[1], self.name)
		self.file_name = self.folder_name + '%s.pdf' % self.name
		print(str(self.listIndex) + ': ' + self.name)

		if not os.path.exists(self.folder_name):
		    os.makedirs(self.folder_name)


		if l[-4:-1] == 'pdf':
			try:
				self.directDownload()
				self.directDownloadNum += 1
			except Exception as e:
				print(e)
				self.webpageDownload()
		else:
			self.webpageDownload()

		l = f.readline()

	f.close()
	print('OK' + '='*50 + '\n')
	print('Num of Directly Downloaded PDF files: ' + str(self.directDownloadNum))
