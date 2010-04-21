#Import the modules we need
import setup
import serial
import NMEA 
import rssi 
import distance
from defines import * 
from sendSerial import *
from sensorData import *
import numpy as np
import time

#Points we are shooting for
x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
waypoints = zip(x,y)

gps_waypoints = [[3246.6417,11704.2338],
                [3246.6428,11704.2037],
                [3246.6350,11704.1956],
                [3246.6224,11704.2317],
                [3246.6306,11704.2410]]
#initialization, our huge lists of information
sd = []
nmea = [] 
rssi = [] 
current_position = [] 
position_list = []

waypoint_count = 0
beacon_count = 0

#Set up serial connections
ard_ser = serial.Serial('/dev/arduino', 9600)
gps_ser = serial.Serial('/dev/gps', 9600)
rssi_ser = serial.Serial('/dev/rssi', 19200)

#print ser.readline()
main()

def main():
    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        updateEverything()

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        if obstacle():
            moveOutTheWay()

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.
        #Use rssi for proximity and override main path 
        elif beacon():
           goTowardsBeacon() 

        #Otherwise continue going about our way
        #wayPoint is the new calcPosition()
        elif atWaypoint():
            waypoint_count+=1
            goTowardsNewDestination()

    return

def obstacle():
    #Check if the obstacles are dangerously in the way
    if sd.us['right'] < RANGE_LIMIT or sd.us['left'] or sd.flex['left'] < LEFT_HITTING or sd.flex['right'] < RIGHT_HITTING:
        return 1

    return 0

def moveOutTheWay():
    #Check for flex first
    flex()

    #Then check for ultrasonics
    range_finders()

    return 1

def goTowardsBeacon():
    #Check if the Beacons are within range
    pos.append(sd.beacon)
    arr = np.array(pos)
    mean = arr.mean() 
    std = arr.std()

    if mean < 85 and std < 5:
        turn(right, mean)
        goDir(FORWARD)

    elif mean > 95 and std < 5:
        #Turn left
        turn(left, mean - 90)
        goDir(FORWARD)

    elif mean > 85 and mean < 95 and std < 5:
        #Turn right 
        goDir(FORWARD)

    if len(pos) > 10:
        del pos[0]

    return 1


def beaconDetect():
    if rssi[0].rx_distance() == 1:
        return 1

    return 0

def atGpsWaypoint(gw):
    updateGps()
    if nmea.satellites > 6:
        if distance.havDistance([nmea.lat,nmea.lon], gw) < 5  :
            return 1
        return 0
    return -1

def atWaypoint(wp):
    current_point = calcPosition()
    if math.hypot(current_point[0] + current_point[1]) == math.hypot(wp[0] + wp[1]):
        return 1
    return 0

def goTowardsNewDestination():
    #this gets called when we need to calculate the next stop we should go to
    #Decide how to get there
    goDir(STOP)
    current_point = calcPosition()
    
    #Find distance and bearing to next position
    distance = (current_point, next_waypoint)
    angle =(current_point, next_waypoint) 

    goFeet(distance)
    turn(angle)
    goDir(FORWARD)

    return

def calcGpsDistance(gw):
    updateGps()
    if nmea.satellites > 5:
        return distance.havDistance([nmea.lat , nmea.lon], gps_waypoint[gw])
    return -1

def calcDistance(pt1, pt2, gw):
    return  math.sqrt(math.pow((pt2[0] - pt1[0]),2)+math.pow((pt2[1] - pt1[1]), 2))
    
 
def calcAngle(pt1, pt2):
    #now we need to find angle A, since we know sinA is height/distance we can just find the inverse sine 
    distance = calcDistance(pt1, pt2)
    if abs(pt2[0] - pt1[0]) > abs(pt2[1] - pt1[1]):
        diff = pt2[1] - pt[1]
    #Else we want to calculate the difference in x
    else:
        diff = pt2[0] - pt[0] 
    #Calculate the angle
    return math.asin(diff/distance) 

    
