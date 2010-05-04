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
#define BACKWARD 4

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
#define PID_RIGHT_INPUT_MAX  100
#define PID_RIGHT_OUTPUT_MIN -10
#define PID_RIGHT_OUTPUT_MAX 10
#define PID_LEFT_INPUT_MIN  0
#define PID_LEFT_INPUT_MAX  100
#define PID_LEFT_OUTPUT_MIN -10
#define PID_LEFT_OUTPUT_MAX 10

// the desired distance in ticks 
// can be converted 2364 ticks = 1 revolution = 2 feet
//1182 = 1 foot
#define SETPOINT 0


// turns
// 135 ticks    180 degrees
// 300 ticks    360 degrees
//slips in lab but ok outdoors

#define TIME_LIMIT_1 1900
#define TIME_LIMIT_2 5000


#define EPSILON 50


#define SPEED 25

#define MAX_PWM_LEFT  255
#define MAX_PWM_RIGHT 255



#define PW_LEFT_START 100

#define PW_RIGHT_START 100



//Motors
Motor_Driver Motor_Driver(MOTOR_RIGHT_ENABLE, MOTOR_RIGHT_CONTROL1, MOTOR_RIGHT_CONTROL2,MOTOR_LEFT_ENABLE, MOTOR_LEFT_CONTROL1, MOTOR_LEFT_CONTROL2);

//Wheel Encoding
volatile float clicks_RIGHT = 0; 
volatile float clicks_LEFT = 0; 

//PID stuff
double Setpoint, Input_RIGHT, Input_LEFT, Output_RIGHT, Output_LEFT, Speed;
//int wait_time = 0;
//int done = 0;

//Please set constants, no magic numbers
PID PID_RIGHT(&Input_RIGHT, &Output_RIGHT, &Speed,PID_P_RIGHT, PID_I_RIGHT,PID_D_RIGHT);
PID PID_LEFT(&Input_LEFT, &Output_LEFT, &Speed,PID_P_LEFT ,PID_I_LEFT,PID_D_LEFT);





//unsigned long StartTime;

//Receive data
char recvData[MAXSIZE];
char direction_command[MAXSIZE];
char number_ticks_command[MAXSIZE];
int incomingByte;



char xml[MAX_STRING];

char buff[]= "0000000000";
int drive=0; 
int ticks=0; 


int pw_LEFT=0;
int pw_RIGHT=0; 

float previous_clicks_RIGHT = 0;
float previous_clicks_LEFT = 0 ;



int done_LEFT = 0, done_RIGHT = 0;

int   ticks_thousands= 0  ,  ticks_hundereds= 0, ticks_tens = 0 , ticks_ones = 0; 

float  ticks_tenthousands =0, Serial_Setpoint = 0;
int command = 0, Serial_Setpoint_Updated = 0, Serial_Direction_Updated = 0;

/*******************SETUP*****************/
void setup() {
  //Serial Communication
  Serial.begin(9600);  
  


  //Interrupts for Wheel encoders
  attachInterrupt(MOTOR_RIGHT_ENCODER, motor_RIGHT_tick, FALLING);    
  attachInterrupt(MOTOR_LEFT_ENCODER, motor_LEFT_tick, FALLING); 


    Input_LEFT= clicks_LEFT - previous_clicks_LEFT;
    Input_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;


  PID_RIGHT.SetInputLimits(PID_RIGHT_INPUT_MIN ,PID_RIGHT_INPUT_MAX );
  PID_RIGHT.SetOutputLimits(PID_RIGHT_OUTPUT_MIN ,PID_RIGHT_OUTPUT_MAX);
  
  PID_LEFT.SetInputLimits(PID_LEFT_INPUT_MIN ,PID_LEFT_INPUT_MAX);
  PID_LEFT.SetOutputLimits(PID_LEFT_OUTPUT_MIN ,PID_LEFT_OUTPUT_MAX);

  //turn the PID on
PID_RIGHT.SetMode(AUTO);
PID_LEFT.SetMode(AUTO);

  

 pw_RIGHT=PW_RIGHT_START; 
 
  pw_LEFT = PW_LEFT_START;
 previous_clicks_RIGHT = 0;
 previous_clicks_LEFT = 0;
  
    Motor_Driver.Reset();
delay(3000);

  
  // we are in forward mode
   Motor_Driver.Forward();
  Setpoint = SETPOINT;
  
  PID_RIGHT.SetSampleTime(10);
  PID_LEFT.SetSampleTime(10);
  
  
  Speed = SPEED; // ticks per unit time
  
   MsTimer2::set(30, do_PID); 
   MsTimer2::start();
}

/*******************MAIN*****************/
void loop() {
  
  

  
  
  
//    if(done_RIGHT = 1 && done_LEFT ==1 && command == 1)
//  {
//    MsTimer2::stop();
//    pw_RIGHT = 0; 
//    pw_LEFT = 0;
//    previous_clicks_RIGHT = 0;
//    previous_clicks_LEFT = 0;
//    clicks_LEFT = 0;
//    clicks_RIGHT = 0;
//    done_RIGHT = 0;
//    done_LEFT = 0;
//    MsTimer2::stop();
//    Motor_Driver.Reset();
//    delay(5000);
//    
//    
//    Motor_Driver.Forward();
//     
//     Setpoint = 11820 ;
//     command++;
//    MsTimer2::start(); 
//    
//    
//  }
     
//       Serial.println("clicks RIGHT: ");
//    Serial.println(clicks_RIGHT);
//                Serial.println("PWM RIGHT: ");
// Serial.println(pw_RIGHT);
// 
// 
// Serial.println("input RIGHT: ");
//    Serial.println(Input_RIGHT);
//    
//         Serial.println("output RIGHT: ");
//    Serial.println(Output_RIGHT);
//;
//           Serial.println("clicks LEFT: ");
// Serial.println(clicks_LEFT);
//            Serial.println("PWM LEFT: ");
// Serial.println(pw_LEFT);
// 
//  Serial.println("input LEFT: ");
//    Serial.println(Input_LEFT);
//    
//    
//      Serial.println("output LEFT: ");
//    Serial.println(Output_LEFT);
//    
//
// Serial.println("Setpoint: ");
//    Serial.println(Setpoint);
   
   
 // if(done_RIGHT = 1 && done_LEFT == 1  )
   
     get_command();

       sendSerialInfo( clicks_RIGHT, clicks_LEFT, done_RIGHT, done_LEFT);


    receiveData();

}



