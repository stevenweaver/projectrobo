#!/usr/bin/python
import rssi 
import serial
import time 

ser = serial.Serial('/dev/rssi', 19200)
while 1:
    rssi_data = ser.readline()
    rssi_d = rssi.RSSI(rssi_data) 
    rssi.handle_line()
    print rssi_d.RxNumber
    print rssi_d.RxRSSI
    print rssi_d.distance
    print rssi_d.rx_distance()
