import comm
import time

def go(ft, direction):
    ser = comm.comm()
    #send direction to serial port
    #1182 ticks equals a foot 
    ticks = ft * 1182;
    ser.send(str(direction))
    time.sleep(1)
    ser.send(str(ticks) + 'T')
    return 1

def turn(direction, degrees):
    print "dir " + str(direction) 
    print "degrees " + str(degrees) 
    return 1

def execute(command):
    if command[0] is 'turn':
        turn(command[1], command[2])

    elif command[0] is 'go':
        go(command[1], command[2])

    else:
        print "invalid_command: " + str(command)

    return 1
