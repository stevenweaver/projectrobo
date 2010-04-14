#include <Wire.h>
//#include <wiring.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 
#include <motor_driver.h>
#include <PID_Beta6.h>

//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
const int LEFT_FLEX_PIN = 0;  
const int RIGHT_FLEX_PIN = 1;  
const int LEFT_ULTRASONIC_PIN= 5;   
const int RIGHT_ULTRASONIC_PIN = 6;

const int LEFT_BEACON_INT  = 4;  //Interrupt 0 
const int RIGHT_BEACON_INT = 5;  //Interrupt 1  

//Servo Constants
const int SERVO_PIN = 4;
const int HMC6352Address = 0x42;

//Beacon Constants
const int NA = -1;
const int STRAIGHT = 0;
const int LEFT = 1;
const int RIGHT = 2;

//Direction Constants
const int STOP = -1;
const int FORWARD = 0;
//const int LEFT = 1;
//const int RIGHT = 2;

//MOTORS
const int MOTOR_RIGHT_ENABLE = 9;
const int MOTOR_RIGHT_CONTROL1 = 8;
const int MOTOR_RIGHT_CONTROL2 = 10;
const int MOTOR_RIGHT_ENCODER = 1; //INT 0 (no need to define// wont be used directly)

const int MOTOR_LEFT_ENABLE = 6;
const int MOTOR_LEFT_CONTROL1 = 5;
const int MOTOR_LEFT_CONTROL2 = 7;
const int MOTOR_LEFT_ENCODER = 0; //INT 1

//Receive data
#define MAXSIZE 8 
#define MAX_STRING 255 

// PID parameters for each motor
// might have morse set for different situations
const int PID_P_RIGHT = 30;
const int PID_I_RIGHT = 0;
const int PID_D_RIGHT = 0.4;
const int PID_P_LEFT = 30;
const int PID_I_LEFT = 0;
const int PID_D_LEFT = 0.4;

// range of input = ticks and output = pwm 
const int PID_RIGHT_INPUT_MIN =  0;
const int PID_RIGHT_INPUT_MAX =  20000;
const int PID_RIGHT_OUTPUT_MIN = 0;
const int PID_RIGHT_OUTPUT_MAX = 60;
const int PID_LEFT_INPUT_MIN =  0;
const int PID_LEFT_INPUT_MAX =  20000;
const int PID_LEFT_OUTPUT_MIN = 0;
const int PID_LEFT_OUTPUT_MAX = 60;

// the desired distance in ticks 
// can be converted 197 ticks = 1 revolution = 2 feet
const int SETPOINT = 1000;


const int TIME_LIMIT_1 = 1900;
const int TIME_LIMIT_2 = 5000;

/*******************GLOBAL VARIABLES*****************/

//For the compass
int slave_address;

//For the servo
Servo myservo;

//Servo Variables
//Should take out of global
int pos,back = 50;

//Beacon Specific Variables
volatile int left_time, right_time = 0;
int beacon_dir;

//Motors
Motor_Driver Motor_Driver(MOTOR_RIGHT_ENABLE, MOTOR_RIGHT_CONTROL1, MOTOR_RIGHT_CONTROL2,MOTOR_LEFT_ENABLE, MOTOR_LEFT_CONTROL1, MOTOR_LEFT_CONTROL2);

//Wheel Encoding
volatile int clicks_RIGHT = 0; 
volatile int clicks_LEFT = 0; 



//PID stuff
double Setpoint, Input_RIGHT, Input_LEFT, Output_RIGHT, Output_LEFT;
int wait_time = 0;
int done = 0;

//Please set constants, no magic numbers
PID PID_RIGHT(&Input_RIGHT, &Output_RIGHT, &Setpoint,PID_P_RIGHT, PID_I_RIGHT,PID_D_RIGHT);
PID PID_LEFT(&Input_LEFT, &Output_LEFT, &Setpoint,PID_P_LEFT ,PID_I_LEFT,PID_D_LEFT);
unsigned long StartTime;

//Receive data
char recvData[MAXSIZE];
char direction_command[MAXSIZE];
char number_ticks_command[MAXSIZE];
int incomingByte;

//Our "protothreading"
Metro serialMetro = Metro(250);
Metro servoMetro = Metro(10);
Metro goRightMetro = Metro(10000);
Metro motorMetro = Metro(2200);

char xml[MAX_STRING];

#define TIMER_CLK_DIV1024 0x05; 
#define TIMER_PRESCALE_MASK 0x07; 


