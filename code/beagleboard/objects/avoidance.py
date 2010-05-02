import setup
import path_find
from defines import *
#import motor

def obstacle(sd):
    #Check if the obstacles are dangerously in the way
    if sd.us['left'] < RANGE_LIMIT or sd.flex['left'] < LEFT_DANGEROUS or sd.flex['right'] < RIGHT_DANGEROUS:
        if setup.QA:
            print 'us right' + str(sd.us['right'])
            print 'us left' + str(sd.us['left'])
            print 'flex right' + str(sd.flex['right'])
            print 'flex left' + str(sd.flex['left'])
        return 1

    return 0

def moveOutTheWay(sd):
    #Check for flex first
    #Flex Sensors
    #Check right side
    if sd.flex['right'] < RIGHT_HITTING:
        return [('turn','left', 15)]

    elif sd.flex['right'] < RIGHT_SCRAPPING: 
        return [('turn','left', 45)]

    elif sd.flex['right'] < RIGHT_DANGEROUS:
        return [('go',0,STOP),('go',4,REVERSE),('turn','left',45),('dir',0,FORWARD)] 

    #Check left side
    elif sd.flex['left'] < LEFT_HITTING:
        return [('turn','right', 15)]

    elif sd.flex['left'] < LEFT_SCRAPPING: 
        return [('turn','right', 45)]

    elif sd.flex['left'] < LEFT_DANGEROUS:
        return [('go',0,STOP),('go',4,REVERSE),('turn','right',45),('go',0,STOP)] 

    #Then check for ultrasonics
    if sd.us['left'] < RANGE_LIMIT:
        return [('go',0,STOP),('turn', LEFT, 90),('go',1,FORWARD),('go',0,STOP),('turn', RIGHT, 90),('go',0,STOP)] 
    return 0 

def isOutOfWay(sd):
    #Then check for ultrasonics
    if sd.us['right'] < RANGE_LIMIT:
        print sd.us['right']
        return 0 
    return 1
