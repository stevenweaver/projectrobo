from sendSerial import *
from sensorData import *
from defines import *
import serial
import time 
import numpy as np

#we should be receiving the servo position, if it's around the same position for any length of time, we should no to move in that direction. 

#Set up
#ser = serial.Serial('/dev/arduino', 9600)
#print ser.readline()

sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>3</left><right>10</right></ultrasonic><beacon>2</beacon><wheelencoder>???</wheelencoder></sensor>"
sd = sensorData(sxml)
send = sendData()

#list of past positions
#pos = np.zeros(10)
pos = [] 

#f = open('./log/beacontest_' + str(time.time()) , 'w')

while 1:
    #sd.update(ser.readline())

    #print sd.beacon
    #f.write(str(sd.beacon) + '\n')

    pos.append(sd.beacon)
    arr = np.array(pos)
    mean = arr.mean() 
    std = arr.std()


    if mean < 85 and std < 5:
        print "beacon is on the right, turn right" 
        ser.write(send.sendStr(RIGHT))
        print ser.readline()
        #ser.send(send.sendStr(RIGHT))

    elif mean > 95 and std < 5:
        #Turn left
        print "beacon is on the left, turn left"
        ser.write(send.sendStr(LEFT))
        print ser.readline()
        #ser.send(send.sendStr(LEFT))

    elif mean > 85 and mean < 95 and std < 5:
        #Turn right 
        print "beacon is on the forward, turn forward"
        ser.write(send.sendStr(FORWARD))
        #ser.send(send.sendStr(FORWARD))

    
    if len(pos) > 10:
        del pos[0]

    #time.sleep(.001)
    time.sleep(1)
