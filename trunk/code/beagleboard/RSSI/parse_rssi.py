#!/usr/bin/python
import rssi 
import serial
import time 

rssi = rssi.RSSI()
ser = serial.Serial('/dev/rssi', 19200)
while 1:
    rssi_data = ser.readline()
    rssi.handle_line(rssi_data)
    print rssi.RxNumber
    print rssi.RxRSSI
    print rssi.distance
    print rssi.rx_distance()
