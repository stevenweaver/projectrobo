from sensorData import *
from defines import *
import serial
import time

#Data to send:
## stop, forward, reverse, left, right
#<direction>right,left,forward,reverse</direction>

def sendStr(command):
    data = str(command)
    #data += "\n"
    data = data.zfill(10)
    return data 

if __name__ == '__main__':
    ser = serial.Serial('/dev/babyarduino', 9600)
    # Self-testing code goes here.
    sxml= "<?xml version=\"1.0\"?><sensor><c>256.39</c><f><l>497</l><r>400</r></f><us><l>80</l><r>79</r></us><b>87</b><we><a>2000</a><b>1998</b></we></sensor>"
    sd = sensorData(sxml)
    send = sendData()

    time.sleep(1)
    ser.write(send.sendStr(STOP))

    time.sleep(1)

    ser.write(send.sendStr(LEFT))
    print ser.readline()
    time.sleep(1)

    ser.write(send.sendStr("5000T"))
    print ser.readline()
    time.sleep(10)

    ser.write(send.sendStr(STOP))
    print ser.readline()
    time.sleep(1)

    ser.write(send.sendStr(RIGHT))
    print ser.readline()
    time.sleep(1)

    ser.write(send.sendStr("3000T"))
    print ser.readline()
    time.sleep(5)

    ser.write(send.sendStr(FORWARD))
    print ser.readline()
    time.sleep(1)

    ser.write(send.sendStr("10000T"))
    print ser.readline()
    time.sleep(10)


    ser.write(send.sendStr(STOP))
    print ser.readline()
