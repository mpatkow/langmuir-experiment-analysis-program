import sys

fname = sys.argv[1]
f = open(fname, "r")
r = f.readline()
f.close()

new_data = r.split(",")
vs = [new_data[2*i] for i in range(int(len(new_data)/2))]

for i in range(len(new_data)-1, -1, -1):
	if new_data.count(new_data[i]) > 1 and i % 2 == 0:
		del new_data[i+1]
		del new_data[i]

nd = ""
for l in new_data:
	nd += l
	nd += ","
nd = nd[:-1]	

f = open(fname + "NO_OVER", "w")
f.write(nd)
f.close()
	
	#print([j for j, n in enumerate(vs) if n == new_data[2*i]]) 
