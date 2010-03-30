

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

double Setpoint, Input, Output;

PID myPID(&Input, &Output, &Setpoint,6,4,1);


volatile int clicks_a = 0;
volatile int clicks_b = 0;
//int turns = 0;

int pwm_a = 0;
int pwm_b = 0;
int turns_a = 0;

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
  // attachInterrupt(1, motor_b_tick, FALLING);
  
  myPID.SetInputLimits(0,20000);
  //myPID.SetOutputLimits(0,100);
  //  //initialize the variables we're linked to
  Input = clicks_a;
  Setpoint = 2000;
//
//  //turn the PID on
  myPID.SetMode(AUTO);
}
  
void loop()                     
{
  
  
   //Set Tuning Parameters based on how close we are to setpoint
   if(abs(Setpoint-Input)>200)myPID.SetTunings(6,4,1);  //aggressive
   else myPID.SetTunings(3,4,1); //comparatively moderate

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
   
   Input = clicks_a;
   //  Input = analogRead(0);
  myPID.Compute();
//  analogWrite(3,Output);

      analogWrite(MOTOR_A_ENABLE,Output);
    analogWrite(MOTOR_B_ENABLE,Output);

  
//    Serial.print("Current turns A : ");
//    Serial.println(clicks_a);
    
   
   
        Serial.print("Current input : ");
      Serial.println(Input);
              Serial.print("Current output : ");
      Serial.println(Output);
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



