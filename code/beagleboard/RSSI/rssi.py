import string
import math

class RSSI:
    def __init__(self):
        self.RxNumber = 0.0
        self.RxRSSI = 0x00
        self.distance = 0

    def handle_line(self, line):
        if line[0] == 'B':
            sline = line.split()
            self.RxNumber = sline[1]
            self.RxRSSI = sline[3]
            self.distance = int(sline[3],16)
        else:
            return "Not RSSI"
        
    def rx_distance(self):
        #Under the beacon
        if (self.distance > 230):
            return 0
        #3 - 10 f withn the beacon
        if (self.distance>160)&(self.distance<231):
            return 1
        #10- 20 f withn the beacon
        if (self.distance>140)&(self.distance<161):
            return 2
        #20- 40 f withn the beacon
        if (self.distance>100)&(self.distance<141):
            return 3
        #more than 40 f
        if (self.distance<100):
            return 4
        return
 



if __name__ == '__main__':
    # Self-testing code goes here.
    rssi = RSSI()
    lines = [
        "BeaconRxNumber: 01    BeaconRxRSSI: 0xE0",
    ]
    for line in lines:
        rssi.handle_line(line)
    print rssi.RxNumber
    print rssi.RxRSSI
    print rssi.distance
    print rssi.rx_distance()
