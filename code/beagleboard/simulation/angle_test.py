#!/usr/bin/env python

#calculate current position on graph, move based on plot
import pylab
import numpy as np
import time 
from pylab import imread, imshow, gray, mean
import math


def calcDistance(pt1, pt2):
    return math.sqrt(math.pow((pt2[0] - pt1[0]),2)+math.pow((pt2[1] - pt1[1]), 2))

def calcAngle(pt1, pt2):
    #now we need to find angle A, since we know sinA is height/distance we can just find the inverse sine 
    distance = calcDistance(pt1, pt2)
    if abs(pt2[0] - pt1[0]) > abs(pt2[1] - pt1[1]):
        diff = pt2[1] - pt1[1]
    #Else we want to calculate the difference in x
    else:
        diff = pt2[0] - pt1[0] 

    #Calculate the angle
    return math.asin(diff/distance) 

def animate():
    x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
    y = [61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]
    waypoints = zip(x,y)
    tstart = time.time()                   # for profiling
    for i in range(len(x) - 1):
        angle = calcAngle(waypoints[i], waypoints[i+1])
        if abs(x[i+1] - x[i]) > abs(y[i+1] - y[i]):
            for j in range(abs(x[i+1]-x[i])):
                if x[i+1] < x[i]:
                    xc = x[i] - j
                else:
                    xc = x[i] + j
                yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 

                if x[i+1] < x[i]:
                    distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))
                else:
                    distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))

                delta_y = math.sin(angle) * distance 
                delta_x = math.cos(angle) * distance

                if x[i+1] < x[i]:
                    print "waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + " current_point: " + str(xc) + ',' + str(yc) + " calc_pt: " + str(x[i] - delta_x) + ',' + str(y[i] + delta_y) 
                else:
                    print "waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + " current_point: " + str(xc) + ',' + str(yc) + " calc_pt: " + str(x[i] + delta_x) + ',' + str(y[i] + delta_y)

        else:
            for j in range(abs(y[i+1]-y[i])):
                if y[i+1] < y[i]:
                    yc = y[i] - j
                else:
                    yc = y[i] + j
                xc = x[i] + (yc-y[i])*(x[i+1] - x[i])/(y[i+1] - y[i]) 

                if y[i+1] < y[i]:
                    distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))
                else:
                    distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))

                delta_x = math.sin(angle) * distance 
                delta_y = math.cos(angle) * distance

                if y[i+1] < y[i]:
                    print "waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + " current_point: " + str(xc) + ',' + str(yc) + " calc_pt: " + str(x[i] + delta_x) + ',' + str(y[i] - delta_y) 
                else:
                    print "waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + " current_point: " + str(xc) + ',' + str(yc) + " calc_pt: " + str(x[i] + delta_x) + ',' + str(y[i] + delta_y) 

animate()

