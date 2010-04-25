import dead_reckon

class pathFind:
    def __init__(self):
        #Points we are shooting for
        self.x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
        self.y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]
        self.waypoints = zip(x,y)

        self.current_point = ()

        self.waypoint_count = 0
        self.beacon_count = 1

    def goTowardsNewDestination(sd):
        #this gets called when we need to calculate the next stop we should go to
        #Decide how to get there
        motor.goDir(STOP)
        dr_current_point = dead_reckon.calcPosition(sd)
        
        #Find distance and bearing to next position
        distance = (current_point, next_waypoint)
        angle = (current_point, next_waypoint) 

        motor.goFeet(distance)
        motor.turn(angle)
        motor.goDir(FORWARD)

        return

    #waypoint matching using dead-reckoning
    #return: 0 if not, 1 if at waypoint
    def atWaypoint(self,sd):
        last_waypoint = self.waypoints[self.waypoint_count]
        next_waypoint = self.waypoints[self.waypoint_count + 1]
        #This is NOT the end all, be all to waypoint detection, this is the dead reckoning and compass portion. 
        current_point = dead_reckon.calcPosition(sd)
        #we have to use dead reckoning and compass information in order to get a good idea of where we have gone
        if abs(next_waypoint[0] - last_waypoint[0]) > abs(next_waypoint[1] - last_waypoint[1]):
            if current_point[0] > next_waypoint[0]:
                return 1 
        else:
            if current_point[1] > next_waypoint[1]:
                return 1
        return 0
