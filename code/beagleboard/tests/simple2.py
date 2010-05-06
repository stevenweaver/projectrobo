#Import the modules we need
import setup
import distance
import motor
import avoidance
import compass
import comm
from defines import * 
import time
import random

#main loop 
def main():
    #initialization, our huge lists of information
    f = open('/home/ubuntu/beagle/log/simple_' + str(random.randint(0,999999)) , 'w')
    try:
        ser = comm.comm()
    except:
        print "could not open serial ports"
        f.write('could not open serial ports \n')
        quit()

    bearing_avg = 0
    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    wheels = []
    busy = 0
    motor.execute(('go',0,STOP))
    starting_degree = -1 
    command_count = 0
    bearing = 0 

    command_queue = [] 
    compass_commands = []
    command_queue.append(('go',0,STOP))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))

    command = command_queue.pop(0)
    motor.execute(command)

    sd = ser.updateSensors()
    while sd == 0:
        sd = ser.updateSensors()

    sensor_data.insert(0,sd)
    starting_degree = sensor_data[0].compass 

    while(1):
        ser.babyard.flushInput()
        wheel_info = ser.updateWheel()
        ser.ard_ser.flushInput()
        sd = ser.updateSensors()

        if sd:
            sensor_data.insert(0,sd)
        if wheel_info:
            wheels.insert(0,wheel_info)

        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            #execute the last command
            bearing = distance.calcRelBearing(starting_degree, sensor_data[0].compass)
            if abs(bearing) > 10:
                if bearing > 10:
                    #compass_commands.append(('go',0,STOP))
                    compass_command = ('turn', RIGHT, bearing)
                    response = motor.execute(compass_commands)

                if bearing < -10:
                    #compass_commands.append(('go',0,STOP))
                    compass_commands = ('turn', LEFT, -1*bearing)
                    response = motor.execute(compass_commands)

                compass_commands = () 
                bearing = 0

            elif command_queue:
                command = command_queue.pop(0)
                response = motor.execute(command)

            else:
                print 'finished'
                f.write('finished')
                quit()
    return
main()
