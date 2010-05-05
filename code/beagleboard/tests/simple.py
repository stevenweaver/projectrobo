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
    f = open('../log/back_and_forth_' + str(int(time.time())) , 'w')
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
    busy = 0
    motor.execute(('go',0,STOP))
    starting_degree = -1 

    command_queue = [] 
    command_queue.append(('go',20,FORWARD))
    #command_queue.append(('turn',RIGHT, 90)) 
    #command_queue.append(('go',5, FORWARD)) 
    #command_queue.append(('turn',90, RIGHT)) 
    #command_queue.append(('go',20, FORWARD)) 

    #keep the time since we've started, could be useful to use along with wheel encoder information if we know how fast yertle goes ;)
    time_started = time.time()
    while(1):
        motor.execute(command_queue.pop(0))
        wheel_info = ser.updateWheel()
        sd = ser.updateSensors()

        if sd:
            sensor_data.insert(0,sd)

        if wheel_info:
            wheels.insert(0,wheel_info)

        if starting_degree != -1:
            compass_commands = compass.checkCompass(starting_degree,sensor_data)
            ft_traveled = (wheels[0].ft['left'] + wheels[0].ft['right'])/2
            desired_feet = command[1]

            if desired_feet - ft_traveled > desired_feet/2
                compass_command.append('go',ft_traveled, FORWARD)
                #Go back 
            else:
                compass_command.append('go',(desired_feet - ft_traveled), FORWARD)


                
        if wheels[0].done_flags['right'] == 1 and wheels[0].done_flags['left'] == 1: 
            #execute the last command
            if command_queue:
                command = command_queue.pop(0)
                response = motor.execute(command)
                if command[2] == FORWARD:
                    starting_degree = sensor_data[0].compass

            else:
                print 'finished'
                quit()
    return
main()
