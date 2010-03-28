#define MOTOR_B_ENABLE 6
#define MOTOR_B_L3 5
#define MOTOR_B_L4 7
#define MOTOR_A_ENABLE 3
#define MOTOR_A_L1 2
#define MOTOR_A_L2 4
 
 
 
#define ENCODER_A 53
#define ENCODER_B 53
//
int val_new_a;
int val_old_a;

int val_new_b;
int val_old_b;
int clicks_a = 0;
int clicks_b = 0;
//int turns = 0;

int pwm_a = 0;
int pwm_b = 0;

void setup()  {
  pinMode (MOTOR_A_ENABLE,OUTPUT);
  pinMode (MOTOR_A_L1,OUTPUT);
  pinMode (MOTOR_A_L2,OUTPUT);
  pinMode (MOTOR_B_ENABLE,OUTPUT);
  pinMode (MOTOR_B_L3,OUTPUT);
  pinMode (MOTOR_B_L4,OUTPUT);
  
  
   Serial.begin(9600);
    pinMode(ENCODER_A, INPUT);
    val_new_a = digitalRead(ENCODER_A);
    val_old_a = val_new_a;
    
    
        pinMode(ENCODER_B, INPUT);
    val_new_b = digitalRead(ENCODER_B);
    val_old_b = val_new_b;
//    
    
   analogWrite(MOTOR_B_ENABLE,0);
   analogWrite(MOTOR_B_L3,255);
   analogWrite(MOTOR_B_L4,0);
   
   
   analogWrite(MOTOR_A_ENABLE,0);
   analogWrite(MOTOR_A_L1,0);
   analogWrite(MOTOR_A_L2,255);
}
  
void loop()                     
{
  if (pwm_a != 255)
    for (int i=0; i < 256; i++){
      analogWrite(MOTOR_A_ENABLE,i);
      analogWrite(MOTOR_B_ENABLE,i);
      delay(100);
      
      pwm_a = i;
      Serial.print("Current PWM : ");
      Serial.println(i);
   } 
   
   
   
  


//    //analogWrite(PWM, 80);
   val_new_a = digitalRead(ENCODER_A);
     val_new_b = digitalRead(ENCODER_B);
//    
    if(val_new_a != val_old_a) {
//        if(clicks == 1000) {
//            clicks = 0;
////            turns++;
////            Serial.print("TURNS: ");
////            Serial.println(turns);   
//        }
         clicks_a++;
//        
        Serial.print("CLICKS A: ");
        Serial.println(clicks_a);
        val_old_a = val_new_a;
    }
    
    
       if(val_new_b != val_old_b) {
////        if(clicks == 1000) {
////            clicks = 0;
//////            turns++;
//////            Serial.print("TURNS: ");
//////            Serial.println(turns);   
////        }
        clicks_b++;
////        
//        Serial.print("CLICKS B: ");
//        Serial.println(clicks_b);
        val_old_b = val_new_b;
    }
    
    
   if(clicks_a > 500){
     
      analogWrite(MOTOR_A_ENABLE,0);
      analogWrite(MOTOR_B_ENABLE,0);
      
                 Serial.print("CLICKS A: ");
        Serial.println(clicks_a);
             Serial.print("CLICKS B: ");
        Serial.println(clicks_b);
        delay(3000);
     
    pwm_a = 0;
    clicks_a = 0;
     clicks_b = 0;
     

//   
//   analogWrite(MOTOR_B_ENABLE,0);
//   
//   
//   analogWrite(MOTOR_A_ENABLE,0);
//   
//   delay (3000);
//      analogWrite(MOTOR_B_ENABLE,255);
//   
//   
//   analogWrite(MOTOR_A_ENABLE,255);
//   
//   turns = 0;
   }
}