/*************CREATE XML FOR BEAGLEBOARD************/
void sendSerialInfo( float clicks_RIGHT, float clicks_LEFT, int done_RIGHT, int done_LEFT)
{
   
    sprintf(xml,"<?xml version=\"1.0\"?><motor><cl><r>%d</r><l>%d</l></cl>,<d><r>%d</r><l>%d</l></d></motor>",  clicks_RIGHT, clicks_LEFT, done_RIGHT, done_LEFT); 
  //  Serial.println(xml);
    return;
}


void receiveData() {
  
  for (int j = 0; j< 11; j++)
  {
    buff[j]= '0';
  }

  while (Serial.available()>0) {
    for (int i=0; i<10; i++) {
      buff[i]=buff[i+1];
    }
    buff[10]=Serial.read();
    
    
    
    if (buff[10]=='D') {
      drive=int(buff[9]);
      drive -= 48;
     
      Serial.print("drive: ");
      Serial.println(drive);
       Serial.println(buff);
      
     // Serial_Direction_Updated = 1;
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
      
      Serial_Setpoint =( 10000* ticks_tenthousands + 1000 * ticks_thousands +  100 * ticks_hundereds + 10 * ticks_tens + ticks_ones);



      Serial_Setpoint_Updated = 1;

      Serial.print("serial setpoint ");
      Serial.println(Serial_Setpoint);
       Serial.println(buff);
    }

  }
}


void motor_RIGHT_tick() {   
  clicks_RIGHT++; 
}   

void motor_LEFT_tick() { 
  clicks_LEFT++;        
}






void do_PID(){

   Input_LEFT = clicks_LEFT - previous_clicks_LEFT;
    Input_RIGHT = clicks_RIGHT - previous_clicks_RIGHT;
    
    previous_clicks_LEFT = clicks_LEFT;
    previous_clicks_RIGHT = clicks_RIGHT;

    PID_RIGHT.Compute();
    PID_LEFT.Compute();



          
    
    if( Setpoint - clicks_LEFT > EPSILON) {

      pw_LEFT = pw_LEFT + Output_LEFT;      
      done_LEFT= 0;
    }
    else{
     pw_LEFT = 0;
     done_LEFT = 1; 
    }
      
    if( Setpoint - clicks_RIGHT > EPSILON) {

       pw_RIGHT = pw_RIGHT + Output_RIGHT; 
       done_RIGHT= 0;
      
    }
    else{
      pw_RIGHT = 0;
      done_RIGHT = 1; 
    }
    
    
    
        if(pw_LEFT <0)
      pw_LEFT = 0;
      
        if(pw_RIGHT <0 )
      pw_RIGHT = 0;
    if(pw_LEFT > MAX_PWM_LEFT)
      pw_LEFT = MAX_PWM_LEFT;
      
        if(pw_RIGHT > MAX_PWM_RIGHT )
      pw_RIGHT = MAX_PWM_RIGHT;
      
    analogWrite(Motor_Driver.pwm_pin_right, pw_RIGHT);
    analogWrite(Motor_Driver.pwm_pin_left, pw_LEFT);
    


}


void get_command(){
  
       if(drive == STOP) {
     
         MsTimer2::stop();
        
        pw_RIGHT = 0; 
        pw_LEFT = 0;
        previous_clicks_RIGHT = 0;
        previous_clicks_LEFT = 0;
        clicks_LEFT = 0;
       clicks_RIGHT = 0;
       
       Setpoint = 0;
       
          
    }
    
  
    //Motor_Driver.Forward();
    if(Serial_Setpoint_Updated == 1){
     
         Setpoint = Serial_Setpoint ;
         Serial_Setpoint_Updated = 0;
    }

       
  if(done_RIGHT == 1 && done_LEFT == 1  ){
   
    
   
   MsTimer2::stop();
    
    
   Setpoint = 0;
 
    pw_RIGHT = 0; 
    pw_LEFT = 0;
    previous_clicks_RIGHT = 0;
    previous_clicks_LEFT = 0;
   clicks_LEFT = 0;
   clicks_RIGHT = 0;
   done_RIGHT = 0;
    done_LEFT = 0;
  
//   Motor_Driver.Reset();
    delay(1000);
    
    
    
   if(drive == FORWARD) {
        
          
          Motor_Driver.Forward();
      }
      
      else if(drive == LEFT) {
        Motor_Driver.Left();
      }  
//      
      else if(drive == RIGHT) {
        Motor_Driver.Right();
      }
//      
            else if(drive == BACKWARD) {
        Motor_Driver.Backward();
      }
//      
      else {
       Motor_Driver.Stop();
      }    
    
    
    MsTimer2::start(); 
   
  }
  
  
  

    
 
  
  
}

