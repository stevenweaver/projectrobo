#!/usr/bin/python
import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

def toDec(a):
    return a[0] + (a[1] * 1/60) + (a[2] * 1/60 * 1/60)

def getDir(lat1, lon1, lat2, lon2):
    return (lat2 - lat1)/(lon2 - lon1)
 
lat1 = [32, 46, 38.41]
lon1 = [117, 4, 12.83]

lat2 = [32, 46, 38.38]
lon2 = [117, 4, 12.39]

dlat1 = toDec(lat1)
dlon1 = toDec(lon1)
dlat2 = toDec(lat2)
dlon2 = toDec(lon2)

arc = distance_on_unit_sphere(dlat1, dlon1, dlat2, dlon2)
miles = 3963.19245606
feet = miles * 5280 * arc

print getDir(dlat1, dlon1, dlat2, dlon2)
#print feet 

#Calculate distance nd degree   
