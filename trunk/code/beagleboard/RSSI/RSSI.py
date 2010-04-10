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
            self.distacne = int(sline[3],16)
        else:
            return "Not RSSI"
        
    def rx_distance(self, rx):
        #Under the beacon
        if (rx > 230):
            return 0
        #3 - 10 f withn the beacon
        if (rx>160)&(rx<231):
            return 1
        #10- 20 f withn the beacon
        if (rx>140)&(rx<161):
            return 2
        #20- 40 f withn the beacon
        if (rx>100)&(rx<141):
            return 3
        #more than 40 f
        if (rx<100):
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
    print rssi.distacne
    print rssi.rx_distance(rssi.distacne)

