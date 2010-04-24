#Compaass
def checkCompass(desired_degree):
    #Make sure we have a decent sample rate
    #Reply back with veering right, veering left, going straight
    sum = 0
    if abs(sd.compass[0] - desired_degree) > 10:
        #TODO:Make sure it's not a blip
        if len(sd) > 10: 
            for i in range(10):
                #Sum up the differences
                sum+= (sd.compass[0] - desired_degree + 360) % 360

            avg = sum/10
            if avg > 180:
                #Veering off left 
                return "left"
            elif avg > 3:
                #Veering off right 
                return "right"
            else:
                #Going straight enough
                return "good"

