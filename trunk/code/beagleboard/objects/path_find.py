import setup
from defines import * 
import dead_reckon
import computations as comp
import math

class pathFind:
    def __init__(self):
        #Points we are shooting for
        if setup.DEAD_RECKON_TEST:
            self.x = [125,130,130,125,125]
            self.y = [170,170,175,175,170]
        else:
            self.x = [125, 256, 294, 85, 85, 80, 75, 75, 60, 60, 16, 16, 8, 8, 48, 48, 10, 10, 44, 10, 33]
            self.y = [170, 170, 66, 66, 55, 50, 50, 42, 42, 10, 10, 87, 87, 120, 127, 135, 135, 140, 150, 152, 167]

        self.waypoints = zip(self.x,self.y)
        self.current_orientation = 0
        self.current_point = ()

        self.waypoint_count = 0
        self.beacon_count = 1

    def lastWaypoint(self):
        if self.waypoint_count == len(self.waypoints) - 1:
            return 1
        return 0

    def goTowardsNewDestination(self,sd,sensors):
        #this gets called when we need to calculate the next stop we should go to
        #Decide how to get there

        #current_orientation = sd[0].compass[0]
        commands = []

        if self.waypoint_count == len(self.waypoints) - 1:
            return -1

        current_waypoint = self.waypoints[self.waypoint_count]
        next_waypoint = self.waypoints[self.waypoint_count + 1]

        #commands.append(('go',0,STOP)) 
        dr_current_point = dead_reckon.calcPosition(sd,self.waypoints, self.waypoint_count)
        self.current_point = dr_current_point
        distance23 = comp.calcDistance(self.current_point, next_waypoint)

        if self.waypoint_count >= 1:
            last_waypoint = self.waypoints[self.waypoint_count - 1]
            #Find distance and bearing to next position
            distance12 = comp.calcDistance(last_waypoint, self.current_point)
            distance13 = comp.calcDistance(last_waypoint, next_waypoint)
            angle = math.degrees(math.acos((math.pow(distance23,2) - math.pow(distance12,2) - math.pow(distance13,2))/(2*distance12*distance13)))
            print "angle: " + str(angle)

        else:
            angle = comp.calcAngle2(self.current_point, next_waypoint) 
            print "angle:" + str(angle)

        #In order to get the real angle, we are going to have to know the current orientation of the robot
        if angle > 1.1:
            commands.append(('turn', RIGHT, angle)) 
        else:
            commands.append(('turn', RIGHT, 0)) 

        distance = distance23
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
