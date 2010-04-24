#!/usr/bin/python
import NMEA 
import distance
import serial
import time 

Goals = [[3246.6417,11704.2338],
        [3246.6428,11704.2037],
        [3246.6350,11704.1956],
        [3246.6224,11704.2317],
        [3246.6306,11704.2410]]
GoalNum = 0
Goal = distance.toDec(Goals[GoalNum])
while(1):
    gps_serial = serial.Serial('/dev/gps', 9600)
    gps_data = gps_serial.readline()
    nmea = NMEA.NMEA(gps_data)
    position = [float(nmea.lat), float(nmea.lon)]
    positionA = distance.toDec(position)
    dis = distance.havDistance(Goal, positionA)
    if (dis < 20):
        GoalNum = GoalNum+1
        Goal = distance.toDec(Goals[GoalNum])
    #if the robot is moving find the bearing 
    gps_data = gps_serial.readline()
    nmea = NMEA.NMEA(gps_data)
    position = [float(nmea.lat), float(nmea.lon)]
    positionB = distance.toDec(position)
    bearing = distance.calcBearing(positionA , Goal)
    bearing2 = distance.calcBearing(positionA , positionB)
    dirc = bearing - bearing2
    #we need compass info to find direction of Goal
    print gps_data
    print GoalNum
    print position
    print dis
    print dirc
