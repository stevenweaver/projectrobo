
// create a directory named Motor_Driver in libraries directory of arduino and add 
// this file(motor_driver.h) and  motor_driver.cpp in it to have motor_driver library

#ifndef Motor_Driver_h

class Motor_Driver
{


  public:


Motor_Driver(int enable_pin_a , int control_1_pin_a, int  control_2_pin_a,
			 int enable_pin_b , int control_1_pin_b, int  control_2_pin_b);


void Forward();

void Backward();

void Right();

void Left();


void Stop();





private:

	int enable_pin_a, control_1_pin_a, control_2_pin_a, enable_pin_b, control_1_pin_b, control_2_pin_b;
 

};

#endif
