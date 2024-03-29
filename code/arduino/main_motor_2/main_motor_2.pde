#include <Wire.h>
#include <string.h>
//#include <Servo.h> 
//#include <Metro.h> 
#include <motor_driver.h>
#include <PID_Beta6.h>

#include <MsTimer2.h>



//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
//#define LEFT_FLEX_PIN 0
//#define RIGHT_FLEX_PIN 1  
//#define LEFT_ULTRASONIC_PIN 11 
//#define RIGHT_ULTRASONIC_PIN 12
//
//#define LEFT_BEACON_INT  4  //Interrupt 0 
//#define RIGHT_BEACON_INT 5  //Interrupt 1  

//Servo Constants
//#define SERVO_PIN 4
//#define HMC6352Address 0x42

//Beacon Constants
//#define NA -1
//#define STRAIGHT 0
//#define LEFT 1
//#define RIGHT 2

//Direction Constants
#define STOP 0
#define FORWARD 3
#define LEFT 1
#define RIGHT 2

//MOTORS
#define MOTOR_RIGHT_ENABLE 7
#define MOTOR_RIGHT_CONTROL1 5
#define MOTOR_RIGHT_CONTROL2 9
#define MOTOR_RIGHT_ENCODER 0


#define MOTOR_LEFT_ENABLE 8
#define MOTOR_LEFT_CONTROL1 6
#define MOTOR_LEFT_CONTROL2 10
#define MOTOR_LEFT_ENCODER 1





//Receive data
#define MAXSIZE 8 
#define MAX_STRING 255 

// PID parameters for each motor
// might have morse set for different situations
#define PID_P_RIGHT 4
#define PID_I_RIGHT 0
#define PID_D_RIGHT 0.4
#define PID_P_LEFT 4
#define PID_I_LEFT 0
#define PID_D_LEFT 0.4

// range of input = ticks and output = pwm 
#define PID_RIGHT_INPUT_MIN  0
#define PID_RIGHT_INPUT_MAX  20000
#define PID_RIGHT_OUTPUT_MIN -10
#define PID_RIGHT_OUTPUT_MAX 10
#define PID_LEFT_INPUT_MIN  0
#define PID_LEFT_INPUT_MAX  20000
#define PID_LEFT_OUTPUT_MIN -10
#define PID_LEFT_OUTPUT_MAX 10

// the desired distance in ticks 
// can be converted 2364 ticks = 1 revolution = 2 feet
#define SETPOINT 11820


// turns
// 135 ticks    180 degrees
// 300 ticks    360 degrees
//slips in lab but ok outdoors

#define TIME_LIMIT_1 1900
#define TIME_LIMIT_2 5000


#define EPSILON 50


#define SPEED 35

#define MAX_PWM_LEFT  255
#define MAX_PWM_RIGHT 255


#define PW_LEFT_START 100

#define PW_RIGHT_START 100
/*******************GLOBAL VARIABLES*****************/

//For the compass
//int slave_address;

//For the servo
//Servo myservo;

//Servo Variables
//Should take out of global
//int back = 0;
//int pos = 90;

//Beacon Specific Variables
//volatile int left_time, right_time = 0;
//int beacon_dir = NA;
//int compass_val = 0;

//Motors
Motor_Driver Motor_Driver(MOTOR_RIGHT_ENABLE, MOTOR_RIGHT_CONTROL1, MOTOR_RIGHT_CONTROL2,MOTOR_LEFT_ENABLE, MOTOR_LEFT_CONTROL1, MOTOR_LEFT_CONTROL2);

//Wheel Encoding
volatile int clicks_RIGHT = 0; 
volatile int clicks_LEFT = 0; 

//PID stuff
double Setpoint, Input_RIGHT, Input_LEFT, Output_RIGHT, Output_LEFT, Speed;
//int wait_time = 0;
//int done = 0;

