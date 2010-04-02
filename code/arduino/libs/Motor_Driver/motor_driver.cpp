
// create a directory named Motor_Driver in libraries directory of arduino and add 
// this file(motor_driver.cpp) and motor_driver.h in it to have motor_driver library


#include <motor_driver.h>
#include <wiring.h>




Motor_Driver:: Motor_Driver(int enable_a , int control_1_a, int  control_2_a, 
			                int enable_b , int control_1_b, int  control_2_b )
{

  enable_pin_a = enable_a;
  control_1_pin_a = control_1_a;  
  control_2_pin_a = control_2_a;


 

  enable_pin_b = enable_b;
  control_1_pin_b = control_1_b;  
  control_2_pin_b = control_2_b;


 

  
  pinMode (enable_pin_a,OUTPUT);   
  pinMode (control_1_pin_a,OUTPUT);   
  pinMode (control_2_pin_a,OUTPUT);  
  

  pinMode (enable_pin_b,OUTPUT);   
  pinMode (control_1_pin_b,OUTPUT);   
  pinMode (control_2_pin_b,OUTPUT);  
  
 

}






void Motor_Driver:: Forward()
{
	analogWrite(enable_pin_a,0);    
	analogWrite(control_1_pin_a,0);    
	analogWrite(control_2_pin_a,255);

    analogWrite(enable_pin_b,0);    
	analogWrite(control_1_pin_b,0);    
	analogWrite(control_2_pin_b,255);


}

void Motor_Driver:: Backward()
{
	analogWrite(enable_pin_a,0);    
	analogWrite(control_1_pin_a,255);    
	analogWrite(control_2_pin_a,0);

    analogWrite(enable_pin_b,0);    
	analogWrite(control_1_pin_b,255);    
	analogWrite(control_2_pin_b,0);
}


void Motor_Driver::  Stop()
{


    analogWrite(enable_pin_a,0);    
	analogWrite(control_1_pin_a,0);    
	analogWrite(control_2_pin_a,0);

    analogWrite(enable_pin_b,0);    
	analogWrite(control_1_pin_b,0);    
	analogWrite(control_2_pin_b,0);
  
}


