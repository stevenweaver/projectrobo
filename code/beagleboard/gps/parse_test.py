#!/usr/bin/python
import NMEA 

nmea = NMEA.NMEA()

f = open('./gps_sample_data/4-3/1.txt', 'r+')

gps_data = f.readlines()


#for raw in gps_data:
print nmea.handle_line(gps_data[0].lstrip('"'))
