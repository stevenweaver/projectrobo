import setup
from defines import *
import motor

def obstacle(sd):
    #Check if the obstacles are dangerously in the way
    if sd.us['right'] < RANGE_LIMIT or sd.us['left'] < RANGE_LIMIT or sd.flex['left'] < LEFT_DANGEROUS or sd.flex['right'] < RIGHT_DANGEROUS:
        if setup.QA:
            print 'us right' + str(sd.us['right'])
            print 'us left' + str(sd.us['left'])
            print 'flex right' + str(sd.flex['right'])
            print 'flex left' + str(sd.flex['left'])
        return 1

    return 0

def moveOutTheWay(sd):
    #Check for flex first
    flex(sd)

    #Then check for ultrasonics
    range_finders(sd)

    return 1

def flex(sd):
    #Flex Sensors
    #Check right side
    if sd.flex['right'] < RIGHT_HITTING:
        motor.turn(LEFT, 15)

    elif sd.flex['right'] < RIGHT_SCRAPPING: 
        motor.turn(LEFT, 45)

    elif sd.flex['right'] < RIGHT_DANGEROUS:
        motor.goDir(STOP)
        motor.goDir(REVERSE)
        motor.goFeet(4)
        motor.turn(LEFT, 45)
        motor.goDir(FORWARD)

    #Check left side
    elif sd.flex['left'] < LEFT_HITTING:
        motor.turn(right, 15)

    elif sd.flex['left'] < LEFT_SCRAPPING: 
        motor.turn(LEFT, 45)

    elif sd.flex['left'] < LEFT_DANGEROUS:
        motor.goDir(STOP)
        motor.goDir(REVERSE)
        motor.goFeet(4)
        motor.turn(LEFT, 45)
        motor.goDir(FORWARD)

def range_finders(sd):
    if sd.us['right'] < RANGE_LIMIT and sd.us['left'] < RANGE_LIMIT:
        motor.goDir(STOP)
        motor.turn(LEFT, 90)
        motor.goFeet(1)
        motor.goDir(FORWARD)
        motor.goDir(STOP)
        motor.turn(RIGHT, 90)
        motor.goDir(FORWARD)

    elif sd.us['right'] < RANGE_LIMIT:
        #Turn left a little bit, then straighten out
        motor.turn(LEFT, 15)
        motor.goDir(FORWARD)

    elif sd.us['left'] < RANGE_LIMIT:
        #Turn right a little bit, then straigten out 
        motor.turn(RIGHT, 15)
        motor.goDir(FORWARD)
