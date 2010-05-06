#!/usr/bin/python
import rssi 
import serial
import time 

def mean(values):
   return sum(values, 0.0)/len(values) 

ser = serial.Serial('/dev/rssi', 115200)
rssi_distance_list = []
dis_avg = 0

while 1:
    rssi_data = ser.readline()
    rssi_d = rssi.RSSI(rssi_data) 

    if rssi_d.RxNumber == 4:
        rssi_distance_list.insert(0,rssi_d.distance)


        if len(rssi_distance_list) > 10:
            dis_avg = mean(rssi_distance_list)
            rssi_distance_list.pop()

        #if rssi_d.RxNumber == 1:
        #print rssi_d.RxNumber, "  ", rssi_d.RxRSSI,"  ", rssi_d.distance, "  ", rssi_d.rx_distance()

        print rssi_d.RxNumber, "  ", rssi_d.RxRSSI,"  ", rssi_d.distance, "  ", dis_avg
