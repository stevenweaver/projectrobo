#Import the modules we need
import setup
import distance 
import motor
import avoidance
import compass
import path_find
import comm
from defines import * 
import time

#main loop 
def main():
    #initialization, our huge lists of information
    f = open('../log/back_and_forth_' + str(int(time.time())) , 'w')
    try:
        ser = comm.comm()
    except:
        print "could not open serial ports"
        f.write('could not open serial ports \n')
        quit()

    #Sensor data
    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    wheels = []
    pf = path_find.pathFind()
    busy = 0
    motor.execute(('go',0,STOP))

    #Beacon
    going_towards_beacon = 0
    sensor_data = []

    #Compass stuff

    #RSSI 
    rssi_list = [] 
    rssi_distance_list = []
    dis_avg = 0

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        wheel_info = ser.updateWheel()

        if wheel_info:
            ser.babyard.flushInput()
            wheel_info = ser.updateWheel()

            ser.ard_ser.flushInput()
            sd = ser.updateSensors()

            rssi_d = ser.updateRssi()

            if rssi_d:
                if rssi_d.RxNumber == beacon_number:
                    rssi_distance_list.insert(0,rssi_d.distance)

                    if len(rssi_distance_list) > 10:
                        print rssi_distance_list
                        dis_avg = mean(rssi_distance_list)
                        rssi_distance_list.pop()

            if sd:
                sensor_data.insert(0,sd)
            if wheel_info:
                wheels.insert(0,wheel_info)

            wheels.insert(0,wheel_info)

            #Beacon Detection
            #Change direction to accommodate going through the beacon.
            if beacon.beaconDetect(dis_avg, sensor_data) and not going_towards_beacon:
                beacon_commands = beacon.goTowardsBeacon(sensor_data)
                print "beacon commands", beacon_commands
                if beacon_commands:
                    response = motor.execute(beacon_commands)
                    going_towards_beacon = 1
                    starting_degree = sensor_data[0] = compass

                beacon_commands = ()

            elif going_towards_beacon:
                response = motor.execute(('go',1,FORWARD))
                if beacon.underBeacon(dis_avg):
                    going_towards_beacon = 0
                    print "going towards beacon", going_towards_beacon

                if beacon.stillLocked(sensor_data) != 1: 
                    going_towards_beacon = 0

            
            #Compass correction
            compass_commands = compass.checkCompass(starting_degree, compass)
            if compass_commands:
                response = motor.execute(compass_commands)
                compass_commands = ()

            if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
                if pf.goTowardsNewDestination(wheels,sensor_data) == -1:
                    f.write('finished_course!\n')
                    print 'finished_course!\n'
                    f.write('all of the wheel information = \n')
                    for wheel in wheels:
                        f.write('left: ' + str(wheel.ft['left']) + ' right: ' + str(wheel.ft['right']) + ' \n')
                    quit()

                else:
                    command_queue = pf.goTowardsNewDestination(wheels, sensor_data)
                    f.write('new commands = ' + str(command_queue) + '\n')
                    #this will be a turn and then a command
                    #validate that it is a turn
                    if len(command_queue) > 1:
                        for count in range(len(command_queue) -1):
                            command = command_queue.pop(0)
                            response = motor.execute(command)
                            if response:
                                while wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
                                    wheel_info = ser.updateWheel()
                                    if wheel_info:
                                        wheels.insert(0,wheel_info)
                                
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
    return
main()
