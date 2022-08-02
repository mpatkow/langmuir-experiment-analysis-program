import sys

f = open(sys.argv[1], "r")
r = f.readline()
f.close()

r = r.split(",")

f = open(sys.argv[1], "w")

new_data = ""

for i in range(int(len(r)/2)):
	new_data += r[2*i]
	new_data += "\t"
	new_data += r[2*i+1]
	new_data += "\n"

f.write(new_data)
f.close()
