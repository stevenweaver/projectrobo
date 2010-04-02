

/********************************************************
 * PID Simple Example
 * Reading analog input 0 to control analog PWM output 3
 ********************************************************/

#include <PID_Beta6.h>

////Define Variables we'll be connecting to
//double Setpoint, Input, Output;
//
////Specify the links and initial tuning parameters
//PID myPID(&Input, &Output, &Setpoint,2,5,1);
//
//void setup()
//{
//  //initialize the variables we're linked to
//  Input = analogRead(0);
//  Setpoint = 100;
//
//  //turn the PID on
//  myPID.SetMode(AUTO);
//}
//
//void loop()
//{
//  Input = analogRead(0);
//  myPID.Compute();
//  analogWrite(3,Output);
//}
//



#define MOTOR_B_ENABLE 12
#define MOTOR_B_L3 11
#define MOTOR_B_L4 13
#define MOTOR_A_ENABLE 9
#define MOTOR_A_L1 8
#define MOTOR_A_L2 10
 
 
 


 
#define ENCODER_A 2 //  interrupt 0 
#define ENCODER_B 3 // interrupt 1
//
//int val_new_a;
//int val_old_a;
//
//int val_new_b;
//int val_old_b;

double Setpoint, Input_A, Input_B, Output_A, Output_B;

PID PID_A(&Input_A, &Output_A, &Setpoint,30,0,.4);
PID PID_B(&Input_B, &Output_B, &Setpoint,30,0,.4);

volatile int clicks_a = 0;
volatile int clicks_b = 0;
//int turns = 0;

int pwm_a = 0;
int pwm_b = 0;
int turns_a = 0;

unsigned long StartTime;

void setup()  {
  pinMode (MOTOR_A_ENABLE,OUTPUT);
  pinMode (MOTOR_A_L1,OUTPUT);
  pinMode (MOTOR_A_L2,OUTPUT);
  pinMode (MOTOR_B_ENABLE,OUTPUT);
  pinMode (MOTOR_B_L3,OUTPUT);
  pinMode (MOTOR_B_L4,OUTPUT);
  
  
   Serial.begin(9600);
//    pinMode(ENCODER_A, INPUT);
//    val_new_a = digitalRead(ENCODER_A);
//    val_old_a = val_new_a;
    
    
//        pinMode(ENCODER_B, INPUT);
//    val_new_b = digitalRead(ENCODER_B);
//    val_old_b = val_new_b;
//    
    
   analogWrite(MOTOR_B_ENABLE,0);
   analogWrite(MOTOR_B_L3,0);
   analogWrite(MOTOR_B_L4,255);
   
   
   analogWrite(MOTOR_A_ENABLE,0);
   analogWrite(MOTOR_A_L1,0);
   analogWrite(MOTOR_A_L2,255);
   
   attachInterrupt(0, motor_a_tick, FALLING);
   attachInterrupt(1, motor_b_tick, FALLING);
  
  PID_A.SetInputLimits(0,20000);
  PID_A.SetOutputLimits(20,255);
  
  PID_B.SetInputLimits(0,20000);
  PID_B.SetOutputLimits(20,255);
  //  //initialize the variables we're linked to
  Input_A = clicks_a;
  Input_B = clicks_b;
  Setpoint = 1000;
  Output_A = 0;
   Output_B = 0;
//
//  //turn the PID on
  PID_A.SetMode(AUTO);
  PID_B.SetMode(AUTO);
  StartTime = millis();

}
  
