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



if __name__ == '__main__':
    # Self-testing code goes here.
    rssi = RSSI()
    lines = [
        "BeaconRxNumber: 01    BeaconRxRSSI: 0xff",
    ]
    for line in lines:
        rssi.handle_line(line)
    print rssi.RxNumber
    print rssi.RxRSSI
    print rssi.distacne

