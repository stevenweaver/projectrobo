import setup
import numpy as np
import distance
import nmea

class gps:
    def __init__(self, wp, gps_point0, compass):
        #Import the modules we need
        self.gps_waypoints = [[3246.6428,11704.2037],
                        [3246.6350,11704.1956],
                        [3246.6224,11704.2317],
                        [3246.6306,11704.2410]]
        self.robot_heading = 0
        self.direction = 0
        self.distance = 0
        self.gps_coor = [0,0]
        self.handle(self.gps_waypoints[wp], gps_point0,compass)
        
    def handle(self,waypoint,point0,compass):
        gps_waypoint = distance.toDec(waypoint)
        gps_point0 = distance.toDec(point0)
        self.robot_heading = compass   #self.calcGpsHeading(gps_point0, gps_point1)
        self.direction = self.calcDirection(gps_point0,gps_waypoint,self.robot_heading)
        self.distance = self.calcGpsDistance(gps_waypoint,gps_point0)
        self.gps_coor = self.calcGpsPosition(point0)
        return
    
    def calcGpsHeading(self,gps_point0):
        return distance.calcBearing(gps_point1, gps_point0)
    
    def calcDirection(self,gps_point0,gps_waypoint,robot_heading):
        bearing = distance.calcBearing(gps_waypoint, gps_point0)
        return distance.calcRelBearing(bearing,robot_heading)
    
    #GPS DISTANCE CALCUATION
    def calcGpsDistance(self,gps_waypoint,gps_point0):
        return distance.havDistance(gps_waypoint,gps_point0)
    
    #ROBOT LOCATION FROM GPS
    #RETURN: POINT IF GOOD DATA, -1 IF BAD DATA
    def calcGpsPosition(self,gps_point0):
        gps_point = distance.getCoor(gps_point0)
        return gps_point


    #WAYPOINT MATCHING USING GPS DATA
    #RETURN: 0 IF WITHIN 5FT, 1 WITHIN 10FT, 2 MORETHAN 10FT,AND -1 BAD DATA
##    def atGpsWaypoint(gw):
##        updateGps()
##        if nmea.satellites > 6:
##            if distance.havDistance([nmea.lat,nmea.lon], gw) < 6  :
##                return 0
##            if distance.havDistance([nmea.lat,nmea.lon], gw) < 11  :
##                return 1
##            return 2
##        return -1
##
##    def compareLocation():
##        gps_point = calcGpsPosition()
##        if gps_point != -1:
##            current_point = calcPosition()
##            current_point_hypot = math.hypot(current_point[0],current_point[1])
##            gps_point_hypot = math.hypot(gps_point[0],gps_point[1])
##            point_diff = math.fabs(current_point_hypot - gps_point_hypot)
##            return point_diff
##        return -1

##p1 = [3246.6417,11704.2338]
##p2 = [3246.6428,11704.2037]
##gps_data = gps(2, p1,90)
##print gps_data.distance, " " ,gps_data.direction