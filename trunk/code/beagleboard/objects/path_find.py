import setup
from defines import * 
import dead_reckon
import computations as comp
import math

class pathFind:
    def __init__(self):
        #Points we are shooting for
        if setup.DEAD_RECKON_TEST:
            self.x = [0, 20, 0]
            self.y = [0, 0, 0]
        else:
            self.x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
            self.y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]

        self.waypoints = zip(self.x,self.y)

        self.current_point = ()

        self.waypoint_count = 0
        self.beacon_count = 1

    def lastWaypoint(self):
        if self.waypoint_count == len(self.waypoints) - 1:
            return 1
        return 0

    def goTowardsNewDestination(self,sd):
        #this gets called when we need to calculate the next stop we should go to
        #Decide how to get there
        commands = []

        if self.waypoint_count == len(self.waypoints) - 1:
            return -1

        last_waypoint = self.waypoints[self.waypoint_count]
        next_waypoint = self.waypoints[self.waypoint_count + 1]

        commands.append(('go',0,STOP)) 
        dr_current_point = dead_reckon.calcPosition(sd,self.waypoints, self.waypoint_count)
        self.current_point = dr_current_point

        #Find distance and bearing to next position
        distance = comp.calcDistance(self.current_point, next_waypoint)
        angle = comp.calcAngle2(self.current_point, next_waypoint) 

        if angle > 1.1:
            commands.append(('turn', RIGHT, angle)) 

        commands.append(('go',distance,FORWARD)) 
        return commands 


    #waypoint matching using dead-reckoning
    #return: 0 if not, 1 if at waypoint
    def atWaypoint(self,sd):
        last_waypoint = self.waypoints[self.waypoint_count]
        next_waypoint = self.waypoints[self.waypoint_count + 1]
        #This is NOT the end all, be all to waypoint detection, this is the dead reckoning and compass portion. 
        self.current_point = dead_reckon.calcPosition(sd,self.waypoints, self.waypoint_count)
        #we have to use dead reckoning and compass information in order to get a good idea of where we have gone
        if abs(next_waypoint[0] - last_waypoint[0]) > abs(next_waypoint[1] - last_waypoint[1]):
            if current_point[0] > next_waypoint[0]:
                return 1 
        else:
            if current_point[1] > next_waypoint[1]:
                return 1
        return 0

    def getCurrentPoint(self,sd):
        if self.waypoint_count == len(self.waypoints) - 1:
            return -1

        self.current_point = dead_reckon.calcPosition(sd,self.waypoints, self.waypoint_count) 
        return self.current_point
