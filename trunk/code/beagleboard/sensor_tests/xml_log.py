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

while len(sxml) < 100:
    sxml = ser.readline()

print sxml

sd = sensorData(sxml)

f = open('./log/xml_' + str(int(time.time())) , 'w')

while 1:
    sxml = ser.readline()
    f.write(sxml + '\n')
    print sxml
