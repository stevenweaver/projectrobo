
// create a directory named Motor_Driver in libraries directory of arduino and add 
// this file(motor_driver.cpp) and motor_driver.h in it to have motor_driver library


#include <motor_driver.h>
#include <wiring.h>




Motor_Driver:: Motor_Driver(int enable_right , int control_1_right, int  control_2_right, 
			                int enable_left , int control_1_left, int  control_2_left )
{

  enable_pin_right = enable_right;
  control_1_pin_right = control_1_right;  
  control_2_pin_right = control_2_right;


 

  enable_pin_left = enable_left;
  control_1_pin_left = control_1_left;  
  control_2_pin_left = control_2_left;


 

  
  pinMode (enable_pin_right,OUTPUT);   
  pinMode (control_1_pin_right,OUTPUT);   
  pinMode (control_2_pin_right,OUTPUT);  
  

  pinMode (enable_pin_left,OUTPUT);   
  pinMode (control_1_pin_left,OUTPUT);   
  pinMode (control_2_pin_left,OUTPUT);  
  
 

}






void Motor_Driver:: Forward()
{
	//analogWrite(enable_pin_a,255);    
	//analogWrite(control_1_pin_a,0);    
	
		digitalWrite(enable_pin_right,HIGH);    
	digitalWrite(control_1_pin_right,LOW);   
	


	//analogWrite(control_2_pin_a,255);

   // analogWrite(enable_pin_b,255);    
	//analogWrite(control_1_pin_b,0);    
	//analogWrite(control_2_pin_b,255);

       // digitalWrite(enable_pin_a, HIGH);

	     //digitalWrite(control_1_pin_b, LOW);   
	// digitalWrite(control_2_pin_a, LOW);


			digitalWrite(enable_pin_left,HIGH);    
	digitalWrite(control_1_pin_left,LOW);   
	

	// digitalWrite(enable_pin_b, HIGH);

	// digitalWrite(control_2_pin_b, LOW);

    // digitalWrite(control_1_pin_b, LOW);   
	// digitalWrite(control_2_pin_b, HIGH);

	pwm_pin_right = control_2_pin_right;
	pwm_pin_left = control_2_pin_left;

}

void Motor_Driver:: Backward()
{
	//analogWrite(enable_pin_a,0);    
//	analogWrite(control_1_pin_a,255);    
	//analogWrite(control_2_pin_a,0);

    digitalWrite(enable_pin_right,HIGH);    
	digitalWrite(control_2_pin_right,LOW);   
	


	    digitalWrite(enable_pin_left,HIGH);    
	digitalWrite(control_2_pin_left,LOW);  
   // analogWrite(enable_pin_b,0);    
	////analogWrite(control_1_pin_b,255);    
	//analogWrite(control_2_pin_b,0);

		pwm_pin_right = control_1_pin_right;
	    pwm_pin_left = control_1_pin_left;
}

void Motor_Driver:: Right()
{
	//analogWrite(enable_pin_a,0);    
	//analogWrite(control_1_pin_right,255);    
	//analogWrite(control_2_pin_right,0);

  //  analogWrite(enable_pin_b,0);    
//	analogWrite(control_1_pin_left,0);    
	//analogWrite(control_2_pin_left,255);

	 digitalWrite(enable_pin_right,HIGH);
     digitalWrite(enable_pin_left,HIGH);


		   digitalWrite(control_1_pin_left,LOW);
		 digitalWrite(control_2_pin_right,LOW);


	 pwm_pin_right = control_1_pin_right;

	 pwm_pin_left = control_2_pin_left;
}


void Motor_Driver:: Left()
{
	//analogWrite(enable_pin_a,0);    
	//analogWrite(control_1_pin_right,0);    
	//analogWrite(control_2_pin_right,255);

   // analogWrite(enable_pin_b,0);    
	//analogWrite(control_1_pin_left,255);    
	//analogWrite(control_2_pin_left,0);


		 digitalWrite(enable_pin_right,HIGH);
     digitalWrite(enable_pin_left,HIGH);


	 		   digitalWrite(control_2_pin_left,LOW);
		 digitalWrite(control_1_pin_right,LOW);


	 
	 pwm_pin_right = control_2_pin_right;

	 pwm_pin_left = control_1_pin_left;
}


void Motor_Driver::  Stop()
{


 		 digitalWrite(enable_pin_right,LOW);
     digitalWrite(enable_pin_left,LOW);

	 
	 		   digitalWrite(control_1_pin_left,LOW);
		 digitalWrite(control_1_pin_right,LOW);
		 
	 		   digitalWrite(control_2_pin_left,LOW);
		 digitalWrite(control_2_pin_right,LOW);
}