//Please set constants, no magic numbers
//PID PID_RIGHT(&Input_RIGHT, &Output_RIGHT, &Speed,PID_P_RIGHT, PID_I_RIGHT,PID_D_RIGHT);
//PID PID_LEFT(&Input_LEFT, &Output_LEFT, &Speed,PID_P_LEFT ,PID_I_LEFT,PID_D_LEFT);





//unsigned long StartTime;

//Receive data
char recvData[MAXSIZE];
char direction_command[MAXSIZE];
char number_ticks_command[MAXSIZE];
int incomingByte;

//Our "protothreading"
//Metro serialMetro = Metro(250);
//Metro servoMetro = Metro(10);
//Metro goRightMetro = Metro(10000);
//Metro motorMetro = Metro(2200);

char xml[MAX_STRING];

char buff[]= "0000000000";
int drive=0; 
int ticks=0; 


int pw_LEFT= PW_LEFT_START;
int pw_RIGHT= PW_RIGHT_START; 

int previous_clicks_RIGHT = 0;
int previous_clicks_LEFT = 0 ;

//int displacement_LEFT;
//int displacement_RIGHT;

//float ratio = 0;


//int counter = 0;

int done_LEFT = 0, done_RIGHT = 0;

int ticks_tenthousands =0, ticks_thousands= 0  ,  ticks_hundereds= 0, ticks_tens = 0 , ticks_ones = 0; 

/*******************SETUP*****************/
void setup() {
  //Serial Communication
  Serial.begin(9600);  
  
//   //Timer2 Settings: Timer Prescaler /256, WGM mode 0
//  TCCR2A = 0;
//  TCCR2B = 1<<CS22 | 1<<CS21;
//
//  //Timer2 Overflow Interrupt Enable  
//  TIMSK2 = 1<<TOIE2;
//
//  //reset timer
//  TCNT2 = 0;

  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
 // slave_address = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI

  //For the compass(I2C communication)
  //Wire.begin();

  //Telling which pin the servo is on. 
 // myservo.attach(SERVO_PIN);
  
  //Set up US pins
 // pinMode(LEFT_ULTRASONIC_PIN, INPUT);
//  pinMode(RIGHT_ULTRASONIC_PIN, INPUT);

  //Interrupts for the Beacons. 
 // attachInterrupt(LEFT_BEACON_INT, left_beacon, CHANGE);
//  attachInterrupt(RIGHT_BEACON_INT, right_beacon, CHANGE);

  //Interrupts for Wheel encoders
  attachInterrupt(MOTOR_RIGHT_ENCODER, motor_RIGHT_tick, FALLING);    
  attachInterrupt(MOTOR_LEFT_ENCODER, motor_LEFT_tick, FALLING); 


    Input_LEFT= clicks_LEFT - previous_clicks_LEFT;
    Input_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;

  //PID STUFF I NEED TO FIGURE OUT
//  PID_RIGHT.SetInputLimits(PID_RIGHT_INPUT_MIN ,PID_RIGHT_INPUT_MAX );
//  PID_RIGHT.SetOutputLimits(PID_RIGHT_OUTPUT_MIN ,PID_RIGHT_OUTPUT_MAX);
  
//  PID_LEFT.SetInputLimits(PID_LEFT_INPUT_MIN ,PID_LEFT_INPUT_MAX);
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
  

 pw_RIGHT=PW_RIGHT_START; 
 
  pw_LEFT = PW_LEFT_START;
 previous_clicks_RIGHT = 0;
 previous_clicks_LEFT = 0;
  
  Motor_Driver.Reset();
delay(3000);

  
  // we are in forward mode
   Motor_Driver.Forward();
  Setpoint = SETPOINT;
  
 // PID_RIGHT.SetSampleTime(10);
  //PID_LEFT.SetSampleTime(10);
  
  
  Speed = SPEED; // ticks per unit time
  
   MsTimer2::set(30, do_PID); // 500ms period
   MsTimer2::start();
}

