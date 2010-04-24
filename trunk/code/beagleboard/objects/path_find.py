import dead_reckon

class pathFind:
    def __init__(self):
        #Points we are shooting for
        self.x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
        self.y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
        self.waypoints = zip(x,y)

        self.waypoint_count = 0
        self.beacon_count = 1

    def goTowardsNewDestination():
        #this gets called when we need to calculate the next stop we should go to
        #Decide how to get there
        motor.goDir(STOP)
        dr_current_point = dead_reckon.calcPosition()
        
        #Find distance and bearing to next position
        distance = (current_point, next_waypoint)
        angle = (current_point, next_waypoint) 

        motor.goFeet(distance)
        motor.turn(angle)
        motor.goDir(FORWARD)

        return

    #waypoint matching using dead-reckoning
    #return: 0 if not, 1 if at waypoint
    def atWaypoint(wp):
        current_point = calcPosition()
        if (math.hypot(current_point[0] + current_point[1]) == math.hypot(wp[0] + wp[1])):
            return 1
        return 0
