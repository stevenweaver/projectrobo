import setup
import rssi
import motor

def goTowardsBeacon(sd):
    #Check if the Beacons are within range
    pos.append(sd.beacon)
    arr = np.array(pos)
    mean = arr.mean() 
    std = arr.std()

    if mean < 85 and std < 5:
        motor.turn(right, mean)
        motor.goDir(FORWARD)

    elif mean > 95 and std < 5:
        #Turn left
        motor.turn(left, mean - 90)
        motor.goDir(FORWARD)

    elif mean > 85 and mean < 95 and std < 5:
        #Turn right 
        motor.goDir(FORWARD)

    if len(pos) > 10:
        del pos[0]

    return 1

#FIND IF THE BEACON IN RANGE
# RETURN 4 ~= 40FT, 3 ~=(20-40)FT, 2 ~= (10-20)FT, 1 ~= (3-10)FT
#       0 IS UNDER THE BEACON, -1 IF NOT DETECTED
def beaconDetect(rssi_d):
    if rssi_d.RxNumber == beacon_count:
        return rssi.rx_distance()
    return -1
