# Introduction #

After Tummula's less than enthusiastic response to our robot's navigation goals, I have concluded that the main issue was that I was not clear enough with how we will achieve some of the concepts that I have put out there.

I'm a firm believer that a true master of his/her domain should be able to explain his/her thoughts so clearly and simply that even their own grandmother would be able to understand.

This is a list of conceptual ideas that may be amended(possibly several times through development)

Please leave comments/ask questions if something does not make sense or raises concern. My grandma should understand this stuff, so if an engineer doesn't, it's my fault, not yours.


# Details #
  * This is what our points will look like in the code... point A corresponds to x`[0`],y`[0`], point B x`[1`],y`[1`], etc:
```
 28     x = [283,428,428,246,204,179,167,62,69,75,109,68,100,76,59]
 29     y = [61,79,214,230,244,269,308,309,142,110,93,84,70,61,40]
```
  * Our robot is moving from point A to point B, linearly. That is, in a straight line. There will be several points along the course. Once robot reaches point B, robot will look at which angle it needs to go in order to reach point C. The robot is going to stop completely, turn until the compass reading corresponds to our computed angle, and then move straight ahead.

  * Well this raises the question. How does it know that it reaches point B in the first place? In our code, we calculate the distance between point A and point B. We have two separate ways of figuring out how far we've gone on the bot, dead reckoning and gps. We will continually be using dead reckoning in order to get an idea of how far we have gone. We will use gps also to compute the distances between. We also will know what direction we should be heading in with the compass. We will check against all 3 of this values to make an educated guess as to where we are on the course, and if we are at our checkpoint. If everything is perfect(or close to perfect) at the check point, we will clear out our data, and prepare for our journey to point C. If things are not perfect, we will choose the most reliable data to use or some sort of average between them. This will be determined by trial and error prior to the race.

  * `[I FEEL LIKE THIS PART IS TOO COMPLICATED, SIMPLIFY PLEASE`]The main idea here is that we should be able to navigate most of the course using the above method. However, we will also have the beacons. We will be able to use the beacons as checkpoints. 48 hrs should be ample time to plug in their coordinates into our code. This gives us a 4th piece of sensor data to use for our plotting scheme. For example, if we lock on to a beacon while on the course, we can calculate what direction that beacon is coming from. If this matches up with our calculated approximation of where we think we are, we can be confident in continuing on with our predestined route. However, if it is blatantly wrong, we can either try to rectify our approximation or if things are horrendously wrong, we can override the predestined path until we reach the beacon. At that point we can recalibrate.

  * In short, if we are completely lost, and none of our calculations from the sensor data vs. what we should be seeing on the bot are adding up, we will need to rely on the beacon to guide us.

  * The robot will work completely linearly. That is, it will never move at an angle. This is to simplify coding/remove possibilities for error. I see no reason to potentially jeopardize our algorithms in an attempt to shave off a few seconds.