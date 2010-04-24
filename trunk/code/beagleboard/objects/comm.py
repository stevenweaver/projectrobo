#This can be a class
import setup
import serial
import sensorData as sensor 
import nmea 
import rssi 
import send

class comm:
    def __init__(self):
        #Set up serial connections
        ard_ser = serial.Serial('/dev/arduino', 9600)
        gps_ser = serial.Serial('/dev/gps', 9600)
        rssi_ser = serial.Serial('/dev/rssi', 115200)

    def updateSensors():
        #Parse serial information
        #Check to make sure we have a nice string
        sxml = ard_ser.readline()
        while sxml.find('<?xml version="1.0"?>') != 0:
            sxml = ser.readline()
        return sensor.sensorData(sxml)

    def updateGps():
        #Parse serial information
        #probably need error checking
        gps_data = gps_ser.readline()
        return nmea.nmea(gps_data)

    def updateRssi():
        #Parse serial information
        #Check to make sure we have a nice string
        #probably need error checking
        rssi_data = rssi_ser.readline()
        return rssi.rssi(rssi_data)

    def send(command):
        ard_ser.write(send.sendStr(command))
