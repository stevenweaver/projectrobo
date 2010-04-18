#Import the modules we need
import setup
import serial
import NMEA 
import RSSI
from defines import * 
from sendSerial import *
from sensorData import *
import numpy as np
import time

#Points we are shooting for
x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
waypoints = zip(x,y)

#initialization, our huge lists of information
sd = []
nmea = [] 
rssi = [] 
current_position = [] 
position_list = []

waypoint_count = 0

#Set up serial connections
ard_ser = serial.Serial('/dev/arduino', 9600)
gps_ser = serial.Serial('/dev/gps', 9600)
rssi_ser = serial.Serial('/dev/rssi', 19200)

#print ser.readline()
#We're going to "package" all of the sensor data and send it in clumps over the serial.

main()

def main():
    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        #This whole function desperately needs more thinking
        
        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        isObstacle = calcObstacles()
        #if isObstacle:

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.

        #Check Directions
        #if calcNextPosition==calcPosition goto: calcDirection

        #Based on the above curricula, we should have a direction we need to go in by now
        #setDirection()

    return

def calcObstacles():
    #Check if the obstacles are dangerously in the way
    #Ultrasonic Sensors

    if sd.us['right'] < 5 and sd.us['right'] < 5:
        print "getting close to something so stop" 

    elif sd.us['right'] < 5:
        #Turn left
        print "something is a smigeon on the right"

    elif sd.us['left'] < 5:
        #Turn right 
        print "something is a smigeon to the left"

    #Flex Sensors

    #Check right side
    if sd.flex['right'] < 450:
        #Turn right 
        print "we are running against a right wall"

    elif sd.flex['right'] < 500: 
        #Turn right 
        print "we are scrapping against a right wall"

    elif sd.flex['right'] < 653:
        #Turn right 
        print "we are hitting against a right wall"

    #Check left side
    if sd.flex['left'] < 400:
        #Turn left
        print "we are running against a left wall"
        #WE might need to stop and reverse

    elif sd.flex['left'] < 450: 
        #Turn left 
        print "we are scrapping against a left wall"

    elif sd.flex['left'] < 603:
        #Turn left 
        print "we are hitting against a left wall"

    return 0

def calcBeacons():
    #Check if the Beacons are within range
    pos.append(sd.beacon)
    arr = np.array(pos)
    mean = arr.mean() 
    std = arr.std()

    if mean < 85 and std < 5:
        print "beacon is on the right, turn right" 

    elif mean > 95 and std < 5:
        #Turn left
        print "beacon is on the left, turn left"

    elif mean > 85 and mean < 95 and std < 5:
        #Turn right 
        print "beacon is on the forward, turn forward"

    if len(pos) > 10:
        del pos[0]

def calcDirection():
    #this gets called when we need to calculate the next stop we should go to
    #Decide how to get there
    return
 
def calcPosition():
    #we have to use dead reckoning and compass information in order to get a good idea of where we have gone

    #we can guess at the direction we are going by just calculating the degree difference between our two points
    last_waypoint = waypoints(waypoint_count)
    next_waypoint = waypoints(waypoint_count + 1)

    #calculate the distance 
    distance = math.sqrt(math.pow((next_waypoint[0] - last_waypoint[0]),2)+math.pow((next_waypoint[1] - last_waypoint[1]), 2)
    
    #now we need to find angle A, since we know sinA is height/distance we can just find the inverse sine 
    diff_y = next_waypoint[1] - last_waypoint[1]

    #TODO:
    #this angle needs figured out more, diff_y might not always be the arc_sin but rather the arc_cos OTZ
    angle = math.asin(diff_y/distance) 

    #TODO:
    #ok we should match that angle with the angle that we have on our compass, and take note of any inconsistencies
    #cur_compass = sd[0].compass

   
    
    #we know the hypotenuse is motor1_ft and we know the angle we should be going, so we should be able to estimate our point 
    #these should be more or less equal, so i'm going to use one for now
    motor1_ft = sd[0].dis_traveled['a']  
    motor2_ft = sd[0].dis_traveled['b']  

    #TODO:same deal as before
    delta_y = math.sin(angle) * motor1_ft
    delta_x = math.cos(angle) * motor1_ft
    
    current_point = ((last_waypoint[0] + delta_x),(last_waypoint[0] + delta_y))

    #TODO: Check to see if the current_point is greater than the next point, if so then we should increment waypoint_count
   
    #TODO: 
    #check out the calculated information with the gps
    #gps

    return

def setDirection(command, type):
    #send direction to serial port
    if type == "feet"
        #97 ticks equals a foot 
        ticks = command * 97;
        ard_ser.write(send.sendStr(str(ticks) + 'T')

    elif type == "direction"
        ard_ser.write(send.sendStr(command))

    return

def updateSensors():
    #Parse serial information

    #Check to make sure we have a nice string
    sxml = ard_ser.readline()
    while sxml.find('<?xml version="1.0"?>') not 0:
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
