#Personal notes for steven, don't peek!

# Introduction #




# Details #
  * Try using analog input for beacon sensors. It should read something like 0 compared to something like 500. I must have somehow made a mistake the last time i tried it.
  * Having a slight problem with parsing NMEA data from ali. need to figure out wtf.


# Beacon #
Have two interrupts, one for each beacon. When one interrupt is asserted, start a timer. When the the other interrupt engages, check the timer.

If the timer has a small value, then the beacon is straight ahead.

Have a time out.