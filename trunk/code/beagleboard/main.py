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
import gps


#main loop 
def main():
    #initialization, our huge lists of information
    beacon_goal = 1;
    ser = comm.comm()
    sd = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    pf = pathFind.pathFind()
    saw_beacon = 0
    
    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()

    while(1):
        sd.insert(0,ser.updateSensors())
        gps_list.insert(0,ser.updateGps())
        rssi_list.insert(0,ser.updateRssi())
        
        #Using flex 
        if(object == 0):
            #GO: reverse 
            #GO: home
            return
        
        #If there is an object in the way USING Ultrasonic
        elif(object == 1):
            #TURN: 90 to left
            #while right not clear and fornt is clear
                #GO:one foot forword
                #Y=Y+1
            #if front is not clear
                #TURN: 180
                #GO: Y*2 -- STOP if object in front
                #TURN: 180 
                #object = 1 ; x = 0 ; Y=0
                #RETURN
            #TURN: right 90
            #While right not clear
                #GO: one foot forword
                # X=X+1 -- ADD X to deadreckoning data
            #TURN: 90 right
            #Go: Y feet
            return
        elif(saw_beacon):
            return
        
        ##main for the first beacon
        #path findinf: deadreckoning,compass 
        #beacon finding: rssi,ultrasoinc
        #object avoid.: Ultrasoinc ... flex?
        elif(beacon_goal == 1):
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
            elif pf.atWaypoint(sd):
                pf.waypoint_count+=1
                pf.goTowardsNewDestination()
                
        ##main for second beacon
        
        elif(beacon_goal == 2):
            return
        ##main for second beacon
        elif(beacon_goal == 2):
            return
        ##main for second beacon
        elif(beacon_goal == 2):
            return
        ##main for second beacon
        elif(beacon_goal == 2):
            return
    return

main()
