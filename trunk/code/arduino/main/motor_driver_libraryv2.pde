#include <motor_driver.h>
#include <PID_Beta6.h>

// enable for motor A = 9
// control 1  for motor A = 8
// control 2  for motor A = 10
// Encoder for motor A = 2 (interrupt 0) 

// enable for motor B = 12
// control 1  for motor B = 11
// control 2  for motor B = 13
// Encoder for motor B = 3 (interrupt 1) 
// need interrupt attaching

Motor_Driver Motor_Driver(9, 8, 10, 12, 11 , 13);

volatile int clicks_a = 0; 
volatile int clicks_b = 0; 


int done = 0;

// PID stuff will be added here

double Setpoint, Input_A, Input_B, Output_A, Output_B;

PID PID_A(&Input_A, &Output_A, &Setpoint,30,0,.4);
PID PID_B(&Input_B, &Output_B, &Setpoint,30,0,.4);


unsigned long StartTime;
    
void setup()  
{
  // encoders are attached to interrupts 0 an 1 
  attachInterrupt(0, motor_a_tick, FALLING);    
  attachInterrupt(1, motor_b_tick, FALLING); 
  PID_A.SetInputLimits(0,20000);
  PID_A.SetOutputLimits(20,255);
  
  PID_B.SetInputLimits(0,20000);
  PID_B.SetOutputLimits(20,255);
  //  //initialize the variables we're linked to
  Input_A = clicks_a;
  Input_B = clicks_b;
 
  Output_A = 0;
   Output_B = 0;
//
//  //turn the PID on
  PID_A.SetMode(AUTO);
  PID_B.SetMode(AUTO);
  StartTime = millis();
  
  
    // we are in forward mode
  Motor_Driver.Forward();
  

  
   Setpoint = 1000;
   
   Serial.begin(9600);
}   

void loop()                     
{            
     if(millis() - StartTime >10000 && done == 1  ){
         Motor_Driver.Right();
              analogWrite(9, 60);
      analogWrite(12, 60);
   } 
  
   else 
   {
    Input_A = clicks_a;
  Input_B = clicks_b;
        if(millis()-StartTime<2200)
   {
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
  
  
      analogWrite(9, Output_A);
      analogWrite(12, Output_B);
      
      
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
void motor_a_tick() 
{   
  clicks_a++; 
}   

void motor_b_tick() 
{ 
  clicks_b++;        
} 