/*******************MAIN*****************/
void loop() {
  
  
//  if(done_RIGHT == 1 && done_LEFT ==1){
//     MsTimer2::stop();
//   clicks_RIGHT = 0;
//     clicks_LEFT = 0;
//    previous_clicks_LEFT = 0;
//    previous_clicks_RIGHT = 0;
//         done_LEFT = 0;
//    done_RIGHT = 0;
//    pw_LEFT = 0;
//    pw_RIGHT = 0;
//   Serial.print("IM IN ");
//   delay(5000);
//    MsTimer2::start();
//  }
  
  
   // int left_us_val, left_flex_val, right_us_val, right_flex_val = 0;
   // int compass_val = 0;
    //Setpoint = 1000;
    
//    Input_LEFT = clicks_LEFT - previous_clicks_LEFT;
//    Input_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;
//    
//    previous_clicks_LEFT = clicks_LEFT;
//    previous_clicks_RIGHT = clicks_RIGHT;
//
//    PID_RIGHT.Compute();
//    PID_LEFT.Compute();
//
//
//
//          
//    
//    if( Setpoint - clicks_LEFT > EPSILON) {
//
//      pw_LEFT = pw_LEFT + Output_LEFT;      
//    }
//    else
//     pw_LEFT = 0;
//      
//      
//      
//    if( Setpoint - clicks_RIGHT > EPSILON) {
//
//       pw_RIGHT = pw_RIGHT + Output_RIGHT; 
//      
//    }
//    else
//      pw_RIGHT = 0;
//      
//    
//    if(pw_LEFT > 255 )
//      pw_LEFT = 255;
//      
//        if(pw_RIGHT > 255 )
//      pw_RIGHT = 255;
//      
//    analogWrite(MOTOR_RIGHT_ENABLE, pw_RIGHT);
//    analogWrite(MOTOR_LEFT_ENABLE, pw_LEFT);
//    
    //    analogWrite(MOTOR_RIGHT_ENABLE, Output_RIGHT);
//    analogWrite(MOTOR_LEFT_ENABLE, Output_LEFT);
    

              // Serial.println("input  RIGHT: ");
  // Serial.println(Input_RIGHT);
////    
////    
//            Serial.println("output RIGHT: ");
//    Serial.println(Output_RIGHT);
////    
       // Serial.println("clicks RIGHT: ");
   // Serial.println(clicks_RIGHT);
////      
//        Serial.println("PWM RIGHT: ");
//    Serial.println(pw_RIGHT);
////    
////    
                   //Serial.println("input  LEFT: ");
  //  Serial.println(Input_LEFT);
//               Serial.println("output LEFT: ");
//    Serial.println(Output_LEFT);
           //  Serial.println("clicks LEFT: ");
  // Serial.println(clicks_LEFT);
////      
//       Serial.println("PWM LEFT: ");
//    Serial.println(pw_LEFT);
//    

//    
//    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
//        //get information
//        //left_us_val       = ultrasonic(LEFT_ULTRASONIC_PIN);
//        //right_us_val      = ultrasonic(RIGHT_ULTRASONIC_PIN);
//        left_flex_val     = flex(LEFT_FLEX_PIN);
//        right_flex_val    = flex(RIGHT_FLEX_PIN);
//        compass_val       = compass();
//
//        //send serial info
       sendSerialInfo( clicks_RIGHT, clicks_LEFT, done_RIGHT, done_LEFT);
//
//        serialMetro.reset();
//    }
//    
//    if (servoMetro.check() == 1) { // check if the metro has passed it's interval .
//      //This needs fixed up
//      if(beacon_dir == LEFT) {
//        if(pos >= 180) {
//           beacon_dir = NA; 
//           right_time = 0;
//           left_time = 0;
//        }
//        pos++;
//        delay(10);
//      }
//      else if(beacon_dir == RIGHT) {
//        if(pos <= 0) {
//           beacon_dir = NA; 
//           right_time = 0;
//           left_time = 0;
//        }
//        pos--;
//        delay(10);
//      }
//      else if(beacon_dir == STRAIGHT) {
//        //do nothing
//      }
//      //Else beacon_dir is unavailable... sweep
//      else {
//        if(pos >= 180) {
//          back = 1; 
//        }
//        
//        else if(pos <= 0) {
//          back = 0; 
//        }
//      
//        if(back == 0)
//          pos = pos+1;   
//      
//        else
//          pos = pos-1;  
//      }
//
//        myservo.write(pos);              // tell servo to go to position in variable 'pos'  
//        servoMetro.reset();
//    }


  //  Input_RIGHT= clicks_RIGHT;
    //Input_LEFT = clicks_LEFT;
   // wait_time = StartTime - millis();
    
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



       Serial.println("clicks RIGHT: ");
    Serial.println(clicks_RIGHT);
                Serial.println("PWM RIGHT: ");
 Serial.println(pw_RIGHT);
 
 
 Serial.println("input RIGHT: ");
    Serial.println(Input_RIGHT);
////      
//        Serial.println("PWM RIGHT: ");
//    Serial.println(pw_RIGHT);
////    
////    
                   //Serial.println("input  LEFT: ");
  //  Serial.println(Input_LEFT);
//               Serial.println("output LEFT: ");
//    Serial.println(Output_LEFT);
           Serial.println("clicks LEFT: ");
 Serial.println(clicks_LEFT);
            Serial.println("PWM LEFT: ");
 Serial.println(pw_LEFT);
 
  Serial.println("input LEFT: ");
    Serial.println(Input_LEFT);
    
    
    
    receiveData();

}

