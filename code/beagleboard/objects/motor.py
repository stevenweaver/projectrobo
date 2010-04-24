import comm

class motor:
    def goFeet(command):
        #send direction to serial port
        #97 ticks equals a foot 
        ticks = command * 97;
        comm.send(str(ticks) + 'T')
        return 1

    def goDir(command):
        comm.send(command)
        return 1

    def turn(dir, degrees):
        return 1
