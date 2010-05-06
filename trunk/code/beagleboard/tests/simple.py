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
import random

def mean(number_list):
    float_nums = [float(x) for x in number_list]
    return sum(float_nums)/len(number_list)

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
    bearing = []

    command_queue = [] 
    compass_commands = []
    command_queue.append(('go',0,STOP))
    command_queue.append(('go',50,FORWARD))

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    command = command_queue.pop(0)
    desired_feet = command[1]
    motor.execute(command)

    sd = ser.updateSensors()
    while sd == 0:
        sd = ser.updateSensors()

    sensor_data.insert(0,sd)
    starting_degree = sensor_data[0].compass 
    print 'starting compass: ' + str(sensor_data[0].compass) + '\n'
    f.write('starting compass: ' + str(sensor_data[0].compass) + '\n')

    starting_degree = sensor_data[0].compass
    time.sleep(1)

    while(1):
        ser.babyard.flushInput()
        wheel_info = ser.updateWheel()
        sd = ser.updateSensors()

        if sd:
            sensor_data.insert(0,sd)
        if wheel_info:
            wheels.insert(0,wheel_info)

        if starting_degree != -1:
            #compass_commands = compass.checkCompass(starting_degree,sensor_data)
            bearing.append(distance.calcRelBearing(starting_degree, sensor_data[0].compass))

            if len(bearing) > 10: 
                print "bearing",bearing
                bearing_avg = mean(bearing)
                bearing.pop(0)
                print "bearing avg: " , bearing_avg

            if bearing_avg > 20:
                compass_commands.append(('go',0,STOP))
                compass_commands.append(('turn', RIGHT, bearing_avg))

            if bearing_avg < -20:
                compass_commands.append(('go',0,STOP))
                compass_commands.append(('turn', LEFT, -1*bearing_avg))

            if compass_commands:
                f.write("compass commands " + str(compass_commands))
                ft_traveled = (wheels[0].ft['left'] + wheels[0].ft['right']) / 2
                new_distance = desired_feet - ft_traveled
                compass_commands.append(('go', new_distance, FORWARD))

                if len(compass_commands) > 1:
                    for count in range(len(compass_commands) -1):
                        command = compass_commands.pop(0)
                        response = motor.execute(command)
                        if response:
                            while wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
                                wheel_info = ser.updateWheel()
                                if wheel_info:
                                    wheels.insert(0,wheel_info)
                            
                    #execute the last command
                    sd = ser.updateSensors()
                    sensor_data.insert(0,sd)
                    starting_degree = sensor_data[0].compass
                    bearing = []
                    bearing_avg = 0
                    motor.execute(compass_commands.pop(0))

        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            #execute the last command
            if command_queue:
                command = command_queue.pop(0)
                desired_feet = command[1]
                response = motor.execute(command)
                if command[2] == FORWARD:
                    starting_degree = sensor_data[0].compass
            else:
                print 'finished'
                f.write('finished')
                quit()
    return
main()
