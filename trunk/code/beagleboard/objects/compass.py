#Compass
def checkCompass(desired_degree, sd):
    #Make sure we have a decent sample rate
    #Reply back with veering right, veering left, going straight
    sum = 0
    if abs(sd[8].compass - desired_degree) > 10:
        #TODO:Make sure it's not a blip
        if len(sd) >= 10: 
            for i in range(10):
                #Sum up the differences
                if i > 0:
                    sum+= abs(sd[i].compass - desired_degree + 360) % 360

            avg = sum/10
            print "avg: " + str(avg)
            if avg > 180:
                #Veering off left 
                print "compass veering left"
                return 1 
            elif avg > 20:
                #Veering off right 
                print "compass veering right"
                return 1 
            else:
                #Going straight enough
                print "compass going straight"
                return 0 
    else:
        print "compass going straight"