/*******************SETUP*****************/
void setup() {
  //Serial Communication
  Serial.begin(9600);  

  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slave_address = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI

  //For the compass(I2C communication)
  Wire.begin();
   
 //TCCR0B = (TCCR0B & 0b11111000) | TIMER_CLK_DIV1024;
//  TCCR1B = (TCCR1B & 0b11111000) | TIMER_CLK_DIV1024;
//  TCCR2B = (TCCR2B & 0b11111000) | TIMER_CLK_DIV1024;
//  TCCR3B = (TCCR3B & 0b11111000) | TIMER_CLK_DIV1024;
//  TCCR4B = (TCCR4B & 0b11111000) | TIMER_CLK_DIV1024;
  //TCCR1B = (TCCR1B & ~TIMER_PRESCALE_MASK) | TIMER_CLK_DIV1024;
  //TCCR3B = (TCCR3B & ~TIMER_PRESCALE_MASK) | TIMER_CLK_DIV1024;
  //TCCR4B = (TCCR4B & ~TIMER_PRESCALE_MASK) | TIMER_CLK_DIV1024;

  //Telling which pin the servo is on. 
  myservo.attach(SERVO_PIN);
  
  //Set up US pins
  pinMode(LEFT_ULTRASONIC_PIN, INPUT);
  pinMode(RIGHT_ULTRASONIC_PIN, INPUT);

  //Interrupts for the Beacons. 
  attachInterrupt(LEFT_BEACON_INT, left_beacon, CHANGE);
  attachInterrupt(RIGHT_BEACON_INT, right_beacon, CHANGE);

  //Interrupts for Wheel encoders
  attachInterrupt(MOTOR_RIGHT_ENCODER, motor_RIGHT_tick, FALLING);    
  attachInterrupt(MOTOR_LEFT_ENCODER, motor_LEFT_tick, FALLING); 


  //PID STUFF I NEED TO FIGURE OUT
  PID_RIGHT.SetInputLimits(PID_RIGHT_INPUT_MIN ,PID_RIGHT_INPUT_MAX );
  PID_RIGHT.SetOutputLimits(PID_RIGHT_OUTPUT_MIN ,PID_RIGHT_OUTPUT_MAX);
  
  PID_LEFT.SetInputLimits(PID_LEFT_INPUT_MIN ,PID_LEFT_INPUT_MAX);
  PID_LEFT.SetOutputLimits(PID_LEFT_OUTPUT_MIN ,PID_LEFT_OUTPUT_MAX);
  //  //initialize the variables we're linked to
  Input_RIGHT = clicks_RIGHT;
  Input_LEFT = clicks_LEFT;
 
  Output_RIGHT = 0;
  Output_LEFT = 0;
  //turn the PID on
  PID_RIGHT.SetMode(AUTO);
  PID_LEFT.SetMode(AUTO);
  StartTime = millis();
  
  
  // we are in forward mode
  Motor_Driver.Forward();
  Setpoint = 1000;
}

/*******************MAIN*****************/
void loop() {
    int left_us_val, left_flex_val, right_us_val, right_flex_val,compass_val = 0;
Setpoint = 1000;
    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
        //get information
        //left_us_val       = ultrasonic(LEFT_ULTRASONIC_PIN);
        //right_us_val      = ultrasonic(RIGHT_ULTRASONIC_PIN);
        left_flex_val     = flex(LEFT_FLEX_PIN);
        right_flex_val    = flex(RIGHT_FLEX_PIN);
        compass_val       = compass();

        //send serial info
        sendSerialInfo(left_us_val, left_flex_val,right_us_val, right_flex_val,compass_val, pos, clicks_RIGHT, clicks_LEFT);

        serialMetro.reset();
    }
    
    if (servoMetro.check() == 1) { // check if the metro has passed it's interval .
      //This needs fixed up
      if(beacon_dir == LEFT) {
        if(pos >= 180) {
           beacon_dir = NA; 
           right_time = 0;
           left_time = 0;
        }
        pos++;
        delay(10);
      }
      else if(beacon_dir == RIGHT) {
        if(pos <= 0) {
           beacon_dir = NA; 
           right_time = 0;
           left_time = 0;
        }
        pos--;
        delay(10);
      }
      else if(beacon_dir == STRAIGHT) {
        //do nothing
      }
      //Else beacon_dir is unavailable... sweep
      else {
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
      }

        myservo.write(pos);              // tell servo to go to position in variable 'pos'   
        servoMetro.reset();
    }


    Input_RIGHT= clicks_RIGHT;
    Input_LEFT = clicks_LEFT;
    wait_time = StartTime - millis();
    
    if(wait_time > TIME_LIMIT_1 && wait_time < TIME_LIMIT_2)  { // check if the metro has passed it's interval .
      PID_RIGHT.SetOutputLimits(PID_RIGHT_INPUT_MIN,PID_RIGHT_INPUT_MAX);
      PID_LEFT.SetOutputLimits(PID_LEFT_INPUT_MIN,PID_LEFT_INPUT_MAX);
        done = 1;
    }
   
    if(done) {
      PID_RIGHT.SetOutputLimits(PID_RIGHT_INPUT_MIN,PID_RIGHT_INPUT_MAX);
      PID_LEFT.SetOutputLimits(PID_LEFT_INPUT_MIN,PID_LEFT_INPUT_MAX);
      done = 0;
    }

    //Set Tuning Parameters based on how close we are to setpoint
    //if(abs(Setpoint-Input_B)<200)  PID_B.SetOutputLimits(15,240);;  //aggressive
    //else myPID.SetTunings(3,4,1); //comparatively moderate
    PID_RIGHT.Compute();
    PID_LEFT.Compute();


    analogWrite(MOTOR_RIGHT_ENABLE, Output_RIGHT);
    analogWrite(MOTOR_LEFT_ENABLE, Output_LEFT);


