from sendSerial import *
from sensorData import *
import serial
import time 

#Set up
#ser = serial.Serial('/dev/arduino', 9600)
#print ser.readline()

sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>3</left><right>10</right></ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"
sd = sensorData(sxml)
send = sendData()

while 1:
    #sd.update(ser.readline())

    print sd.us['left']

    if sd.us['right'] < 5 and sd.us['right'] < 5:
        print "getting close to something so stop" 
        ser.send(send.createXml("stop"))

    elif sd.us['right'] < 5:
        #Turn left
        print "something is on the right"
        ser.send(send.createXml("left"))

    elif sd.us['left'] < 5:
        #Turn right 
        print "something is on the left"
        ser.send(send.createXml("right"))

    #time.sleep(.001)
    time.sleep(1)

