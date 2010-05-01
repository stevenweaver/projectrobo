#Import the modules we need
import setup
import motor
import avoidance
import beacon
import compass
import path_find
import comm
from defines import * 
import time

#main loop 
def main():
    #initialization, our huge lists of information
    ser = comm.comm()
    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = () 
    position_list = []
    wheels = []
    pf = path_find.pathFind()
    command_queue = []
    avoiding_object = 0
    going_towards_beacon = 0
    turning = 0
    current_direction = STOP 

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        #Update wheel encoder information
        wheel_info = ser.updateWheel()
        if wheel_info:
            wheels.insert(0,wheel_info)

        current_position = pf.getCurrentPoint(wheels)   

        if current_position == -1:
            print "reached end of course!"
        else:
            print current_position

        #Update sensor data information
        sd = ser.updateSensors()
        if sd:
            sensor_data.insert(0,sd)

        #gps_list.insert(0,ser.updateGps())
        #rssi_list.insert(0,ser.updateRssi())

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        sd = ser.updateSensors()
        if sd:
            sensor_data.insert(0,sd)
            if avoidance.obstacle(sensor_data[0]) == 1:
                command_queue = avoidance.moveOutTheWay(sensor_data[0])
                avoiding_object = 1

        while avoiding_object:
            #pop off commands
            motor.execute(command_queue.pop(0))

            if not command_queue:
                avoiding_object = 0

            wheel_info = ser.updateWheel()

            if wheel_info:
                wheels.insert(0,wheel_info)

            while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                wheel_info = ser.updateWheel()
                if wheel_info:
                    wheels.insert(0,wheel_info)

        #Check if there are Beacons
        #Change direction to accommodate going through the beacon.
        #Use rssi for proximity and override main path, this needs to send the whole list instead of just one 
        #if beacon.beaconDetect(rssi_list[0]):
        #   beacon.goTowardsBeacon(sensor_data[0]) 

        #Check if we're veering left or right
        #if len(sensor_data) >= 10:
        #    if compass.checkCompass(sensor_data[0].compass,sensor_data[0:10]):
                #Correct ourselves
        #        print "compass_moving"

        #Otherwise continue going about our way
        #wayPoint is the new calcPosition()
        #if pf.atWaypoint(sensor_data):

        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1 and not avoiding_object and not going_towards_beacon: 
            if pf.lastWaypoint():
                print "finished_course!"
                quit()
            else:
                command_queue = pf.goTowardsNewDestination(wheels)
                print command_queue
                pf.waypoint_count+=1

    return
main()
