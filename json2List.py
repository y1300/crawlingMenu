o = open("restaurantURL.json")
f=o.readline()

out = open("list.txt",'w+')

for i in range(0, 1777):
    # print(f[0:5])
    if f[0:5]=='"name':
        print f
        out.write(f[10:-2] + '\n')
    f=o.readline()

o.close()