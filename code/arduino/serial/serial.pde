//This uses a voltage divider. Put into analog
const int FLEX_PIN = 0;  // select the input pin for flex sensor 
const int ULTRASONIC_PIN = 7;    // select the input pin for ultransonic range sensor 
const int MAXLEN = 255;
const int HMC6352Address = 0x42;


#include <Wire.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 

// This is calculated in the setup() function, therefore global
int slave_address;
Servo myservo;
Metro serialMetro = Metro(250);
Metro servoMetro = Metro(10);
int pos,back = 50;

void setup() {
  Serial.begin(9600);  
  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slave_address = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI
  Wire.begin();
  myservo.attach(9);
}

void loop() {
    int us_val, flex_val,compass_val = 0;
    
    //To use an interrupt: 
    //http://www.arduino.cc/en/Reference/AttachInterrupt
    //attachInterrupt(0, blink, CHANGE);

    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
      //send information
      //us_val = ultrasonic();
      //flex_val = flex();
      //compass_val = compass();
      sendSerialInfo(us_val, flex_val,compass_val);
      serialMetro.reset();
    }
    
    if (servoMetro.check() == 1) { // check if the metro has passed it's interval .
      if(pos >= 180) {
       back = 1; 
      }
      else if(pos <= 0) {
       back = 0; 
      }
      if(back == 0)
        pos = pos+1;     
      else
        pos = pos-1;    
      Serial.print("pos: ");
      Serial.println(pos);
      myservo.write(pos);              // tell servo to go to position in variable 'pos'    
      servoMetro.reset();
    }
  }

int ultrasonic() {
    //Used to read in the pulse that is being sent by the MaxSonar device.
    //Pulse Width representation with a scale factor of 147 uS per Inch.
    //Will package in Inches for now
    long pulse, inches;
    
    pinMode(ULTRASONIC_PIN, INPUT);
    pulse = pulseIn(ULTRASONIC_PIN, HIGH);
    inches = pulse/147;

    return inches;
}

int flex() {
    int sensor_value = 0;
    // read the value from the sensor:
    sensor_value = analogRead(FLEX_PIN);       
    return sensor_value;
}

int compass() {
    byte heading_data[2];
    int i, heading_value;
    
    // Send a "A" command to the HMC6352
    // This requests the current heading data
    Wire.beginTransmission(slave_address);
    Wire.send("A");              // The "Get Data" command
    Wire.endTransmission();
    delay(10);                   
    
    // The HMC6352 needs at least a 70us (microsecond) delay
    // after this command.  Using 10ms just makes it safe
    // Read the 2 heading bytes, MSB first
    // The resulting 16bit word is the compass heading in 10th's of a degree
    // For example: a heading of 1345 would be 134.5 degrees
    
    Wire.requestFrom(slave_address, 2);        // Request the 2 byte heading (MSB comes first)
    i = 0;
    
    while(Wire.available() && i < 2)
    { 
      heading_data[i] = Wire.receive();
      i++;
    }
    heading_value = heading_data[0]*256 + heading_data[1];  // Put the MSB and LSB together
    return heading_value;
}

void sendSerialInfo(int us_val, int flex_val,int compass_val)
{
  //This is an absolutely disgusting way of doing it, but to do it right takes too long, i couldn't find an xml-rpc lib, and this works. 
  //Serial.println("Content-Type: text/xml");
  //Serial.println("Content-length: 83");
  Serial.println("<?xml version=\"1.0\"?>");
  Serial.println("<sensor>");
  Serial.print("<gps>");
  Serial.print("???");
  Serial.println("</gps>");
  Serial.print("<compass>");
  Serial.print(int (compass_val / 10));     // The whole number part of the heading
  Serial.print(".");
  Serial.print(int (compass_val % 10));     // The fractional part of the heading
  Serial.print(compass_val);
  Serial.println("</compass>");
  Serial.print("<flex>");
  Serial.print(flex_val);
  Serial.println("</flex>");
  Serial.print("<ultrasonic>");
  Serial.print(us_val);
  Serial.println("</ultrasonic>");
  Serial.print("<beacon>");
  Serial.print("???");
  Serial.println("</beacon>");
  Serial.print("<wheelencoder>");
  Serial.print("???");
  Serial.println("</wheelencoder>");
  Serial.println("</sensor>");
  Serial.println("");
  return;
}
