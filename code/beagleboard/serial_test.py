import serial
import time
s = serial.Serial('/dev/ttyUSB1', 19200)
while 1:
    s.write('123456789')
    print s.readline()
