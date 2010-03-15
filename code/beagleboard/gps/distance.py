#!/usr/bin/python
import math

def toDec(a):
    return a[0] + (a[1] * 1/60) + (a[2] * 1/60 * 1/60)

def getDir(lat1, lon1, lat2, lon2):
    return (lat2 - lat1)/(lon2 - lon1)

#lat2 and lon2 can always be the checkmarks
def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) \
        - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    return math.atan2(y, x)

#lat2 and lon2 can always be the checkmarks
def havDistance(lat1, lon1, lat2, lon2):
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = math.sin(dLat / 2) * math.sin(dLat / 2) \
        + math.cos(lat1) * math.cos(lat2) \
        * math.sin(dLon / 2) * math.sin(dLon / 2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 3963.19245606 * c * 5280
 

lat1 = [32, 46, 38.41]
lon1 = [117, 4, 12.83]

lat2 = [32, 46, 38.38]
lon2 = [117, 4, 12.39]

dlat1 = toDec(lat1)
dlon1 = toDec(lon1)
dlat2 = toDec(lat2)
dlon2 = toDec(lon2)

distance = havDistance(dlat1, dlon1, dlat2, dlon2)

print distance
print calcBearing(dlat1, dlon1, dlat2, dlon2)
