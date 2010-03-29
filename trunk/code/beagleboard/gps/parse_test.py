#!/usr/bin/python
import NMEA 
import serial
import time 

nmea = NMEA.NMEA()

while(1):
    gps_serial = serial.Serial('/dev/ttyUSB0', 9600)
    gps_data = gps_serial.readline()
    nmea.handle_line(gps_data)
    print nmea.lat, nmea.lon
    print nmea.time
