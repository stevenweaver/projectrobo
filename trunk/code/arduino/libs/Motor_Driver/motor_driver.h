
// create a directory named Motor_Driver in libraries directory of arduino and add 
// this file(motor_driver.h) and  motor_driver.cpp in it to have motor_driver library

#ifndef Motor_Driver_h

class Motor_Driver
{


  public:


Motor_Driver(int enable_pin_right , int control_1_pin_right, int  control_2_pin_right,
			 int enable_pin_left , int control_1_pin_left, int  control_2_pin_left);


void Forward();

void Backward();

void Right();

void Left();

void Reset();


void Stop();


int pwm_pin_right, pwm_pin_left;


private:

	int enable_pin_right, control_1_pin_right, control_2_pin_right, enable_pin_left, control_1_pin_left, control_2_pin_left;
 

};

#endif
