#!/usr/bin/python
import math
from numpy import *

def toDec(num):
    #parse first, ick
    a = math.floor(num/100)
    b = math.floor(num) % 100
    c = ((num * 10000) % 10000)/100 
    return a + (b * 1/60) + (c * 1/60 * 1/60)


def havDistance(pnt1, pnt2):
    dLat = pnt2[0] - pnt1[0]
    dLon = pnt2[1] - pnt1[1]
    a = math.sin(dLat / 2) * math.sin(dLat / 2) \
        + math.cos(pnt1[0]) * math.cos(pnt2[0]) \
        * math.sin(dLon / 2) * math.sin(dLon / 2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 3963.19245606 * c * 5280
 

day_one = [(3246.6417,11704.2338),
(3246.6531,11704.2099),
(3246.6308,11704.2030),
(3246.6266,11704.2334),
(3246.6290,11704.2406),
(3246.6373,11704.2594),
(3246.6351,11704.2575),
(3246.6355,11704.2555),
(3246.6443,11704.2504)]

day_two = [(3246.6441,11704.2314),
(3246.6419,11704.2028),
(3246.6270,11704.1983),
(3246.6237,11704.2326),
(3246.6153,11704.2389),
(3246.6335,11704.2544),
(3246.6410,11704.2547),
(3246.6485,11704.2512),
(3246.6500,11704.2502)]

day_three = [(3246.6526,11704.2397),
(3246.6428,11704.2037),
(3246.6350,11704.1956),
(3246.6224,11704.2317),
(3246.6306,11704.2410),
(3246.6386,11704.2534),
(3246.6432,11704.2544),
(3246.6453,11704.2517),
(3246.6470,11704.2503)]

day_four = [(3246.6437,11704.2315),
(3246.6444,11704.2038),
(3246.6286,11704.1981),
(3246.6263,11704.2306),
(3246.6196,11704.2418),
(3246.6329,11704.2531),
(3246.6383,11704.2534),
(3246.6407,11704.2533)]

day_five = [(3246.6472,11704.2303),
(3246.6414,11704.2013),
(3246.6302,11704.1978),
(3246.6266,11704.2309),
(3246.6204,11704.2412),
(3246.6336,11704.2527),
(3246.6373,11704.2515),
(3246.6406,11704.2530),
(3246.6431,11704.2496)]

gps_data = []
gps_data.append(day_one)
gps_data.append(day_two)
gps_data.append(day_three)
gps_data.append(day_four)
gps_data.append(day_five)

dec_gps_data = []
tmp = []

#change from degrees to decimal ugh
for i in range(len(gps_data) - 1):
    for j in range(len(gps_data[i]) - 1):
        tmp.append((toDec(gps_data[i][j][0]),toDec(gps_data[i][j][1]))) 
    dec_gps_data.append(tmp)
    tmp = []

gps_data = dec_gps_data

#We need standard deviation, distance calculation, standard deviation of that, degree difference, standard deviation of that
#First we need the differences between points for each date and points
#print gps_data[0][0][0] - gps_data[0][1][0],gps_data[1][0][0] - gps_data[1][1][0] 

diff_table = [] 
big_diff_table = [] 

for i in range(len(gps_data) - 1):
    for j in range(len(gps_data[i]) - 1):
        diff_table.append([(gps_data[i][j][0] - gps_data[i][j+1][0],gps_data[i][j][1] - gps_data[i][j+1][1])])

    big_diff_table.append(diff_table)
    diff_table = []

#print big_diff_table[0][0], big_diff_table[1][0]

#for i in big_diff_table:
    #print i[0]

print havDistance(gps_data[0][0],gps_data[0][1])
#print gps_data[0][0],gps_data[0][1]
