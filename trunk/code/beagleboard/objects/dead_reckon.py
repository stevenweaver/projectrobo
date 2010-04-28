import computations as comp
import math

def calcPosition(sd,waypoints, waypoint_count):

    #we can guess at the direction we are going by just calculating the degree difference between our two points
    last_waypoint = waypoints[waypoint_count]
    next_waypoint = waypoints[waypoint_count + 1]

    #we have to use dead reckoning and compass information in order to get a good idea of where we have gone
    if abs(next_waypoint[0] - last_waypoint[0]) > abs(next_waypoint[1] - last_waypoint[1]):
        rev_orientation = 0 
    else:
        rev_orientation = 1

    #calculate the distance 
    angle = comp.calcAngle(next_waypoint, last_waypoint)
    deg_angle = math.degrees(angle)

    #we know the hypotenuse is motor1_ft and we know the angle we should be going, so we should be able to estimate our point 
    #these should be more or less equal, so i'm going to use one for now
    motor1_ft = sd[0].ft['right']  
    motor2_ft = sd[0].ft['left']  

    if rev_orientation:
        delta_x = math.sin(angle) * motor1_ft
        delta_y = math.cos(angle) * motor1_ft
    else:
        delta_y = math.sin(angle) * motor1_ft
        delta_x = math.cos(angle) * motor1_ft

    if rev_orientation:
        if next_waypoint[1] < last_waypoint[1]: 
            current_point = ((last_waypoint[0] + delta_x),(last_waypoint[1] - delta_y))
        else:
            current_point = ((last_waypoint[0] + delta_x),(last_waypoint[1] + delta_y))

    else: 
        if next_waypoint[0] < last_waypoint[0]: 
            current_point = ((last_waypoint[0] - delta_x),(last_waypoint[1] - delta_y))
        else:
            current_point = ((last_waypoint[0] + delta_x),(last_waypoint[1] + delta_y))
    
    return current_point
