from xml.dom.minidom import Document
from sensorData import *
import serial
import time

#Data to send:
## stop, forward, reverse, left, right
#<direction>right,left,forward,reverse</direction>

class sendData:
    def sendStr(self, direction, ticks):
        data = "d"
        data += str(direction)
        data += "d"
        data += "t"
        data += str(ticks) 
        data += "t"
        data += "\n"
        return data 

if __name__ == '__main__':
    while(1):
        ser = serial.Serial('/dev/arduino', 9600)
        #Beacon Constants
        NA = -1
        STRAIGHT = 0
        LEFT = 1
        RIGHT = 2
        STOP = 3

        # Self-testing code goes here.
        sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>10</left><right>10</right></ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"
        sd = sensorData(sxml)
        send = sendData()
        print send.sendStr(3,200)        
        print len(send.sendStr(3,200)) 
        #quit()
        #print ser.readline()
        #ser.write(send.sendStr(3,200))
        ser.write("stupid")
        print ser.readline()
