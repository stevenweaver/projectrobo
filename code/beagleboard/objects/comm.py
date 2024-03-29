#This can be a class
import setup
import serial
import sensorData as sensor 
import wheelParse
import nmea 
import rssi 
import send

class comm:
    def __init__(self):
        #Set up serial connections
        if setup.QA:
            #Read from file
            self.f = open('./xml_test', 'r')
            self.fw = open('./wheel_test', 'r')
        elif setup.DEAD_RECKON_TEST:
            self.babyard = serial.Serial('/dev/babyarduino', 9600)
        else:
            self.ard_ser = serial.Serial('/dev/arduino', 9600)
            self.babyard = serial.Serial('/dev/babyarduino', 9600)
            self.gps_ser = serial.Serial('/dev/gps', 9600)
            self.rssi_ser = serial.Serial('/dev/rssi', 115200)

    def updateSensors(self):
        #Parse serial information
        #Check to make sure we have a nice string
        if setup.QA: 
            sxml = self.f.readline()
        else: 
            sxml = self.ard_ser.readline()
            while sxml.find('<?xml version="1.0"?>') != 0:
                sxml = self.ard_ser.readline()

        try:
            return sensor.sensorData(sxml)
        except:
            #print "whoops! bad xml"
            return 0

    def updateWheel(self):
        #Parse serial information
        #Check to make sure we have a nice string
        if setup.QA: 
            sxml = self.fw.readline()
        else: 
            sxml = self.babyard.readline()
            #print sxml
            while sxml.find('<?xml version="1.0"?>') != 0:
                sxml = self.babyard.readline()
#print sxml

        try:
            print sxml
            return wheelParse.wheelParse(sxml)
        except:
            #print "whoops! bad xml"
            return 0

    def updateGps(self):
        #Parse serial information
        #probably need error checking
        gps_data = self.gps_ser.readline()
        return nmea.nmea(gps_data)

    def updateRssi(self):
        #Parse serial information
        #Check to make sure we have a nice string
        #probably need error checking
        rssi_data = self.rssi_ser.readline()
        return rssi.rssi(rssi_data)

    def send(self,command):
        if setup.QA:
            print command
        else:
            print send.sendStr(command)
            self.babyard.write(send.sendStr(command))
            self.babyard.flushInput()
        return
