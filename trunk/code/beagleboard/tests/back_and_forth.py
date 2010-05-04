#Import the modules we need
import setup
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
    f = open('/home/ubuntu/beagle/log/back_and_forth_' + str(int(time.time())) , 'w')
    try:
        ser = comm.comm()
    except:
        print "could not open serial ports"
        f.write('could not open serial ports \n')
        quit()

    sensor_data = []
    gps_list = [] 
    rssi_list = [] 
    current_position = [] 
    position_list = []
    wheels = []
    pf = path_find.pathFind()
    busy = 0

    motor.execute(('go',0,STOP))

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        wheel_info = ser.updateWheel()

        if wheel_info:
            wheels.insert(0,wheel_info)

            if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
                if pf.goTowardsNewDestination(wheels) == -1:
                    f.write('finished_course!\n')
                    print 'finished_course!\n'
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
