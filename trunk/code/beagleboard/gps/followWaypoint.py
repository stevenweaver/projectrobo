#!/usr/bin/python
import NMEA 
import distance
import serial
import time 

Goals = [[3246.6420,11704.2315],
        [3246.6420,11704.2035],
        [3246.6273,11704.1990],
        [3246.6255,11704.2302],
        [3246.6204,11704.2400],
        [3246.6396,11704.2527]]
x = [125, 256, 291,95,61 ]
y = [167, 167, 72,66,20]
GoalNum = 0
coor_fix = [0,0]
Goal = distance.toDec(Goals[GoalNum])


while(1):
    gps_serial = serial.Serial('/dev/gps', 9600)
    gps_data = gps_serial.readline()
    nmea = NMEA.NMEA(gps_data)
    if nmea.satellites == "00":
        print "No Satellite"
    else:
        position = [float(nmea.lat), float(nmea.lon)]
        positionA = distance.toDec(position)
        dis = distance.havDistance(Goal, positionA)
        if (dis < 5):
            xDiff = (x[GoalNum] - coor_position[0])
            yDiff = (y[GoalNum] - coor_position[1])
            coor_fix = [xDiff,yDiff]
            GoalNum = GoalNum +1
            Goal = distance.toDec(Goals[GoalNum])
            gps_data = gps_serial.readline()
            nmea = NMEA.NMEA(gps_data)
            position = [float(nmea.lat), float(nmea.lon)]
            positionA = distance.toDec(position)
            dis = distance.havDistance(Goal, positionA)
        bearing = distance.calcBearing(positionA , Goal)
        robot_Bearing = distance.calcRelBearing(bearing, 270)
        coor_position = distance.getCoor([float(nmea.lat),float(nmea.lon)])
        coor_position=[coor_position[0]+coor_fix[0],coor_position[1]+coor_fix[1]]
        print nmea.satellites,"  ",GoalNum ,"  ",dis,"  ",robot_Bearing,"  ",coor_position ,"  ", position