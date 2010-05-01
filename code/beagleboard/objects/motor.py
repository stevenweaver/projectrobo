import comm

def go(ft, dir):
    ser = comm.comm()
    #send direction to serial port
    #1182 ticks equals a foot 
    ticks = command * 1182;
    ser.send(str(ticks) + 'T')
    ser.send(command)
    return 1

def turn(dir, degrees):
    print "dir " + dir 
    print "degrees " + str(degrees) 
    return 1

def execute(command):
    print command
    return 1
