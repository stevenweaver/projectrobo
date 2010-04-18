#include <Wire.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 
#include <motor_driver.h>
//#include <PID_Beta6.h>

//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
#define LEFT_FLEX_PIN 0
#define RIGHT_FLEX_PIN 1  
#define LEFT_ULTRASONIC_PIN 11 
#define RIGHT_ULTRASONIC_PIN 12

#define LEFT_BEACON_INT  4  //Interrupt 0 
#define RIGHT_BEACON_INT 5  //Interrupt 1  

//Servo Constants
#define SERVO_PIN 4
#define HMC6352Address 0x42

//Beacon Constants
#define NA -1
#define STRAIGHT 0
#define LEFT 1
#define RIGHT 2

//Direction Constants
#define STOP 0
#define FORWARD 3
//#define LEFT 1
//#define RIGHT 2

//MOTORS
#define MOTOR_RIGHT_ENABLE 9
#define MOTOR_RIGHT_CONTROL1 8
#define MOTOR_RIGHT_CONTROL2 10
#define MOTOR_RIGHT_ENCODER 1 //INT 0 (no need to define// wont be used directly)

#define MOTOR_LEFT_ENABLE 6
#define MOTOR_LEFT_CONTROL1 5
#define MOTOR_LEFT_CONTROL2 7
#define MOTOR_LEFT_ENCODER 0 //INT 1

//Receive data
#define MAXSIZE 8 
#define MAX_STRING 255 

// PID parameters for each motor
// might have morse set for different situations
#define PID_P_RIGHT 30
#define PID_I_RIGHT 0
#define PID_D_RIGHT 0.4
#define PID_P_LEFT 30
#define PID_I_LEFT 0
#define PID_D_LEFT 0.4

// range of input = ticks and output = pwm 
#define PID_RIGHT_INPUT_MIN  0
#define PID_RIGHT_INPUT_MAX  20000
#define PID_RIGHT_OUTPUT_MIN 15
#define PID_RIGHT_OUTPUT_MAX 80
#define PID_LEFT_INPUT_MIN  0
#define PID_LEFT_INPUT_MAX  20000
#define PID_LEFT_OUTPUT_MIN 13
#define PID_LEFT_OUTPUT_MAX 72

// the desired distance in ticks 
// can be converted 197 ticks = 1 revolution = 2 feet
#define SETPOINT 1000


#define TIME_LIMIT_1 1900
#define TIME_LIMIT_2 5000


#define EPSILON 20

#define MAX_PWM_LEFT  100
#define MAX_PWM_RIGHT 100

/*******************GLOBAL VARIABLES*****************/

//For the compass
int slave_address;

//For the servo
Servo myservo;

//Servo Variables
//Should take out of global
int back = 0;
int pos = 90;

//Beacon Specific Variables
volatile int left_time, right_time = 0;
int beacon_dir = NA;
int compass_val = 0;

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
//PID PID_RIGHT(&Input_RIGHT, &Output_RIGHT, &Setpoint,PID_P_RIGHT, PID_I_RIGHT,PID_D_RIGHT);
//PID PID_LEFT(&Input_LEFT, &Output_LEFT, &Setpoint,PID_P_LEFT ,PID_I_LEFT,PID_D_LEFT);
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

char buff[]= "0000000000";
int drive=0; 
int ticks=0; 


int pw_LEFT;
int pw_RIGHT; 

int previous_clicks_RIGHT;
int previous_clicks_LEFT;

int displacement_LEFT;
int displacement_RIGHT;

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
 // PID_RIGHT.SetInputLimits(PID_RIGHT_INPUT_MIN ,PID_RIGHT_INPUT_MAX );
 // PID_RIGHT.SetOutputLimits(PID_RIGHT_OUTPUT_MIN ,PID_RIGHT_OUTPUT_MAX);
  
 // PID_LEFT.SetInputLimits(PID_LEFT_INPUT_MIN ,PID_LEFT_INPUT_MAX);
 // PID_LEFT.SetOutputLimits(PID_LEFT_OUTPUT_MIN ,PID_LEFT_OUTPUT_MAX);
  //  //initialize the variables we're linked to
 // Input_RIGHT = clicks_RIGHT;
 // Input_LEFT = clicks_LEFT;
 
 // Output_RIGHT = 0;
//Output_LEFT = 0;
  //turn the PID on
 // PID_RIGHT.SetMode(AUTO);
//PID_LEFT.SetMode(AUTO);
//StartTime = millis();
  
 pw_LEFT = 30;
 pw_RIGHT= 30; 
 previous_clicks_RIGHT = 0;
 previous_clicks_LEFT = 0;
  
  

  
  // we are in forward mode
   Motor_Driver.Forward();
  Setpoint = SETPOINT;
}

