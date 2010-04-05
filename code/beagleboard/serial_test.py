import serial
import time 

while(1):
    ser = serial.Serial('/dev/arduino', 9600)
    ser.write("hello")
    ser.write("hello")
    ser.write("hello")
    ser.write("hello")
    ser.write("hello")
    se.write("hello")
    time.sleep(1)
    print ser.readline()
    time.sleep(1)
    
