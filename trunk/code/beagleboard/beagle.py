#First we need to include the new python path
import sys
#QA
HOME = '/home/steven/projectrobo/code/beagleboard' 
#BEAGLE
#HOME = '/home/ubuntu/beagle' 
sys.path.append(HOME + '/libs/') 


#Import the modules we need
import serial
import defines

#ser = serial.Serial('/dev/arduino', 9600)
#ser = serial.Serial('/dev/gps', 9600)
#ser = serial.Serial('/dev/rssi', 9600)

#print ser.readline()

#We're going to "package" all of the sensor data and send it in clumps over the serial.

def masterControl():
    #This whole function desperately needs more thinking
    
    #Check if there are obstacles
    #If there are obstacles, move out of the way. Once we feel safe, update new point on map and recreate interpolation to include new point where we sit.

    #Check if there are Beacons
    #Change direction to accommodate going through the beacon.

    #Check Directions
    #if calcNextPosition==calcPosition goto: calcDirection

    #Based on the above curricula, we should have a direction we need to go in by now
    #setDirection()
    return

def calcObstacles():
    #Check if the obstacles are dangerously in the way
    return

def calcBeacons():
    #Check if the Beacons are within range
    return

def calcDirection():
    #calcPosition
    #calcNextPosition
    #Decide how to get there
    return
 
def calcPosition():
    #compass
    #dead reckoning
    #gps
    return

def getObstacles():
    #ultrasonic sensors
    #flex sensors
    return

def getBeacon():
    #beacon
    return

def setDirection():
    #send direction to serial port
    return

def parseSerialInfo():
    #Parse serial information
    #Thought: we might want to do this in a separate thread to ensure we continually get fresh data?
    return
