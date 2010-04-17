import setup
from sendSerial import *
from sensorData import *
import serial
import time 

#Set up
ser = serial.Serial('/dev/arduino', 9600)

#while 1:
#    print ser.readline()
sxml = ""

while sxml.find('<?xml version="1.0"?>') == -1:
    sxml = ser.readline()

print sxml

sd = sensorData(sxml)

f = open('./log/compass_' + str(int(time.time())) , 'w')

while 1:
    sxml = ser.readline()
    print len(sxml)
    sd.update(sxml)
    f.write(str(sd.compass) + '\n')
    print str(sd.compass) + '\n'
