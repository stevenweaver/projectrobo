import string
import math

class nmea:
    def __init__(self, line):
        self.time = '?'
        self.lat = 0.0
        self.lon = 0.0
        self.satellites = 0 
        self.track = 0.0
        self.speed = 0.0
        self.handle_line(line)

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


