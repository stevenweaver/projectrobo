import serial
import time 

while(1):
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    print ser.readline()
    #time.sleep(1)
    