/***************SENSOR FUNCTIONS***************/

//int ultrasonic(int pin) {
//    //Used to read in the pulse that is being sent by the MaxSonar device.
//    //Pulse Width representation with a scale factor of 147 uS per Inch.
//    //Will package in Inches for now
//    long pulse;
//
//    pulse = pulseIn(pin, HIGH);
//    //inches = pulse/147;
//    return pulse;
//}
//
//int flex(int pin) {
//    int sensor_value = 0;
//    // read the value from the sensor:
//    sensor_value = analogRead(pin);       
//    return sensor_value;
//}

//int compass() {
//    byte heading_data[2];
//    int i;
//    int heading_value;
//    
//    // Send a "A" command to the HMC6352
//    // This requests the current heading data
//    Wire.beginTransmission(slave_address);
//    Wire.send("A");              // The "Get Data" command
//    Wire.endTransmission();
//    //delay(10);                   
//    
//    // The HMC6352 needs at least a 70us (microsecond) delay
//    // after this command.  Using 10ms just makes it safe
//    // Read the 2 heading bytes, MSB first
//    // The resulting 16bit word is the compass heading in 10th's of a degree
//    // For example: a heading of 1345 would be 134.5 degrees
//    
//    Wire.requestFrom(slave_address, 2);        // Request the 2 byte heading (MSB comes first)
//    i = 0;
//    
//    while(Wire.available() && i < 2)
//    { 
//      heading_data[i] = Wire.receive();
//      i++;
//    }
//    heading_value = heading_data[0]*256 + heading_data[1];  // Put the MSB and LSB together
//    return heading_value;
//}


/*************CREATE XML FOR BEAGLEBOARD************/
void sendSerialInfo( int clicks_RIGHT, int clicks_LEFT, int done_RIGHT, int done_LEFT)
{
    
    sprintf(xml,"<?xml version=\"1.0\"?><motor><r>%d<r><l>%d</l><r>%d</r><l><us></l></motor>",  clicks_RIGHT, clicks_LEFT, done_RIGHT, done_LEFT); 
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
      Serial.print("drive: ");
      Serial.println(drive);
    }
    if (buff[10]=='T') {
      ticks_ones = int(buff[9]);
      ticks_ones -= 48;

      ticks_tens = int(buff[8]);
      ticks_tens -= 48;

      ticks_hundereds = int(buff[7]);
      ticks_hundereds -= 48;
      ticks_thousands = int(buff[6]);
      ticks_thousands -= 48;
      
      ticks_tenthousands = int(buff[5]);
      ticks_tenthousands -= 48;
      
      Setpoint =( 10000* ticks_tenthousands + 1000 * ticks_thousands +  100 * ticks_hundereds + 10 * ticks_tens + ticks_ones);
      //ticks*=1000;
     // Setpoint = ticks;
      Serial.print("serial setpoint ");
      Serial.println(Setpoint);
    }

  }
}

