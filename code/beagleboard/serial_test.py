import serial
import time 

while(1):
    ser = serial.Serial('/dev/arduino', 9600)
    print ser.readline()
    #time.sleep(1)
    
