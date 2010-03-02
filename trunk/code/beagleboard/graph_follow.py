#!python

#Our points that we want to get to
x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
y = [61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]

#calculate current position on graph, move based on plot
import pylab
import numpy as np

pylab.plot(x, y)

#Screw interpolation, we will do simple algebra instead

#start between points 1 and 2
for i in range(len(x) - 1):
    #create linear function
    for j in range(abs(x[i+1]-x[i])):
        xc = x[i] + j
        yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 
        pylab.plot(xc,yc,'bs')

pylab.show()

