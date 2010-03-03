#!/usr/bin/env python

#calculate current position on graph, move based on plot
import pylab
import numpy as np
import matplotlib
import time 
from pylab import imread, imshow, gray, mean

matplotlib.use('TkAgg') # do this before importing pylab

#pylab.plot(x, y)
fig = pylab.figure()
ax = fig.add_subplot(111)
b = imread('beagle.png')
imshow(b)

def animate():
    x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
    y = [61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]

    tstart = time.time()                   # for profiling
    line, = ax.plot(x, y)

    for i in range(len(x) - 1):
        if abs(x[i+1] - x[i]) > abs(y[i+1] - y[i]):
            for j in range(abs(x[i+1]-x[i])):
                if x[i+1] < x[i]:
                    xc = x[i] - j
                else:
                    xc = x[i] + j
                yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 
                ax.plot(xc,yc,'bo')                        # update the data
                if j > 0:
                    del ax.lines[1]
                fig.canvas.draw()                         # redraw the canvas
            print 'FPS:' , 200/(time.time()-tstart)
        else:
            for j in range(abs(y[i+1]-y[i])):
                if y[i+1] < y[i]:
                    yc = y[i] - j
                else:
                    yc = y[i] + j
                xc = x[i] + (yc-y[i])*(x[i+1] - x[i])/(y[i+1] - y[i]) 
                ax.plot(xc,yc,'bo')                        # update the data
                if len(ax.lines) > 1:
                    del ax.lines[1]
                fig.canvas.draw()                         # redraw the canvas
            print 'FPS:' , 200/(time.time()-tstart)


win = fig.canvas.manager.window
fig.canvas.manager.window.after(100, animate)
pylab.show()
