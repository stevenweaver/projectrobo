#Import the modules we need
import setup
import comm
import motor
import avoidance
import beacon
import path_find
from defines import * 
import numpy as np
import time


#main loop 
def main():
    #initialization, our huge lists of information
    ser = comm.comm()
    sd = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        sd.insert(0,ser.updateSensors())
        gps_list.insert(0,ser.updateGps())
        rssi_list.insert(0,ser.updateRssi())

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        if avoidance.obstacle(sd[0]):
            avoidance.moveOutTheWay(sd[0])

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.
        #Use rssi for proximity and override main path, this needs to send the whole list instead of just one 
        elif beacon.beaconDetect(rssi_list[0]):
           beacon.goTowardsBeacon(sd[0]) 

        #Otherwise continue going about our way
        #wayPoint is the new calcPosition()
        elif pathFind.atWaypoint():
            pathFind.waypoint_count+=1
            pathFind.goTowardsNewDestination()
    return

main()

