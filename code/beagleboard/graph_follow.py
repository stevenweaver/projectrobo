#!/usr/bin/env python

#calculate current position on graph, move based on plot
import pylab
import numpy as np
import matplotlib
import time 

matplotlib.use('TkAgg') # do this before importing pylab

#pylab.plot(x, y)
fig = pylab.figure()
ax = fig.add_subplot(111)

def animate():
    x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
    y = [61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]

    tstart = time.time()                   # for profiling
    line, = ax.plot(x, y)

    for i in range(len(x) - 1):
        for j in range(abs(x[i+1]-x[i])):
            if x[i+1] < x[i]:
                xc = x[i] - j
            else:
                xc = x[i] + j
            yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 
            line.set_xdata(xc)
            line.set_ydata(yc)                        # update the data
            fig.canvas.draw()                         # redraw the canvas
        print 'FPS:' , 200/(time.time()-tstart)


win = fig.canvas.manager.window
fig.canvas.manager.window.after(100, animate)
pylab.show()


##start between points 1 and 2
#for i in range(len(x) - 1):
#    #create linear function
#    for j in range(abs(x[i+1]-x[i])):
#        if x[i+1] < x[i]:
#            xc = x[i] - j
#        else:
#            xc = x[i] + j
#        yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 
#        #print xc,yc
#        #pylab.plot(xc,yc)
