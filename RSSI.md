# Introduction #




# Details #

  * TX: 8n1, 19200 bps
  * RF INT: Low pulse on RF interrupt
  * RSSI PWM: 1.960 kHz
  * ID2-ID0: Binary Beacon Value 1-5
  * VCC: 5-9V regulated to 3.3V

Pin 8 TX: This is the serial data, this may be the optimum way of reading the information from the RSSI receiver. It will have a hexadecimal number indicating how far the beacon is, and what the beacon number is. We probably should hook this up straight to the beagleboard.

Pin 7: This works the same way as the PWM with the US sensors, however, the kHz will have to change. We may not have to use this.

Pins 4-2: ID2-ID0, this will tell you the number of the pin you are receiving. ID0 with a 1 corresponds to beacon 1

Pin 2: GND

Pin 1: Vcc 5-9v