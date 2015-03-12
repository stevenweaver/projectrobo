# Introduction #
The arduino is surprisingly pleasant to work with. These are some notes for the code.


# Details #

The main code is in serial called serial.pde. This will interface with all of the sensors we are receiving.

### FLEX ###
The flex pin corresponds to Analog IN 0

For the flex sensors, you need to use a voltage divider. (Very much like project 2 of the senior lab).

Picture:
![http://mjpa.co.uk/screenshots/voltage_divider.png](http://mjpa.co.uk/screenshots/voltage_divider.png)

The flex sensor standing up is 8k, bent it was something like 20k.

using 15k resistor

| **Flex** | **standing up** | **something bad is happening** |**emergency** | **OMG WTF we're dead** |
|:---------|:----------------|:-------------------------------|:-------------|:-----------------------|
| 1 | 653 | <570 | <500 | <450 |
| 2 | 603 | <530 | <450 | <400 |


### SONAR ###

The sonar sensor corresponds to pin 7 of the PWM side.

### COMPASS ###
For the compass. You must use pins 20 and 21 under Communication. pin 20 is for the data pin SDA and 21 is for SCL, as marked.

### BEACON ###
The beacon needs to be on a pin that is on an interrupt.

External Interrupts: 2 (interrupt 0), 3 (interrupt 1), 18 (interrupt 5), 19 (interrupt 4), 20 (interrupt 3), and 21 (interrupt 2). These pins can be configured to trigger an interrupt on a low value, a rising or falling edge, or a change in value. See the attachInterrupt() function for details.

CAVEAT: If you use interrupts 2-5 you need to enable the pull-up resistor first.

Use the ground that is on the same Header(The PWM side). Digital Pin 2 is on the PWM header row as well.

You'll see it work by using this code:

```
int pin = 13;
volatile int state = HIGH;

void setup()
{
 pinMode(pin, OUTPUT);
 digitalWrite(pin, state);
 attachInterrupt(0, blink, CHANGE);
}

void loop()
{
 //digitalWrite(pin, state);
 //do nothing
}

void blink()
{
 digitalWrite(pin, LOW);
}

```

The led labeled 13 on the arduino will turn off once you trip the sensor.