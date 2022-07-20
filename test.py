
import pyvisa
rm = pyvisa.ResourceManager()

my_instrument = rm.open_resource('GPIB0::14::INSTR')

my_instrument.baud_rate = 19200
my_instrument.timeout = 25000
my_instrument.chunk_size = 102400
my_instrument.open()
del my_instrument.timeout

my_instrument.write('*IDN?')
while True:
    print(my_instrument.read_bytes(1))