def calcPosition():
    #we have to use dead reckoning and compass information in order to get a good idea of where we have gone
    if abs(next_waypoint[0] - last_waypoint[0]) > abs(next_waypoint[1] - last_waypoint[1]):
        rev_orientation = 0 
    else:
        rev_orientation = 1

    #we can guess at the direction we are going by just calculating the degree difference between our two points
    last_waypoint = waypoints[waypoint_count]
    next_waypoint = waypoints[waypoint_count + 1]

    #calculate the distance 
    angle = calcAngle(next_waypoint, last_waypoint)

    #TODO:
    #ok we should match that angle with the angle that we have on our compass, and take note of any inconsistencies
    #cur_compass = sd[0].compass
   
    #we know the hypotenuse is motor1_ft and we know the angle we should be going, so we should be able to estimate our point 
    #these should be more or less equal, so i'm going to use one for now
    motor1_ft = sd[0].dis_traveled['a']  
    motor2_ft = sd[0].dis_traveled['b']  

    #TODO:same deal as before
    if rev_orientation:
        delta_x = math.sin(angle) * motor1_ft
        delta_y = math.cos(angle) * motor1_ft
    else:
        delta_y = math.sin(angle) * motor1_ft
        delta_x = math.cos(angle) * motor1_ft

    current_point = ((last_waypoint[0] + delta_x),(last_waypoint[0] + delta_y))

    #TODO: 
    #check out the calculated information with the gps
    #gps
    updateGps()
    if nmea.satellites > 6:
        gps_point = distance.getCoor([nmea.lat , nmea.lon])
        current_point_hypot = math.hypot(current_point[0],current_point[1])
        gps_point_hypot = math.hypot(gps_point[0],gps_point[1])
        point_diff = math.fabs(current_point_hypot - gps_point_hypot)
        if point_diff > 20:
            current_point = gps_point
    return current_point

def goFeet(command):
    #send direction to serial port
    #97 ticks equals a foot 
    ticks = command * 97;
    ard_ser.write(send.sendStr(str(ticks) + 'T'))
    return 1

def goDir(command):
    ard_ser.write(send.sendStr(command))
    return 1

def turn(dir, degrees):
    return 1

def updateSensors():
    #Parse serial information
    #Check to make sure we have a nice string
    sxml = ard_ser.readline()
    while sxml.find('<?xml version="1.0"?>') != 0:
        sxml = ser.readline()
    sd.insert(0,sensorData(sxml))
    return

def updateGps():
    #Parse serial information
    #probably need error checking
    gps_data = gps_ser.readline()
    nmea.insert(0,NMEA(gps_data))
    return

def updateRssi():
    #Parse serial information
    #Check to make sure we have a nice string
    #probably need error checking
    rssi_data = rssi_ser.readline()
    rssi.insert(0,RSSI(rssi_data))
    return

def updateEverything():
    updateSensors()
    updateGps()
    updateRssi()
    return

#We can have this computed beforehand
def computeCourse(): 
    #every point on the course
    #not sure if we need this, maybe for timing
    for i in range(len(x) - 1):
        if abs(x[i+1] - x[i]) > abs(y[i+1] - y[i]):
            for j in range(abs(x[i+1]-x[i])):
                if x[i+1] < x[i]:
                    xc = x[i] - j
                else:
                    xc = x[i] + j
                    yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 

    else:
        for j in range(abs(y[i+1]-y[i])):
            if y[i+1] < y[i]:
                yc = y[i] - j
            else:
                yc = y[i] + j
            xc = x[i] + (yc-y[i])*(x[i+1] - x[i])/(y[i+1] - y[i]) 

def flex():
    #Flex Sensors
    #Check right side
    if sd.flex['right'] < RIGHT_HITTING:
        turn(left, 15)

    elif sd.flex['right'] < RIGHT_SCRAPPING: 
        turn(left, 45)

    elif sd.flex['right'] < RIGHT_DANGEROUS:
        goDir(STOP)
        goDir(REVERSE)
        goFeet(4)
        turn(left, 45)
        goDir(FORWARD)

    #Check left side
    elif sd.flex['left'] < LEFT_HITTING:
        turn(right, 15)

    elif sd.flex['left'] < LEFT_SCRAPPING: 
        turn(left, 45)

    elif sd.flex['left'] < LEFT_DANGEROUS:
        goDir(STOP)
        goDir(REVERSE)
        goFeet(4)
        turn(left, 45)
        goDir(FORWARD)

def range_finders():
    if sd.us['right'] < RANGE_LIMIT and sd.us['left'] < RANGE_LIMIT:
        goDir(STOP)
        turn(left, 90)
        goFeet(1)
        goDir(FORWARD)
        goDir(STOP)
        turn(right, 90)
        goDir(FORWARD)

    elif sd.us['right'] < RANGE_LIMIT:
        #Turn left a little bit, then straighten out
        turn(left, 15)
        goDir(FORWARD)

    elif sd.us['left'] < RANGE_LIMIT:
        #Turn right a little bit, then straigten out 
        turn(right, 15)
        goDir(FORWARD)