void loop()                     
{
  
//     if(millis()-StartTime<2000)
//   {
//     PID_A.SetTunings(2,0,.4);
//     PID_B.SetTunings(2,0,.4);
//   }
//   else  {
//     PID_A.SetTunings(30,0,.4);
//     PID_B.SetTunings(30,0,.4);
//   }
//   
   
        if(millis()-StartTime<2200)
   {
  PID_A.SetOutputLimits(20,100);
    PID_B.SetOutputLimits(20,85);
   }
   else  {
     PID_A.SetOutputLimits(15,245);
  PID_B.SetOutputLimits(15,230);
   }


   //Set Tuning Parameters based on how close we are to setpoint
  if(abs(Setpoint-Input_B)<200)  PID_B.SetOutputLimits(15,240);;  //aggressive
   //else myPID.SetTunings(3,4,1); //comparatively moderate



//  if (pwm_a == 0)
//    for (int i=0; i < 256; i += 16){
//      analogWrite(MOTOR_A_ENABLE,i);
//      analogWrite(MOTOR_B_ENABLE,i);
//      delay(100);
//      
//      pwm_a = i;
//      Serial.print("Current PWM : ");
//      Serial.println(i);
//      Serial.println(pwm_a);
//   } 
   
//   if ((clicks_a % 197) == 0){ 
//     clicks_a = 0;
//     turns_a++;
//    Serial.print("Current turns A : ");
//    Serial.println(turns_a);
//    
//   }
   
//      Serial.print("Current turns A : ");
//   Serial.println(turns_a);
//   
   
   Input_A = clicks_a;
    Input_B = clicks_b;
   //  Input = analogRead(0);
  PID_A.Compute();
  PID_B.Compute();
//  analogWrite(3,Output);

      analogWrite(MOTOR_A_ENABLE,Output_A);
      analogWrite(MOTOR_B_ENABLE,Output_B);

  
//    Serial.print("Current turns A : ");
//    Serial.println(clicks_a);
    
   
   
        Serial.print("Current input A: ");
      Serial.println(Input_A);
              Serial.print("Current output A: ");
      Serial.println(Output_A);
      
      
             Serial.print("Current input B: ");
      Serial.println(Input_B);
              Serial.print("Current output B: ");
      Serial.println(Output_B);
//   
//           Serial.print("Current click B : ");
//      Serial.println(clicks_b);
//  


//    //analogWrite(PWM, 80);
//   val_new_a = digitalRead(ENCODER_A);
//     val_new_b = digitalRead(ENCODER_B);
//    
//    if(val_new_a != val_old_a) {
////        if(clicks == 1000) {
////            clicks = 0;
//////            turns++;
//////            Serial.print("TURNS: ");
//////            Serial.println(turns);   
////        }
//         clicks_a++;
////        
//        Serial.print("CLICKS A: ");
//        Serial.println(clicks_a);
//        val_old_a = val_new_a;
//    }
    
//    
//       if(val_new_b != val_old_b) {
//////        if(clicks == 1000) {
//////            clicks = 0;
////////            turns++;
////////            Serial.print("TURNS: ");
////////            Serial.println(turns);   
//////        }
//        clicks_b++;
//////        
////        Serial.print("CLICKS B: ");
////        Serial.println(clicks_b);
//        val_old_b = val_new_b;
//    }
//    
//    
//   if(clicks_a > 500){
//     
//      analogWrite(MOTOR_A_ENABLE,0);
//      analogWrite(MOTOR_B_ENABLE,0);
//      
//                 Serial.print("CLICKS A: ");
//        Serial.println(clicks_a);
//             Serial.print("CLICKS B: ");
//        Serial.println(clicks_b);
//        delay(3000);
//     
//    pwm_a = 0;
//    clicks_a = 0;
//     clicks_b = 0;
//     
//
////   
////   analogWrite(MOTOR_B_ENABLE,0);
////   
////   
////   analogWrite(MOTOR_A_ENABLE,0);
////   
////   delay (3000);
////      analogWrite(MOTOR_B_ENABLE,255);
////   
////   
////   analogWrite(MOTOR_A_ENABLE,255);
////   
////   turns = 0;
//   }
}

void motor_a_tick()
{
  clicks_a++;
//     if ((clicks_a % 197) == 0){ 
//     clicks_a = 0;
//     turns_a++;
//     }
 
      //    Serial.print("Current click A : ");
  ///    Serial.println(clicks_a);
}


void motor_b_tick()
{
 clicks_b++;
 
          //  Serial.print("Current click B : ");
    //  Serial.println(clicks_b);
  
}



