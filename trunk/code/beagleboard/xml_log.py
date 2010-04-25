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

#Parse serial information
#Check to make sure we have a nice string
sxml = ser.readline()
while sxml.find('<?xml version="1.0"?>') != 0:
    sxml = ser.readline()

print sxml

f = open(setup.HOME + '/log/xml_' + str(int(time.time())) , 'w')
h = open(setup.HOME + '/log/xml_sensors_' + str(int(time.time())) , 'w')

while 1:
    sxml = ser.readline()
    sd = sensorData(sxml)
    f.write(sxml + '\n')

    h.write("right flex: " + str(sd.flex['right']) +'\n')

    h.write("left flex: " + str(sd.flex['left']) +'\n')

    h.write("right ultrasonic: " + str(sd.us['right']) +'\n')
    h.write("left ultrasonic: " + str(sd.us['left']) +'\n')
    #print sxml
