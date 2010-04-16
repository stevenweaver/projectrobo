import setup
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

    print sd.flex['left']

    #Check right side
    if sd.flex['right'] < 450:
        #Turn right 
        print "we are running against a right wall"
        ser.send(send.createXml("left"))

    elif sd.flex['right'] < 500: 
        #Turn right 
        print "we are scrapping against a right wall"
        ser.send(send.createXml("left"))

    elif sd.flex['right'] < 653:
        #Turn right 
        print "we are hitting against a right wall"
        ser.send(send.createXml("left"))

    #Check left side
    if sd.flex['left'] < 400:
        #Turn left
        print "we are running against a left wall"
        #WE might need to stop and reverse
        ser.send(send.createXml("right"))

    elif sd.flex['left'] < 450: 
        #Turn left 
        print "we are scrapping against a left wall"
        ser.send(send.createXml("right"))

    elif sd.flex['left'] < 603:
        #Turn left 
        print "we are hitting against a left wall"
        ser.send(send.createXml("right"))


    #time.sleep(.001)
    time.sleep(1)

