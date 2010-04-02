#include <motor_driver.h>

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


// PID stuff will be added here
    
void setup()  
{
  // encoders are attached to interrupts 0 an 1 
  attachInterrupt(0, motor_a_tick, FALLING);    
  attachInterrupt(1, motor_b_tick, FALLING); 
}   

void loop()                     
{            
  // we are in forward mode
  Motor_Driver.Forward();
  
  
   
} 

void motor_a_tick() 
{   
  clicks_a++; 
}   

void motor_b_tick() 
{ 
  clicks_b++;        
} 
