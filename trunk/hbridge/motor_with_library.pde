#include <motor.h>

 


// define I/0 pins. 3 PWM for each motor
Motor Motor_A(1,2,3);
Motor Motor_B(4,5,6);


void setup()  
{





}   
void loop()                     
{            
  Motor_A.Stop();
  Motor_B.Stop();
  
  delay (3000);      
  Motor_A.Forward(255);
  Motor_B.Forward(255);  
   
} 



