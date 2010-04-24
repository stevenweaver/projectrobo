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
x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
GoalNum = 0
coor_fix = [0,0]
Goal = distance.toDec(Goals[GoalNum])
gps_serial = serial.Serial('/dev/gps', 9600)

while(1):
    gps_data = gps_serial.readline()
    nmea = NMEA.NMEA(gps_data)
    if nmea.satellites == "00":
        print "No Satellite"
    else:
        position = [float(nmea.lat), float(nmea.lon)]
        positionA = distance.toDec(position)
        dis = distance.havDistance(Goal, positionA)
        bearing = distance.calcBearing(positionA , Goal)
        robot_Bearing = distance.calcRelBearing(bearing, 270)
        coor_position = distance.getCoor([float(nmea.lat),float(nmea.lon)])
        coor_position=[coor_position[0]+coor_fix[0],coor_position[1]+coor_fix[1]]
        if (dis < 5):
            xDiff = (x[GoalNum] - coor_position[0])
            yDiff = (y[GoalNum] - coor_position[1])
            coor_fix = [xDiff,yDiff]
            distance.coorFix([x[GoalNum],y[GoalNum]],coor_position)
            GoalNum = GoalNum+1
            Goal = distance.toDec(Goals[GoalNum])

        print nmea.satellites,"  ",GoalNum ,"  ",dis,"  ",robot_Bearing,"  ",coor_position 