//        Serial.print("Current input A: ");
//        Serial.println(Input_A);
//        Serial.print("Current output A: ");
//        Serial.println(Output_A);
////  //  //
////  //  //
//         Serial.print("Current input B: ");
//         Serial.println(Input_B);
//         Serial.print("Current output B: ");
//         Serial.println(Output_B);
}

/***************SENSOR FUNCTIONS***************/

int ultrasonic(int pin) {
    //Used to read in the pulse that is being sent by the MaxSonar device.
    //Pulse Width representation with a scale factor of 147 uS per Inch.
    //Will package in Inches for now
    long pulse;

    pulse = pulseIn(pin, HIGH);
    //inches = pulse/147;
    return pulse;
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
    //delay(10);                   
    
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


/*************CREATE XML FOR BEAGLEBOARD************/
void sendSerialInfo(int left_us_val, int left_flex_val,int right_us_val, int right_flex_val,int compass_val, int pos, int clicks_RIGHT, int clicks_LEFT)
{

    sprintf(xml,"<?xml version=\"1.0\"?><sensor><c>%f</c><f><l>%d</l><r>%d</r></f><us><l>%d</l><r>%d</r></us><b>%d</b><we><a>%d</a><b>%d</b></we></sensor>", compass_val, left_flex_val, right_flex_val, left_us_val, right_us_val,pos, clicks_RIGHT, clicks_LEFT); 
    Serial.println(xml);
    //Serial.println(millis());
    return;
}

void receiveData() {
  int count = 0;
  int flag = 0;
  memset(recvData, 0, 8);       
  while(count <= 8) {
    while (Serial.available() > 0) {
      // read the incoming byte:
      incomingByte = Serial.read();
      recvData[count] = byte(incomingByte);
      count++;
      flag  = 1;
    }
  }
  if(flag){
    //We need to parse our information here
    Serial.println(recvData);
  }
  Serial.flush();
}



//INTERRUPTS//
void left_beacon() {
  int diff;
  if(!left_time){
    left_time = millis();
    beacon_dir = NA;
  }

  //Serial.print("Saw Left Interrupt! TIME: ");
  //Serial.println(left_time);
  beacon_dir = NA;
  if(right_time) {
    if((left_time - right_time) > 500) {  
      //Serial.println("Beacon Right!");
      beacon_dir = RIGHT;
      right_time = 0;
      left_time = 0;
    }
    else {
      Serial.println("Beacon Straight!"); 
      //delay(10);
      beacon_dir = STRAIGHT;
      left_time = 0;
      right_time = 0;
    }
  }
}

void right_beacon() {
  int diff;
  
  if(!right_time){
    right_time = millis();
    beacon_dir = NA;
  }

  //Serial.print("Saw Right Interrupt! TIME: ");
  //Serial.println(right_time);

  if(left_time){
    if((right_time - left_time) > 500) {
      //Serial.println("Beacon Left!");
      beacon_dir = LEFT;
      left_time = 0;
      right_time = 0;
    }    
    
    else {
      //delay(10);
      beacon_dir = STRAIGHT;
      left_time = 0;
      right_time = 0;
    }  

  }
}  

void motor_RIGHT_tick() {   
  clicks_RIGHT++; 
}   

void motor_LEFT_tick() { 
  clicks_LEFT++;        
}

