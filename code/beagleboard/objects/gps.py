import nmea

class gps:
    def __init__(self):
    #Import the modules we need
    self.gps_waypoints = [[3246.6417,11704.2338],
                [3246.6428,11704.2037],
                [3246.6350,11704.1956],
                [3246.6224,11704.2317],
                [3246.6306,11704.2410]]

    #ROBOT LOCATION FROM GPS
    #RETURN: POINT IF GOOD DATA, -1 IF BAD DATA
    def calcGpsPosition():
        updateGps()
        if nmea.satellites > 6:
            gps_point = distance.getCoor([nmea.lat , nmea.lon])
            return gps_point
        return -1

    #GPS DISTANCE CALCUATION
    def calcGpsDistance(gw):
        updateGps()
        if nmea.satellites > 5:
            return distance.havDistance([nmea.lat , nmea.lon], gps_waypoint[gw])
        return -1

    ####################################
    ##LOCATING ROBOT AND DEAD-RECONING##
    ####################################
    #WAYPOINT MATCHING USING GPS DATA
    #RETURN: 0 IF WITHIN 5FT, 1 WITHIN 10FT, 2 MORETHAN 10FT,AND -1 BAD DATA
    def atGpsWaypoint(gw):
        updateGps()
        if nmea.satellites > 6:
            if distance.havDistance([nmea.lat,nmea.lon], gw) < 6  :
                return 0
            if distance.havDistance([nmea.lat,nmea.lon], gw) < 11  :
                return 1
            return 2
        return -1

    def compareLocation():
        gps_point = calcGpsPosition()
        if gps_point != -1:
            current_point = calcPosition()
            current_point_hypot = math.hypot(current_point[0],current_point[1])
            gps_point_hypot = math.hypot(gps_point[0],gps_point[1])
            point_diff = math.fabs(current_point_hypot - gps_point_hypot)
            return point_diff
        return -1


