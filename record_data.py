import time
import pyvisa
import os
from matplotlib import pyplot as plt
import numpy as np

# When Keithley sends terminator, quit reading
terminator = '\n'

# Keithley can only store up to 80 data points per set. We use 75 to not deal with any OBOEs :D 
# was -50,60,11,75
starting_voltage = 	 -50 	# Sweep start and end values normally at -50 
ending_voltage   = 	 60	
divisions        =	 11 	# The higher this number is, the closer together and more data points, but longer run time
n_sec = 60
max_curr = 0.005

starting_voltages = []
ending_voltages = []

for i in range(divisions):
	starting_voltages.append(int(starting_voltage + (ending_voltage-starting_voltage)/(divisions) * i))
	ending_voltages.append(int(starting_voltage + (ending_voltage-starting_voltage)/(divisions) * (i+1))+2)


# EXPERIMENTAL TODO
#starting_voltages = [-5,5,15,25,35,45,55]
#ending_voltages = [10,20,30,40,50,60,70]
#divisions = 7

# Make a new file with name sample<#+1> 
i = 0
while os.path.exists("sample%s.txt" % i):
	i += 1
fname = "sample%sR.txt" % i
f = open(fname, "a")


for loop_num in range(divisions):
	rm = pyvisa.ResourceManager()
	intr = rm.open_resource('ASRL/dev/cu.usbserial-1410::INSTR')
	intr.baud_rate = 9600 
	intr.timeout = 25000
	intr.chunk_size = 102400
	intr.open()
	intr.read_termination = terminator
	intr.write_termination = terminator
	del intr.timeout
	

	starting_voltage = starting_voltages[loop_num]
	ending_voltage = ending_voltages[loop_num]
	incrs = (ending_voltage-starting_voltage)/n_sec
	intr.write(":*RST")
	intr.write(":*ESE 0")
	intr.write(":*CLS")
	intr.write(":STAT:MEAS:ENAB 1024")
	intr.write(":*SRE 1")

	intr.write(":TRAC:CLE")
	intr.write(":TRAC:POIN %i" % (n_sec+1)) ##### FIX THIS

	intr.write(":SOUR:FUNC:MODE VOLT")
	intr.write(":SOUR:VOLT:STAR %i " % starting_voltage)
	intr.write(":SOUR:VOLT:STOP %i " % ending_voltage)
	intr.write(":SOUR:VOLT:STEP %f " % incrs)

	intr.write(":SOUR:CLE:AUTO ON")
	intr.write(":SOUR:VOLT:MODE SWE")
	intr.write(":SOUR:SWE:spac lin")
	intr.write(":sour:del:auto off")
	intr.write(":SOUR:DEL 0.10")

	intr.write(":SENS:FUNC 'CURR'")
	intr.write(":SENS:FUNC:CONC ON")
	intr.write(":SENS:CURR:RANG:AUTO ON")

	intr.write(":SENS:CURR:PROT:LEV %f" % max_curr)

	intr.write(":SENS:CURR:NPLC 1")
	intr.write(":FORM:ELEM:SENS VOLT,CURR")
	intr.write(":TRIG:COUN %i" % (n_sec+1))
	intr.write(":TRIG:DEL 0.01")
	intr.write(":SYST:AZER:STAT OFF")
	intr.write(":SYST:TIME:RES:AUTO ON")
	intr.write(":TRAC:TST:FORM ABS")
	intr.write(":TRAC:FEED:CONT NEXT")
	intr.write(":OUTP ON")
	intr.write(":INIT")

	# TRY REDUCING THIS TODO
	
	time.sleep(6)

	intr.write(":TRAC:DATA?")

	# Store the results in a new file

	time.sleep(1)

	while True:
		try:
			charr = intr.read_bytes(1).decode(encoding="utf-8")
		except:
			break
		f.write(charr)
		if charr == terminator or charr == "\r" or charr == "^M":
			break

	intr.write(":*RST")
	intr.write(":*CLS")
	intr.write(":*SRE 0")

	intr.close()

f.close()

# Now we implement the fixing of the data, which is currently stored raw in a file.

f = open(fname, "r")
vi_data = f.readlines()
f.close()

# Each element of the vi_data is a string. Take off the last character of the string (a terminator), and append a comma.
new_data = ""
for d in vi_data:
	new_data += d[:-1]
	new_data += ","

new_data = new_data[:-1] # Remove extra comma at the end

f = open("sample%s.txt" % i, "w")
f.write(new_data)
os.remove(fname)
