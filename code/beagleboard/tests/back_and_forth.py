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
import pprint

#main loop 
def main():
    #initialization, our huge lists of information
    f = open('../log/back_and_forth_' + str(int(time.time())) , 'w')
    ser = comm.comm()
    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    wheels = []
    pf = path_find.pathFind()
    busy = 0

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        wheel_info = ser.updateWheel()
        if wheel_info:
            wheels.insert(0,wheel_info)
        #gps_list.insert(0,ser.updateGps())
        #rssi_list.insert(0,ser.updateRssi())

        #Check if there are obstacles
        #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.
        #If obstacle, stop. Figure out which way to go, then try to go in the right direction again. 
        #if avoidance.obstacle(sensor_data[0]) == 1:
        #    avoidance.moveOutTheWay(sensor_data[0])

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
                f.write('finished_course!\n')
                f.write('all of the wheel information = \n')
                for wheel in wheels:
                    f.write('left: ' + str(wheel.ft['left']) + ' right: ' + str(wheel.ft['right']) + ' \n')
                quit()
            else:
                command_queue = pf.goTowardsNewDestination(wheels)
                f.write('new commands = ' + str(command_queue) + '\n')
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

                #execute the last command
                motor.execute(command_queue.pop(0))

                pf.waypoint_count+=1
        #time.sleep(.02)
    return
main()
