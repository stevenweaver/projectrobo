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
import math

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

    #For object avoidance
    bearing_berfore_object = -1
    position_before_object = []

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
                position_before_object = current_position 
                bearing_before_object = sensor_data[0].compass
                distance_traveled = 1
                avoiding_object = 1

        while avoiding_object:
            #pop off commands
            motor.execute(command_queue.pop(0))

            if not command_queue:
                #Check to make sure we are out of the way, else move another foot
                #We've made it through the first commands which we know is turn one and move forward
                if not avoidance.isOutOfWay(sensor_data[0]):
                    distance_traveled = distance_traveled + 1
                    command_queue.append(('go',1,FORWARD))

                else:
                    #We need to update our current position and set that as our new waypoint 
                    #update the current point
                    print position_before_object[1],position_before_object[0] 
                    angle_a = math.atan(position_before_object[1]/position_before_object[0])
                    b = math.sqrt(math.pow(position_before_object[1],2)+math.pow(position_before_object[0],2))
                    d = math.sqrt(math.pow(b,2) + math.pow(distance_traveled,2))
                    angle_b = math.atan(distance_traveled/b)
                    angle_c = angle_a + angle_b
                    print math.degrees(angle_c)
                    angle_d = 180 - 90 - angle_c
                    print d
                    x = d*math.sin(angle_d)
                    y = d*math.sin(angle_c)
                    print x,y
                    quit()

                    pf.waypoints.insert(waypoint_count,current_position)
                    avoiding_object = 0

            wheel_info = ser.updateWheel()

            if wheel_info:
                wheels.insert(0,wheel_info)

            while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                sd = ser.updateSensors()
                wheel_info = ser.updateWheel()
                if wheel_info:
                    wheels.insert(0,wheel_info)
                    #current_position = pf.getCurrentPoint(wheels)   
                    print current_position
                if sd: 
                    sensor_data.insert(0,sd)

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

        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            if pf.goTowardsNewDestination(wheels) == -1:
                print "finished_course!"
                quit()
            else:
                command_queue = pf.goTowardsNewDestination(wheels)
                #this will be a turn and then a command
                #validate that it is a turn
                if len(command_queue) > 1:
                    for count in range(len(command_queue) -1):
                        command = command_queue.pop(0)
                        motor.execute(command)

                        #Wait for the turtle to do its thing
                        wheel_info = ser.updateWheel()

                        if wheel_info:
                            wheels.insert(0,wheel_info)

                        while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                            wheel_info = ser.updateWheel()
                            if wheel_info:
                                wheels.insert(0,wheel_info)
                                current_position = pf.getCurrentPoint(wheels)   
                                print current_position

                #execute the last command
                motor.execute(command_queue.pop(0))
                pf.waypoint_count+=1
        #time.sleep(.02)

    return
main()
