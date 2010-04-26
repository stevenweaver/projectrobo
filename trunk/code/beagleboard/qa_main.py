#Import the modules we need
import setup
import motor
import avoidance
import beacon
import path_find
import comm
from defines import * 
import numpy as np
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
    while(1):
        tmp_data = 0
        while tmp_data == 0:
            tmp_data = ser.updateSensors()

        sensor_data.insert(0,tmp_data)

        #gps_list.insert(0,ser.updateGps())
        #rssi_list.insert(0,ser.updateRssi())

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        if avoidance.obstacle(sensor_data[0]):
            avoidance.moveOutTheWay(sensor_data[0])

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.
        #Use rssi for proximity and override main path, this needs to send the whole list instead of just one 
        #if beacon.beaconDetect(rssi_list[0]):
        #   beacon.goTowardsBeacon(sensor_data[0]) 

        #Otherwise continue going about our way
        #wayPoint is the new calcPosition()
        #if pf.atWaypoint(sensor_data):
            #pf.waypoint_count+=1
            #pf.goTowardsNewDestination()

        time.sleep(.02)
    return

main()
