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
        data = data.zfill(10)
        return data 

if __name__ == '__main__':
    while(1):
        ser = serial.Serial('/dev/arduino', 9600)
        # Self-testing code goes here.
        sxml= "<?xml version=\"1.0\"?><sensor><c>256.39</c><f><l>497</l><r>400</r></f><us><l>80</l><r>79</r></us><b>87</b><we><a>2000</a><b>1998</b></we></sensor>"
        sd = sensorData(sxml)
        send = sendData()
        pis = send.sendStr(3,2000) 
        ser.write(pis)
        print ser.readline()
