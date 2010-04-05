import serial
import time
s = serial.Serial('/dev/arduino', 9600)
while 1:
    s.write('123456789')
    print s.readline()