//INTERRUPTS//
//void left_beacon() {
//  if(!left_time){
//    left_time = millis();
//    beacon_dir = NA;
//  }
//
//  Serial.print("Saw Left Interrupt! TIME: ");
//  //Serial.println(left_time);
//  beacon_dir = NA;
//  if(right_time) {
//    if((left_time - right_time) > 500) {  
//      //Serial.println("Beacon Right!");
//      beacon_dir = RIGHT;
//      right_time = 0;
//      left_time = 0;
//    }
//    else {
//      //Serial.println("Beacon Straight!"); 
//      beacon_dir = STRAIGHT;
//      left_time = 0;
//      right_time = 0;
//    }
//  }
//}
//
//void right_beacon() {
//  if(!right_time){
//    right_time = millis();
//    beacon_dir = NA;
//  }
//  
//  Serial.print("Saw Right Interrupt! TIME: ");
//  //Serial.println(right_time);
//
//  if(left_time){
//    if((right_time - left_time) > 500) {
//      //Serial.println("Beacon Left!");
//      beacon_dir = LEFT;
//      left_time = 0;
//      right_time = 0;
//    }    
//    
//    else {
//      beacon_dir = STRAIGHT;
//      left_time = 0;
//      right_time = 0;
//    }  
//
//  }
//}  

void motor_RIGHT_tick() {   
  clicks_RIGHT++; 
}   

void motor_LEFT_tick() { 
  clicks_LEFT++;        
}


//ISR(TIMER2_OVF_vect) {
//    // 16 microsecond  x 1000 = 16 ms
//  if ( counter % 1000 == 0)
//  {
//   // do  
//   
//   do_PID();
//   
//   counter = 1;
//  }
// 
// 
// counter++;
//  
//  
//  
//  
//  
//  
//  
//}; 




void do_PID(){

   Input_LEFT = clicks_LEFT - previous_clicks_LEFT;
    Input_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;
    
    previous_clicks_LEFT = clicks_LEFT;
    previous_clicks_RIGHT = clicks_RIGHT;

   // PID_RIGHT.Compute();
    //PID_LEFT.Compute();



          
    
    if( Setpoint - clicks_LEFT > EPSILON) {
      
      
            if (Input_LEFT < Speed)
      
      pw_LEFT = pw_LEFT + 1    ;
    
                else if (Input_LEFT > Speed)
                      pw_LEFT = pw_LEFT - 1; 

            
      done_LEFT= 0;
    }
    else{
     pw_LEFT = 0;
     done_LEFT = 1; 
    }
      
    if( Setpoint - clicks_RIGHT > EPSILON) {
      
               if (Input_RIGHT < Speed)
      
            pw_RIGHT = pw_RIGHT + 1;  
            else if (Input_RIGHT > Speed)
                      pw_RIGHT = pw_RIGHT - 1; 

       
       done_RIGHT= 0;
      
    }
    else{
      pw_RIGHT = 0;
      done_RIGHT = 1; 
    }
    
    
    if(pw_LEFT > MAX_PWM_LEFT )
      pw_LEFT = MAX_PWM_LEFT;
      
        if(pw_RIGHT > MAX_PWM_RIGHT )
      pw_RIGHT = MAX_PWM_RIGHT;
      
    analogWrite(Motor_Driver.pwm_pin_right, pw_RIGHT);
    analogWrite(Motor_Driver.pwm_pin_left, pw_LEFT);
    



}


//void checkDone(){
// 
// 
//  if (SETPOINT - clicks_RIGHT < EPSILON ) {
//    
//   delay(500);
//   done = 1;
//  
// // StartTime = millis();
//  }
//  else
//  done = 0;
//  
//  
//}

