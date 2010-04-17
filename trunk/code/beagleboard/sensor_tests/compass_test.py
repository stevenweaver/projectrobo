import setup
from sendSerial import *
from sensorData import *
from defines import * 
import serial
import time 

#Set up
f = open('./log/compass_' + str(int(time.time())) , 'w')
ser = serial.Serial('/dev/arduino', 9600)
send = sendData()
toturn = 180
sxml = ""

while sxml.find('<?xml version="1.0"?>') == -1:
    sxml = ser.readline()

sd = sensorData(sxml)
start_compass = sd.compass
motor_dir = "na"

des_compass = (start_compass + 90) % 360
f.write('des_compass' +  str(des_compass) + '\n')
print des_compass

#ser.write(send.sendStr(RIGHT))
#ser.write("1T")

while 1:
    sxml = ser.readline()
    print sxml
    sd.update(sxml)
    print sd.compass

    diff = des_compass - sd.compass
    print diff
    f.write('diff = ' + str(diff) + ' current: ' + str(sd.compass) + '\n')

    #keep turning right until we are facing north
    if (abs(diff)-360)%360 < 10:
        print "hit it"
        #ser.write(send.sendStr(STOP))
    #time.sleep(.001)
