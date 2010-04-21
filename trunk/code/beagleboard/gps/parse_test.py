#!/usr/bin/python
import NMEA 
import distance
import serial
#import time 



while(1):
    #gps_serial = serial.Serial('/dev/gps', 9600)
    gps_serial = serial.Serial('COM13', 9600)
    gps_data = gps_serial.readline()
<<<<<<< .mine
    nmea = NMEA.NMEA(gps_data)
=======
    nmea = NMEA.NMEA(gps_data)
    print gps_data
>>>>>>> .r196
    print nmea.lat, nmea.lon
    print nmea.time
