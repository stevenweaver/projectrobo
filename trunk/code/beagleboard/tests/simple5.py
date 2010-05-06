#Import the modules we need
import setup
import distance
import beacon
import motor
import avoidance
import compass
import rssi
import comm
from defines import * 
import time
import random

def mean(values):
   return sum(values, 0.0)/len(values) 


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

    #RSSI 
    rssi_list = [] 
    rssi_distance_list = []
    dis_avg = 0
    beacon_number = 4
    going_towards_beacon = 0
    sensor_data = []
    wheels = []

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
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))
    command_queue.append(('go',10,FORWARD))

    command = command_queue.pop(0)
    motor.execute(command)

    sd = ser.updateSensors()
    while sd == 0:
        sd = ser.updateSensors()

    if sd:
        sensor_data.insert(0,sd)
    starting_degree = sensor_data[0].compass 

    while(1):
        ser.babyard.flushInput()
        wheel_info = ser.updateWheel()

        ser.ard_ser.flushInput()
        sd = ser.updateSensors()

        #ser.rssi_ser.flushInput()
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
            
        #wall walking
        while (sensor_data[0].us['r'] < 30)&(wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1):
            if (sensor_data[0].us['l'] < 25):
                response = motor.execute(('turn', LEFT, 90))
            elif (sensor_data[0].us['r'] < 10):    
                response = motor.execute(('turn', LEFT, 20))
            elif (sensor_data[0].us['r'] > 20):
                response = motor.execute(('turn', RIGHT, 15))
            time.sleep(1)
            while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
            response = motor.execute(('go',3, FORWARD))
                                    

        elif going_towards_beacon:
            response = motor.execute(('go',0,STOP))
            response = motor.execute(('go',1,FORWARD))
            time.sleep(1)
            while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                wheel_info = ser.updateWheel()
                if wheel_info:
                    wheels.insert(0,wheel_info)

            ser.ard_ser.flushInput()
            if beacon.underBeacon(dis_avg):
                going_towards_beacon = 0
                print "going towards beacon", going_towards_beacon

            if beacon.stillLocked(sensor_data) != 1: 
                going_towards_beacon = 0
                print "going towards beacon", going_towards_beacon

        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            #execute the last command
            bearing = distance.calcRelBearing(starting_degree, sensor_data[0].compass)

            if abs(bearing) > 10:
                if bearing > 10:
                    #compass_commands.append(('go',0,STOP))
                    compass_commands = ('turn', RIGHT, bearing)
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
