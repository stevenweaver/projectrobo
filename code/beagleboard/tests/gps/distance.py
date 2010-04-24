#!/usr/bin/python
import math

#Convert Coor. to decimal
def toDec(a):
    lat =  32 +((a[0]-3200.0)/60)
    lon = 117 + ((a[1]-11700)/60)
    p = [ lat,lon]
    return p;

#lat2 and lon2 can always be the checkmarks
def calcBearing(p1, p2):
    dLon = p2[1] - p1[1]
    y = math.sin(dLon) * math.cos(p2[0])
    x = math.cos(p1[0]) * math.sin(p2[0]) \
        - math.sin(p1[0]) * math.cos(p2[0]) * math.cos(dLon)
    a = math.atan2(y, x)
    r = math.degrees(a)
    return r

#lat2 and lon2 can always be the checkmarks
def havDistance(dp1 , dp2):
    a1 =(math.atan(math.pow(6356752.3142,2)/math.pow(6378137,2)*math.tan(dp1[0]*math.pi/180)))*180/math.pi
    a2 =(math.atan(math.pow(6356752.3142,2)/math.pow(6378137,2)*math.tan(dp2[0]*math.pi/180)))*180/math.pi
    r1 = math.pow(1/((math.pow(math.cos(a1*math.pi/180),2))/(math.pow(6378137,2))+
                   (math.pow(math.sin(a1*math.pi/180),2))/(math.pow(6356752.3142,2))),0.5)
    r2 = math.pow(1/((math.pow(math.cos(a2*math.pi/180),2))/(math.pow(6378137,2))+
                   (math.pow(math.sin(a2*math.pi/180),2))/(math.pow(6356752.3142,2))),0.5)
    x1 = r1*math.cos(a1*math.pi/180)
    x2 = r2*math.cos(a2*math.pi/180)
    y1 = r1*math.sin(a1*math.pi/180)
    y2 = r2*math.sin(a2*math.pi/180)
    x = math.hypot((x1-x2),(y1-y2))
    y =2*math.pi*((((x1+x2)/2))/360)*(dp1[1]-dp2[1])
    dm = math.hypot(x ,y)
    df = dm*3.28084
    
    return df

#Finding X - Y Coor in the map
def getCoor(p):
    lat = (p[0]-3246) *10000
    lon = (p[1]-11704) *10000
    ax = 0.478969631
    ay = 0.513217847
    alx = 2555.32926
    aly = 6140.918582
    x = 300-(300+(lon-alx)*ax) 
    y = (lat-aly)*ay
    coor = [x,y]
    return coor

##p1 = [3246.6449, 11704.2028]
##p2 = [3246.6531,11704.2099]
##dp1 = toDec(p1)
##dp2 = toDec(p2)
##distance = havDistance(dp1, dp2)
##coor = getCoor(p1)
##
##print "p1 To dec:" , dp1
##print "p2 To dec:" , dp2
##print "x,y = " ,coor
##print "distance is: ",distance
##print "Bearing is:",calcBearing(dp2, dp1)
