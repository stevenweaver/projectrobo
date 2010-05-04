from defines import *
import comm
import time

def go(ft, direction):
    if direction != STOP and ft != 0:
        ser = comm.comm()
        #send direction to serial port
        #1182 ticks equals a foot 
        ticks = ft * 1182;
        ser.send(str(direction))
        time.sleep(1)
        ser.send(str(int(ticks)) + 'T')
        print "dir:" + str(direction) + '\n'
        print "ft:" + str(ft) + '\n'
        return 1

    return 0

def turn(direction, degrees):
    #Right works better
    if degrees != 0:
        ser = comm.comm()
        ticks = degrees * (1000/90) 
        ser.send(str(direction))
        time.sleep(1)

        print "dir: " + str(direction) + '\n'
        print "degrees" + str(degrees) + '\n'
        ser.send(str(int(ticks)) + 'T')
        return 1

    return 0

def execute(command):
    print "command: " + str(command) + '\n'
    response = 0 

    if command[0] is 'turn':
        response = turn(command[1], command[2])

    elif command[0] is 'go':
        response = go(command[1], command[2])

    else:
        print "invalid_command: " + str(command)

    return response 
