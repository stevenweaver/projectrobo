#Import the modules we need
import setup
import comm
from defines import * 
import numpy as np
import time
import gps


#main loop 
def main():
    #initialization, our huge lists of information
    ser = comm.comm()
    sd = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    #pf = pathFind.pathFind()

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    gps_count = 0
    heading = 0
    distance = 0
    while(1):
        #rssi_list.insert(0,ser.updateRssi())
        gps_list.insert(0,ser.updateGps())
        if gps_count >3:
            gps_data = gps.gps(1, gps_list[0].coor,gps_list[2].coor)
            robot_heading = gps_data.robot_heading
            heading = gps_data.direction
            distance = gps_data.distance
            gps_coor = gps_data.gps_coor
            print gps_list[0].satellites," ",robot_heading," ",heading," ",distance," ",gps_coor
        else:
            gps_count = gps_count +1
    return

main()
