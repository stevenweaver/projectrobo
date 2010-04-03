#include <Wire.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 

#include <motor_driver.h>
#include <PID_Beta6.h>

//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
const int LEFT_FLEX_PIN = 8;  
const int RIGHT_FLEX_PIN = 9;  
const int LEFT_ULTRASONIC_PIN= 6;   
const int RIGHT_ULTRASONIC_PIN = 7;

const int LEFT_BEACON_INT  = 0;  //Interrupt 0 
const int RIGHT_BEACON_INT = 1;  //Interrupt 1  

//Servo Constants
const int SERVO_PIN = 9;
const int HMC6352Address = 0x42;

//Beacon Constants
const int NA = -1;
const int STRAIGHT = 0;
const int LEFT = 1;
const int RIGHT = 2;

//MOTORS

MOTOR_A_ENABLE = 9;
MOTOR_A_CONTROL1 = 8;
MOTOR_A_CONTROL2 = 10;
//MOTOR_A_ENCODER = 2; //INT 0 (no need to define
// wont be used directly)

MOTOR_B_ENABLE = 12;
MOTOR_B_CONTROL1 = 11;
MOTOR_B_CONTROL2 = 13;
//MOTOR_B_ENCODER = 3; //INT 1

// PID parameters for each motor
// might have morse set for different situations
PID_P_A   30
PID_I_A   0
PID_D_A   0.4
PID_P_B   30
PID_I_B   0
PID_D_B   0.4

// range of input = ticks and output = pwm 
PID_A_INPUT_MIN    0
PID_A_INPUT_MAX    20000
PID_A_OUTPUT_MIN   20
PID_A_OUTPUT_MAX   255
PID_B_INPUT_MIN    0
PID_B_INPUT_MAX    20000
PID_B_OUTPUT_MIN   20
PID_B_OUTPUT_MAX   255

// the desired distance in ticks 
// can be converted 197 ticks = 1 revolution = 2 feet
SETPOINT   1000

/*******************GLOBAL VARIABLES*****************// 

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

//Motors
Motor_Driver Motor_Driver(MOTOR_A_ENABLE, MOTOR_A_CONTROL1, MOTOR_A_CONTROL2,MOTOR_B_ENABLE, MOTOR_B_CONTROL1, MOTOR_B_CONTROL2);

//Wheel Encoding
volatile int clicks_a = 0; 
volatile int clicks_b = 0; 

int done = 0;

//PID stuff
double Setpoint, Input_A, Input_B, Output_A, Output_B;

//Please set constants, no magic numbers
PID PID_A(&Input_A, &Output_A, &Setpoint,30,0,.4);
PID PID_B(&Input_B, &Output_B, &Setpoint,30,0,.4);
unsigned long StartTime;


//Our "protothreading"
Metro serialMetro = Metro(250);
Metro servoMetro = Metro(10);
Metro goRightMetro = Metro(10000);
Metro motorMetro = Metro(2200);


//*******************SETUP*****************// 
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

  //Interrupts for Wheel encoders
  attachInterrupt(MOTOR_A_ENCODER, motor_a_tick, FALLING);    
  attachInterrupt(MOTOR_B_ENCODER, motor_b_tick, FALLING); 


  //PID STUFF I NEED TO FIGURE OUT
  PID_A.SetInputLimits(0,20000);
  PID_A.SetOutputLimits(20,255);
  
  PID_B.SetInputLimits(0,20000);
  PID_B.SetOutputLimits(20,255);
  //  //initialize the variables we're linked to
  Input_A = clicks_a;
  Input_B = clicks_b;
 
  Output_A = 0;
  Output_B = 0;
  //turn the PID on
  PID_A.SetMode(AUTO);
  PID_B.SetMode(AUTO);
  StartTime = millis();
  
  
  // we are in forward mode
  Motor_Driver.Forward();
  Setpoint = 1000;
}

//*******************MAIN*****************// 
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

    if (goRightMetro.check() == 1 && done == 1) { // check if the metro has passed it's interval .
        Motor_Driver.Right();
        analogWrite(MOTOR_A_ENABLE, 60);
        analogWrite(MOTOR_B_ENABLE, 60);
    } 

    else 
    {
        Input_A = clicks_a;
        Input_B = clicks_b;

        if (motorMetro.check() == 1 && done == 1) { // check if the metro has passed it's interval .
            PID_A.SetOutputLimits(20,60);
            PID_B.SetOutputLimits(15,50);
        }
        else  {
            PID_A.SetOutputLimits(20,140);
            PID_B.SetOutputLimits(10,120);
        }

        //Set Tuning Parameters based on how close we are to setpoint
        //if(abs(Setpoint-Input_B)<200)  PID_B.SetOutputLimits(15,240);;  //aggressive
        //else myPID.SetTunings(3,4,1); //comparatively moderate
        PID_A.Compute();
        PID_B.Compute();


        analogWrite(MOTOR_A_ENABLE, Output_A);
        analogWrite(MOTOR_B_ENABLE, Output_B);


        Serial.print("Current input A: ");
        Serial.println(Input_A);
        Serial.print("Current output A: ");
        Serial.println(Output_A);


        Serial.print("Current input B: ");
        Serial.println(Input_B);
        Serial.print("Current output B: ");
        Serial.println(Output_B);
   }
}

//***************SENSOR FUNCTIONS***************//

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


//*************CREATE XML FOR BEAGLEBOARD************//
void sendSerialInfo(int us_val, int flex_val,int right_us_val, int right_flex_val,int compass_val)
{
  //Serial.println("Content-Type: text/xml");
  //Serial.println("Content-length: 83");
  Serial.println("<?xml version=\"1.0\"?>");
  Serial.println("<sensor>");
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


//INTERRUPTS//
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


void motor_a_tick() 
{   
  clicks_a++; 
}   

void motor_b_tick() 
{ 
  clicks_b++;        
}
