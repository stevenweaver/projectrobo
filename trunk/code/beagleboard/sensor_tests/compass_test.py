from sendSerial import *
:q
:q
from sensorData import *
import serial
import time 

#Set up
#ser = serial.Serial('/dev/arduino', 9600)
#print ser.readline()

sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>3</left><right>10</right></ultrasonic><beacon>2</beacon><wheelencoder>???</wheelencoder></sensor>"
sd = sensorData(sxml)
send = sendData()

motor_dir = "na"

while 1:
    print sd.compass

    #keep turning right until we are facing north
    if sd.compass is 0:
        ser.send(send.createXml("stop"))
    else:
        print "going right"
        if motor_dir != "right":
            motor_dir = "right"
            #ser.send(send.createXml(motor_dir))

    #time.sleep(.001)
    time.sleep(1)
