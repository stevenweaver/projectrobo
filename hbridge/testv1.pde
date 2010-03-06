#define MOTOR_B_ENABLE 9
#define MOTOR_B_L3 10
#define MOTOR_B_L4 11
#define MOTOR_A_ENABLE 4
#define MOTOR_A_L1 2
#define MOTOR_A_L2 3
 
 
 
#define IOP 53

int val_new;
int val_old;
int clicks = 0;
int turns = 0;

void setup()  {
  pinMode (MOTOR_A_ENABLE,OUTPUT);
  pinMode (MOTOR_A_L1,OUTPUT);
  pinMode (MOTOR_A_L2,OUTPUT);
  pinMode (MOTOR_B_ENABLE,OUTPUT);
  pinMode (MOTOR_B_L3,OUTPUT);
  pinMode (MOTOR_B_L4,OUTPUT);
  
  
    Serial.begin(115200);
    pinMode(IOP, INPUT);
    val_new = digitalRead(IOP);
    val_old = val_new;
    
    
   analogWrite(MOTOR_B_ENABLE,255);
   analogWrite(MOTOR_B_L3,0);
   analogWrite(MOTOR_B_L4,255);
   
   
   analogWrite(MOTOR_A_ENABLE,255);
   analogWrite(MOTOR_A_L1,255);
   analogWrite(MOTOR_A_L2,0);
}
  
void loop()                     
{
   
    //analogWrite(PWM, 80);
    val_new = digitalRead(IOP);
    
    if(val_new != val_old) {
        if(clicks == 10) {
            clicks = 1;
            turns++;
            Serial.print("TURNS: ");
            Serial.println(turns);   
        }
        else clicks++;
        
        Serial.print("CLICKS: ");
        Serial.println(clicks);
        val_old = val_new;
    }
   if(turns == 100){
   
   analogWrite(MOTOR_B_ENABLE,0);
   
   
   analogWrite(MOTOR_A_ENABLE,0);
   
   delay (3000);
      analogWrite(MOTOR_B_ENABLE,255);
   
   
   analogWrite(MOTOR_A_ENABLE,255);
   
   turns = 0;
   }
}

