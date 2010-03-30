// Sweep
// by BARRAGAN <http://barraganstudio.com> 

#include <Servo.h> 
#include <Wire.h>
#include <string.h>
 
//*********GLOBAL CONSTANTS*******************//
//ARDUINO PINS
const int LEFT_BEACON_INT  = 0;   
const int RIGHT_BEACON_INT = 1; 

//Beacon Constants
const int NA = -1;
const int STRAIGHT = 0;
const int LEFT = 1;
const int RIGHT = 2;




Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
                
//Beacon Specific Variables
int left_time, right_time = 0;
int beacon_dir = NA;
int back = 0;


 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
   Serial.begin(9600); 
  //Interrupts for the Beacons. 
  attachInterrupt(LEFT_BEACON_INT, left_beacon, CHANGE);
  attachInterrupt(RIGHT_BEACON_INT, right_beacon, CHANGE);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
} 
 
 
void loop() 
{ 
  //This needs fixed up
  if(beacon_dir == LEFT) {
    if(pos >= 180) {
       beacon_dir = NA; 
       right_time = 0;
       left_time = 0;
    }
    pos++;
    delay(10);
  }
  else if(beacon_dir == RIGHT) {
    if(pos <= 0) {
       beacon_dir = NA; 
       right_time = 0;
       left_time = 0;
    }
    pos--;
    delay(10);
  }
  else if(beacon_dir == STRAIGHT) {
    //do nothing
  }
  //Else beacon_dir is unavailable... sweep
  else {
    if(pos >= 180) {
      back = 1; 
    }
    
    else if(pos <= 0) {
      back = 0; 
    }
  
    if(back == 0)
      pos = pos+1;   
  
    else
      pos = pos-1;  
  }

   myservo.write(pos);              // tell servo to go to position in variable 'pos'   
   delay(10);   
} 

void sendSerialInfo(int us_val, int flex_val,int right_us_val, int right_flex_val,int compass_val)
{
  Serial.println("</sensor>");
  Serial.println("");
  return;
}


void left_beacon() {
  int diff;
  if(!left_time){
    left_time = micros();
    beacon_dir = NA;
  }

  Serial.print("Saw Left Interrupt! TIME: ");
  Serial.println(left_time);
  beacon_dir = NA;
  if(right_time) {
    if((left_time - right_time) > 500) {  
      Serial.println("Beacon Right!");
      beacon_dir = RIGHT;
      right_time = 0;
      left_time = 0;
    }
    else {
      Serial.println("Beacon Straight!"); 
      beacon_dir = STRAIGHT;
      left_time = 0;
      right_time = 0;
    }
  }
}

void right_beacon() {
  int diff;
  
  if(!right_time){
    right_time = micros();
    beacon_dir = NA;
  }

  Serial.print("Saw Right Interrupt! TIME: ");
  Serial.println(right_time);

  if(left_time){
    if((right_time - left_time) > 500) {
      Serial.println("Beacon Left!");
      beacon_dir = LEFT;
      left_time = 0;
      right_time = 0;
    }    
    else {
      Serial.println("Beacon Straight!");
      beacon_dir = STRAIGHT;
      left_time = 0;
      right_time = 0;
    }  


  }
}  
