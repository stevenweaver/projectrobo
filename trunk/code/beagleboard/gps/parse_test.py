#!/usr/bin/python
import NMEA 
import distance
import serial
import time 


while(1):
    gps_serial = serial.Serial('/dev/gps', 9600)
    gps_data = gps_serial.readline()
    nmea = NMEA.NMEA(gps_data)
    print gps_data
    print nmea.lat, nmea.lon
    print nmea.time
