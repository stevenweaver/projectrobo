import string
import math

class NMEA:
    def __init__(self):
        self.time = '?'
        self.lat = 0.0
        self.lon = 0.0
        self.satellites = 0 
        self.track = 0.0
        self.speed = 0.0

    #Making assumptions I'm in the northern, western hemisphere.
    def processGPGGA(self,words):
        self.time = words[0]
        self.lat = words[1];
        self.lon = words[3];
        self.satellites = words[6] 

    def handle_line(self, line):
        #Just making sure the data is well formed
        if line[0] == '$':
            line = string.split(line[1:-1], '*')
            if len(line) != 2: return
            words = string.split(line[0], ',')
            if NMEA.__dict__.has_key('process'+words[0]):
                NMEA.__dict__['process'+words[0]](self, words[1:])
            else:
                return "Unknown sentence"
        else:
            return "Not NMEA"

if __name__ == '__main__':
    # Self-testing code goes here.
    nmea = NMEA()
    lines = [
        "$GPGGA,180227.933,3246.6682,N,11704.3135,W,1,03,10.3,30.1,M,-34.8,M,,0000*66\n",
    ]
    for line in lines:
        nmea.handle_line(line)
    print nmea.lat
    print nmea.lon
    print nmea.satellites
    print nmea.time
