#Import the modules we need
import setup
import motor
import avoidance
import beacon
import compass
import path_find
import comm
from defines import * 
#import numpy as np
import time

#main loop 
def main():
    #initialization, our huge lists of information
    ser = comm.comm()
    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    pf = path_find.pathFind()

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    #while(1):
    for i in range(1000):
        sensor_data.insert(0,ser.updateSensors())
        #gps_list.insert(0,ser.updateGps())
        #rssi_list.insert(0,ser.updateRssi())

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        #if avoidance.obstacle(sensor_data[0]) == 1:
        #    print i
        #    avoidance.moveOutTheWay(sensor_data[0])

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.
        #Use rssi for proximity and override main path, this needs to send the whole list instead of just one 
        #if beacon.beaconDetect(rssi_list[0]):
        #   beacon.goTowardsBeacon(sensor_data[0]) 

        #Check if we're veering left or right
        if len(sensor_data) > 10:
            print sensor_data[0].compass 
            if compass.checkCompass(sensor_data[0].compass,sensor_data[0:10]):
                print "compass_moving"

        #Otherwise continue going about our way
        #wayPoint is the new calcPosition()
        #if pf.atWaypoint(sensor_data):
            #pf.waypoint_count+=1
            #pf.goTowardsNewDestination()

        #time.sleep(.02)
    return

main()
