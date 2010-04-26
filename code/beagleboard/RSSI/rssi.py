import string
import math

class RSSI:
    def __init__(self, line):
        self.RxNumber = 0.0
        self.RxRSSI = 0x00
        self.distance = 0
        self.rx_distacne = 0
        self.handle_line(line)

    def handle_line(self, line):
        if line[0] == '0':
            sline = line.split()
            self.RxNumber = int(sline[0])
            self.RxRSSI = sline[1]
            self.distance = int(sline[1],16)
            
        else:
            return "Not RSSI"
        
    def rx_distance(self):
        #Under the beacon
        if (self.distance > 200):
            return 0
        #3 - 10 f withn the beacon
        if (self.distance>160)&(self.distance<201):
            return 1
        #10- 20 f withn the beacon
        if (self.distance>140)&(self.distance<161):
            return 2
        #20- 40 f withn the beacon
        if (self.distance>50)&(self.distance<141):
            return 3
        #more than 40 f
        if (self.distance<51):
            return 4
        return
 

##
##
##if __name__ == '__main__':
##    # Self-testing code goes here.
##    rssi = [] 
##    lines = [
##        "BeaconRxNumber: 01    BeaconRxRSSI: 0xE0",
##    ]
##    for line in lines:
##        rssi.append(RSSI(line))
##
##    print rssi[0].RxNumber
##    print rssi[0].RxRSSI
##    print rssi[0].distance
##    print rssi[0].rx_distance()
