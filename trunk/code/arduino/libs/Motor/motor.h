
// create a directory named motor in libraries directory of arduino and add 
// this file (motor.h) and motor.cpp  in it to have motor library

#ifndef motor_h

class Motor
{


  public:


Motor(int enable_pin , int control_1_pin, int  control_2_pin);


void Forward(int speed_value);

void Backward(int speed_value);


void Stop();


private:

	int enable_pin, control_1_pin, control_2_pin;

};

#endif


