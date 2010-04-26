import comm

def goFeet(command):
    ser = comm.comm()
    #send direction to serial port
    #97 ticks equals a foot 
    ticks = command * 97;
    ser.send(str(ticks) + 'T')
    return 1

def goDir(command):
    ser = comm.comm()
    ser.send(command)
    return 1

def turn(dir, degrees):
    return 1
