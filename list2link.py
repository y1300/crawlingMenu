i = open("list.txt",'r', encoding='utf-8')
o = open("link.txt",'w', encoding='utf-8')

name = i.readline()
while name:
	o.write('https://www.google.co.uk/search?q=' + name.replace(' ','+').strip('\n') + '/\n')
	name = i.readline()

o.close()
i.close()