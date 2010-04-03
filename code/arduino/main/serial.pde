#include <Wire.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 

//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
const int LEFT_FLEX_PIN = 8;  
const int RIGHT_FLEX_PIN = 9;  
const int LEFT_ULTRASONIC_PIN= 6;   
const int RIGHT_ULTRASONIC_PIN = 7;

const int LEFT_BEACON_INT  = 0;   
const int RIGHT_BEACON_INT = 1; 

//Servo Constants
const int SERVO_PIN = 9;
const int HMC6352Address = 0x42;

//Beacon Constants
const int NA = -1;
const int STRAIGHT = 0;
const int LEFT = 1;
const int RIGHT = 2;


//*******************GLOBAL VARIABLES*****************// 

//For the compass
int slave_address;

//For the servo
Servo myservo;

//Servo Variables
//Should take out of global
int pos,back = 50;

//Beacon Specific Variables
int left_time, right_time = 0;
int beacon_dir;

//Our "protothreading"
Metro serialMetro = Metro(250);
Metro servoMetro = Metro(10);

void setup() {
  //Serial Communication
  Serial.begin(9600);  

  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slave_address = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI

  //For the compass(I2C communication)
  Wire.begin();

  //Telling which pin the servo is on. 
  myservo.attach(SERVO_PIN);

  //Interrupts for the Beacons. 
  attachInterrupt(LEFT_BEACON_INT, left_beacon, CHANGE);
  attachInterrupt(RIGHT_BEACON_INT, right_beacon, CHANGE);
}

void loop() {
    int left_us_val, left_flex_val, right_us_val, right_flex_val,compass_val = 0;

    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
        //get information
        left_us_val       = ultrasonic(LEFT_ULTRASONIC_PIN);
        right_us_val      = ultrasonic(RIGHT_ULTRASONIC_PIN);
        left_flex_val     = flex(LEFT_FLEX_PIN);
        right_flex_val    = flex(RIGHT_FLEX_PIN);
        compass_val       = compass();

        //send serial info
        sendSerialInfo(left_us_val, left_flex_val,right_us_val, right_flex_val,compass_val);

        serialMetro.reset();
    }
    
    if (servoMetro.check() == 1) { // check if the metro has passed it's interval .
        //This needs fixed up
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

        myservo.write(pos);              // tell servo to go to position in variable 'pos'    

        servoMetro.reset();
    }
}

int ultrasonic(int pin) {
    //Used to read in the pulse that is being sent by the MaxSonar device.
    //Pulse Width representation with a scale factor of 147 uS per Inch.
    //Will package in Inches for now
    long pulse, inches;
    
    pinMode(pin, INPUT);
    pulse = pulseIn(pin, HIGH);
    inches = pulse/147;

    return inches;
}

int flex(int pin) {
    int sensor_value = 0;
    // read the value from the sensor:
    sensor_value = analogRead(pin);       
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

void sendSerialInfo(int us_val, int flex_val,int right_us_val, int right_flex_val,int compass_val)
{
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
  Serial.print("<left>");
  Serial.print(left_flex_val);
  Serial.print("</left>");
  Serial.print("<right>");
  Serial.print(right_flex_val);
  Serial.print("</right>");
  Serial.println("</flex>");
  Serial.print("<ultrasonic>");
  Serial.print("<left>");
  Serial.print(left_us_val);
  Serial.print("</left>");
  Serial.print("<right>");
  Serial.print(right_us_val);
  Serial.print("    </right>");
  Serial.println("</ultrasonic>");
  Serial.print("<beacon>");
  Serial.print(beacon_dir);
  Serial.println("</beacon>");
  Serial.print("<wheelencoder>");
  Serial.print("???");
  Serial.println("</wheelencoder>");
  Serial.println("</sensor>");
  Serial.println("");
  return;
}

void left_beacon() {
	int diff;
	left_time = millis();
	beacon_dir = NA;
	if(right_time) {
		if((left_time - right_time) > 100) {  
			beacon_dir = RIGHT;
		}
		else {
			beacon_dir = STRAIGHT;
		}

		right_time = 0;
		left_time = 0;
	}
}

void right_beacon() {
	int diff;
	right_time = millis();
	beacon_dir = NA;
	if(left_time){
		if((right_time - left_time) > 100) {
			beacon_dir = LEFT;
		}		
		else {
			beacon_dir = STRAIGHT;
		}	

		left_time = 0;
		right_time = 0;
	}
}	
