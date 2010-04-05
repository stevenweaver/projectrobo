from xml.dom.minidom import Document
from sensorData import *
import serial
import time

#Data to send:
## stop, forward, reverse, left, right
#<direction>right,left,forward,reverse</direction>

class sendData:
    def sendStr(self, direction, ticks):
        data = str(direction)
        data += ","
        data += str(ticks) 
        data += "\n"
        data = data.zfill(9)
        return data 

if __name__ == '__main__':
    while(1):
        ser = serial.Serial('/dev/arduino', 9600)
        # Self-testing code goes here.
        sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>10</left><right>10</right></ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"
        sd = sensorData(sxml)
        send = sendData()
        ser.write(send.sendStr(3,200))
        print ser.readline()
