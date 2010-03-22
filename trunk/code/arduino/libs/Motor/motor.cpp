
// create a directory named motor in libraries directory of arduino and add 
// this file(motor.cpp) and motor.h in it to have motor library

#include <wiring.h>

#include <motor.h>

Motor::Motor(int enable , int control_1, int  control_2)
{

  enable_pin = enable;
  control_1_pin = control_1;  
  control_2_pin = control_2;
  
  pinMode (enable_pin,OUTPUT);   
  pinMode (control_1_pin,OUTPUT);   
  pinMode (control_2_pin,OUTPUT);  


}

void Motor:: Forward(int speed_value)
{

	enable_pin = speed_value;
	control_1_pin= 0;
	control_2_pin= 255;  
}

void Motor:: Backward(int speed_value)
{
  enable_pin = speed_value;
  control_1_pin= 0;
  control_2_pin= 255;
  
}


void Motor::  Stop()
{
  enable_pin = 0;
  control_1_pin= 0;
  control_2_pin= 0;
  
}
