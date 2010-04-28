#!/usr/bin/env python

#calculate current position on graph, move based on plot
import pylab
import numpy as np
import matplotlib
import time 
from pylab import imread, imshow, gray, mean
import math

matplotlib.use('TkAgg') # do this before importing pylab

#pylab.plot(x, y)
fig = pylab.figure()
ax = fig.add_subplot(111)
b = imread('Drawing6.png')
imshow(b)

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
    x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
    y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
    waypoints = zip(x,y)
    y[:] = [(-a*9.6) + 2060 for a in y]
    x[:] = [a*9.6 + 410 for a in x]
    #waypoints = zip(x,y)

    tstart = time.time()                   # for profiling
    line, = ax.plot(x, y)

    for i in range(len(x) - 1):
        angle = calcAngle(waypoints[i], waypoints[i+1])
        #ax.set_title("pt" + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1]))) 
        if abs(x[i+1] - x[i]) > abs(y[i+1] - y[i]):
            for j in range(abs(x[i+1]-x[i])):
                fname = '_tmp' + str(i) + str(j) + '_%03d.png'
                if j % 30 == 0:
                    if x[i+1] < x[i]:
                        xc = x[i] - j
                    else:
                        xc = x[i] + j
                    yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 
                    ax.plot(xc,yc,'bo')                        # update the data

                    if x[i+1] < x[i]:
                        distance = math.sqrt(math.pow((xc + x[i]),2)+math.pow((yc - y[i]), 2))
                    else:
                        distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))


                    delta_y = math.sin(angle) * distance 
                    delta_x = math.cos(angle) * distance

                    #ax.set_title("waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + "current_point: " + str(xc) + ',' + str(yc) + "calc_pt: " + str(delta_x) + ',' + str(delta_y)) 

                    if j > 0:
                        ax.lines.reverse()
                        del ax.lines[1:]

                    fig.canvas.draw()                         # redraw the canvas
                    fig.savefig(fname)

            print 'FPS:' , 200/(time.time()-tstart)
        else:
            for j in range(abs(y[i+1]-y[i])):
                fname = '_tmp' + str(i) + str(j) + '_%03d.png'
                if j % 30 == 0:
                    if y[i+1] < y[i]:
                        yc = y[i] - j
                    else:
                        yc = y[i] + j
                    xc = x[i] + (yc-y[i])*(x[i+1] - x[i])/(y[i+1] - y[i]) 
                    ax.plot(xc,yc,'bo')                        # update the data

                    if y[i+1] < y[i]:
                        distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc + y[i]), 2))
                    else:
                        distance = math.sqrt(math.pow((xc - x[i]),2)+math.pow((yc - y[i]), 2))

                    delta_x = math.sin(angle) * distance 
                    delta_y = math.cos(angle) * distance

                    #ax.set_title("waypt: " + str(i) + " angle:" + str(calcAngle(waypoints[i], waypoints[i+1])) + "current_point: " + str(xc) + ',' + str(yc) + "calc_pt: " + str(x[i] + delta_x) + ',' + str(y[i] + delta_y)) 

                    if len(ax.lines) > 1:
                        ax.lines.reverse()
                        del ax.lines[1:]

                    fig.canvas.draw()                         # redraw the canvas
                    fig.savefig(fname)
            print 'FPS:' , 200/(time.time()-tstart)


win = fig.canvas.manager.window
fig.canvas.manager.window.after(100, animate)
pylab.show()
