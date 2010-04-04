from sendSerial import *
from sensorData import *
import serial
import time 

#Set up
#ser = serial.Serial('/dev/arduino', 9600)
#print ser.readline()

f = open('./log/we_' + str(time.time()) , 'w')


sxml= "<sensor><compass>140</compass><flex><left>500</left><right>300</right></flex><ultrasonic><left>3</left><right>10</right></ultrasonic><beacon>???</beacon><wheelencoder><motor_a>2000</motor_a><motor_b>1998</motor_b></wheelencoder></sensor>"
sd = sensorData(sxml)
send = sendData()

motor_dir = "na"

while 1:
    f.write(str(sd.wheelencoder) + '\n')
    time.sleep(1)
