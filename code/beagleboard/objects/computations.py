#TWO DEAD RECONING DISTANCE CALCUATION
def calcDistance(pt1, pt2):
    return  math.sqrt(math.pow((pt2[0] - pt1[0]),2)+math.pow((pt2[1] - pt1[1]), 2))
 
def calcAngle(pt1, pt2):
    #now we need to find angle A, since we know sinA is height/distance we can just find the inverse sine 
    distance = calcDistance(pt1, pt2)
    if abs(pt2[0] - pt1[0]) > abs(pt2[1] - pt1[1]):
        diff = pt2[1] - pt[1]
    #Else we want to calculate the difference in x
    else:
        diff = pt2[0] - pt[0] 
    #Calculate the angle
    return math.asin(diff/distance) 

#Unsure of the use of this
#We can have this computed beforehand
def computeCourse(x,y): 
    #every point on the course
    #not sure if we need this, maybe for timing
    for i in range(len(x) - 1):
        if abs(x[i+1] - x[i]) > abs(y[i+1] - y[i]):
            for j in range(abs(x[i+1]-x[i])):
                if x[i+1] < x[i]:
                    xc = x[i] - j
                else:
                    xc = x[i] + j
                    yc = y[i] + (xc-x[i])*(y[i+1] - y[i])/(x[i+1] - x[i]) 

    else:
        for j in range(abs(y[i+1]-y[i])):
            if y[i+1] < y[i]:
                yc = y[i] - j
            else:
                yc = y[i] + j
            xc = x[i] + (yc-y[i])*(x[i+1] - x[i])/(y[i+1] - y[i]) 
