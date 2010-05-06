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
    bearing = 0 

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
        if sd:
            sensor_data.insert(0,sd)
        if wheel_info:
            wheels.insert(0,wheel_info)

        print 'left', sensor_data[0].us['left']
        
        if sensor_data[0].flex['right'] < 450: 
            response = motor.execute(('go',0,STOP))
            time.sleep(1)
            response = motor.execute(('turn',LEFT,35))
            time.sleep(1)
            
        if sensor_data[0].flex['left'] < 450: 
            response = motor.execute(('go',0,STOP))
            time.sleep(1)
            response = motor.execute(('turn',RIGHT,35))
            time.sleep(1)

        if sensor_data[0].us['left'] < 10: 
            response = motor.execute(('go',0,STOP))
            time.sleep(1)
            response = motor.execute(('turn',LEFT,100))
            time.sleep(1)
             
        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            #wall walking
            if (sensor_data[0].us['left'] < 25):
                response = motor.execute(('turn', LEFT, 100))
                while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                    wheel_info = ser.updateWheel()
                    if wheel_info:
                        wheels.insert(0,wheel_info)
            elif (sensor_data[0].us['right'] < 10):    
                response = motor.execute(('turn', LEFT, 20))
                while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                    wheel_info = ser.updateWheel()
                    if wheel_info:
                        wheels.insert(0,wheel_info)
            elif (sensor_data[0].us['right'] > 40):
                response = motor.execute(('turn', RIGHT, 90))
                while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                    wheel_info = ser.updateWheel()
                    if wheel_info:
                        wheels.insert(0,wheel_info)
            elif (sensor_data[0].us['right'] > 20):
                response = motor.execute(('turn', RIGHT, 15))
                while wheels[0].done_flags['right'] != 1 and wheels[0].done_flags['left'] != 1: 
                    wheel_info = ser.updateWheel()
                    if wheel_info:
                        wheels.insert(0,wheel_info)

            time.sleep(1)
            ser.babyard.flushInput()

            wheel_info = ser.updateWheel()
            if wheel_info:
                wheels.insert(0,wheel_info)


            response = motor.execute(('go',3, FORWARD))
    return
main()
