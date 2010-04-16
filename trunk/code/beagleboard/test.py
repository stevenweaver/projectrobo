#!/bin/python
import time

f = open('/home/steven/projectrobo/code/beagleboard/log/test_' + str(int(time.time())) , 'w')
f.write('it worked\n')