/*******************MAIN*****************/
void loop() {
    int left_us_val, left_flex_val, right_us_val, right_flex_val = 0;
    int compass_val = 0;
    //Setpoint = 1000;
    
    displacement_LEFT = clicks_LEFT - previous_clicks_LEFT;
    displacement_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;
    
    if( Setpoint - clicks_RIGHT > EPSILON) {
       if( displacement_LEFT > displacement_RIGHT) {
         
          if ( (pw_RIGHT + 3) <=   MAX_PWM_RIGHT){
          pw_RIGHT += 3;
        }
       
        else {
          pw_LEFT -= 3;
        }
        
       }
    }
    else
      pw_RIGHT = 0;
      
      
      
    if( Setpoint - clicks_LEFT > EPSILON) {
       if( displacement_RIGHT > displacement_LEFT) {
         
          if ((pw_LEFT + 3) <=  MAX_PWM_LEFT){
          pw_LEFT += 3;
        }
        else {
          pw_RIGHT -= 3;
        }
        
       }
    }
    else
      pw_LEFT = 0;
      
    
    
      
    analogWrite(MOTOR_RIGHT_ENABLE, pw_RIGHT);
    analogWrite(MOTOR_LEFT_ENABLE, pw_LEFT);
    
    previous_clicks_LEFT = clicks_LEFT;
    previous_clicks_RIGHT = clicks_RIGHT;
    
      

    
    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
        //get information
        //left_us_val       = ultrasonic(LEFT_ULTRASONIC_PIN);
        //right_us_val      = ultrasonic(RIGHT_ULTRASONIC_PIN);
        left_flex_val     = flex(LEFT_FLEX_PIN);
        right_flex_val    = flex(RIGHT_FLEX_PIN);
        compass_val       = compass();

        //send serial info
        sendSerialInfo(left_us_val, left_flex_val, right_us_val, right_flex_val, compass_val, pos, clicks_RIGHT, clicks_LEFT);

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
    
//    if(wait_time > TIME_LIMIT_1 && wait_time < TIME_LIMIT_2)  { // check if the metro has passed it's interval .
//      PID_RIGHT.SetOutputLimits(PID_RIGHT_INPUT_MIN,PID_RIGHT_INPUT_MAX);
//      PID_LEFT.SetOutputLimits(PID_LEFT_INPUT_MIN,PID_LEFT_INPUT_MAX);
//        done = 1;
//    }
//   
//    if(done) {
//      PID_RIGHT.SetOutputLimits(PID_RIGHT_INPUT_MIN,PID_RIGHT_INPUT_MAX);
//      PID_LEFT.SetOutputLimits(PID_LEFT_INPUT_MIN,PID_LEFT_INPUT_MAX);
//      done = 0;
//    }

    //Set Tuning Parameters based on how close we are to setpoint
    //if(abs(Setpoint-Input_B)<200)  PID_B.SetOutputLimits(15,240);;  //aggressive
    //else myPID.SetTunings(3,4,1); //comparatively moderate
   // PID_RIGHT.Compute();
   // PID_LEFT.Compute();


//    analogWrite(MOTOR_RIGHT_ENABLE, Output_RIGHT);
//    analogWrite(MOTOR_LEFT_ENABLE, Output_LEFT);

    receiveData();

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
    int i;
    int heading_value;
    
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
void sendSerialInfo(int left_us_val, int left_flex_val,int right_us_val, int right_flex_val, int compass_val, int pos, int clicks_RIGHT, int clicks_LEFT)
{
    //  float compass =   (compass_val / 10) + (compass_val % 10); 
    sprintf(xml,"<?xml version=\"1.0\"?><sensor><c>%d</c><f><l>%d</l><r>%d</r></f><us><l>%d</l><r>%d</r></us><b>%d</b><we><a>%d</a><b>%d</b></we></sensor>", compass_val, left_flex_val, right_flex_val, left_us_val, right_us_val, pos, clicks_RIGHT, clicks_LEFT); 
    Serial.println(xml);
    return;
}

void receiveData() {
  while (Serial.available()>0) {
    for (int i=0; i<10; i++) {
      buff[i]=buff[i+1];
    }
    buff[10]=Serial.read();
    if (buff[10]=='D') {
      drive=int(buff[9]);
      drive -= 48;
      if(drive == FORWARD) {
          Motor_Driver.Forward();
      }
      
      else if(drive == LEFT) {
        Motor_Driver.Left();
      }  
      
      else if(drive == RIGHT) {
        Motor_Driver.Right();
      }
      
      else if(drive == STOP) {
        Motor_Driver.Stop();
      }       
      //Serial.print("drive: ");
      //Serial.println(drive);
    }
    if (buff[10]=='T') {
      ticks=int(buff[9]);
      ticks-= 48;
      ticks*=1000;
      Setpoint = ticks;
      //Serial.print("tick: ");
      //Serial.println(ticks);
    }

  }
}

//INTERRUPTS//
void left_beacon() {
  if(!left_time){
    left_time = millis();
    beacon_dir = NA;
  }

  Serial.print("Saw Left Interrupt! TIME: ");
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
      //Serial.println("Beacon Straight!"); 
      beacon_dir = STRAIGHT;
      left_time = 0;
      right_time = 0;
    }
  }
}

void right_beacon() {
  if(!right_time){
    right_time = millis();
    beacon_dir = NA;
  }
  
  Serial.print("Saw Right Interrupt! TIME: ");
  //Serial.println(right_time);

  if(left_time){
    if((right_time - left_time) > 500) {
      //Serial.println("Beacon Left!");
      beacon_dir = LEFT;
      left_time = 0;
      right_time = 0;
    }    
    
    else {
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



