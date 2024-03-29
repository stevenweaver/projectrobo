#include <Wire.h>
#include <string.h>
#include <Servo.h> 
#include <Metro.h> 
#include <MsTimer2.h>


//*********GLOBAL CONSTANTS*******************//
#define MAX_STRING 255 

//ARDUINO PINS
#define LEFT_FLEX_PIN 0
#define RIGHT_FLEX_PIN 1  
#define LEFT_ULTRASONIC_PIN 11 
#define RIGHT_ULTRASONIC_PIN 12

#define LEFT_BEACON_INT  4  //Interrupt 0 
#define RIGHT_BEACON_INT 5  //Interrupt 1  

//Servo Constants
#define SERVO_PIN 4
#define HMC6352Address 0x42

//Beacon Constants
#define NA -1
#define STRAIGHT 0
#define LEFT 1
#define RIGHT 2

/*******************GLOBAL VARIABLES*****************/


//For the compass
int slave_address;

//For the servo
Servo myservo;

//Servo Variables
//Should take out of global
int back = 0;
int pos = 90;
int beacon_flag = 1;

//Beacon Specific Variables
volatile float left_time = 0;
volatile float right_time = 3000;
int beacon_dir = NA;
int compass_val = 0;

//Our "protothreading"
Metro serialMetro = Metro(250);
Metro servoMetro = Metro(10);

char xml[MAX_STRING];

int flag_LEFT = 0, flag_RIGHT = 0;


/*******************SETUP*****************/
void setup() {
  //Serial Communication
  Serial.begin(9600);  

  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slave_address = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI

  //For the compass(I2C communication)
  Wire.begin();

  //Telling which pin the servo is on. 
  myservo.attach(SERVO_PIN);
  
  //Set up US pins
  pinMode(LEFT_ULTRASONIC_PIN, INPUT);
  pinMode(RIGHT_ULTRASONIC_PIN, INPUT);

  //Interrupts for the Beacons. 
  attachInterrupt(LEFT_BEACON_INT, left_beacon, CHANGE);
  attachInterrupt(RIGHT_BEACON_INT, right_beacon, CHANGE);
  
  MsTimer2::set(30, servo); // 500ms period
  MsTimer2::start();


  }

/*******************MAIN*****************/
void loop() {
    int left_us_val, left_flex_val, right_us_val, right_flex_val = 0;
    int compass_val = 0;
    
    if (serialMetro.check() == 1) { // check if the metro has passed it's interval .
        //get information
        left_us_val       = ultrasonic(LEFT_ULTRASONIC_PIN);
        right_us_val      = ultrasonic(RIGHT_ULTRASONIC_PIN);
        left_flex_val     = flex(LEFT_FLEX_PIN);
        right_flex_val    = flex(RIGHT_FLEX_PIN);
        compass_val       = compass();

        //send serial info
        sendSerialInfo(left_us_val, left_flex_val, right_us_val, right_flex_val, compass_val, pos);

        serialMetro.reset();
    }
    
    //if (servoMetro.check() == 1) { // check if the metro has passed it's interval .

        //servoMetro.reset();
        
        
         //   Serial.println("Millis");  
 //  Serial.println(millis());
   
    //}
}

/***************SENSOR FUNCTIONS***************/

void servo() {
  
  

     
     
//       //This needs fixed up
//      if(beacon_dir == LEFT) {
//        if(pos >= 135) {
//           beacon_dir = NA; 
//           right_time = 0;
//           left_time = 0;
//        }
//        pos++;
//        delay(10);
//      }
//      else if(beacon_dir == RIGHT) {
//        if(pos <= 45) {
//           beacon_dir = NA; 
//           right_time = 0;
//           left_time = 0;
//        }
//        pos--;
//        delay(10);
//      }
//      else if(beacon_dir == STRAIGHT) {
//        //Check if we have interapt
////          int current_time = millis();
////          Serial.print("current_time: ");
////          Serial.println(current_time);
////          Serial.print("left time difference");
////          if (((current_time - left_time) > 800)||((current_time - right_time) > 800)){
////            left_time = 0;
////            right_time = 0;
////            beacon_dir = NA; 
//          }
//          
//       
//            
//            
//      }

if (millis() - right_time > 2000 && millis() - left_time > 2000){

   right_time = 0;
   //left_time = 0;
   left_time = 2000;
   
}
   

      
      
          // if (left_time - right_time > 50 || right_time - left_time > 500){
   
        if (millis() - left_time  > 200 || millis()- right_time > 200){
  
           

      //Else beacon_dir is unavailable... sweep
    
        if(pos >= 135) {
          back = 1; 
        }
        
        else if(pos <= 45) {
          back = 0; 
        }
      
        if(back == 0)
          pos = pos+1;   
      
        else
          pos = pos-1;  
          
          
      
            myservo.write(pos);
                    // tell servo to go to position in variable 'pos'  
                    
   }
//  else if ( left_time - right_time < 100)
//  {
//         pos = pos;  
//      
//        myservo.write(pos);
//  }
//  else if( left_time - right_time < 500){
//    pos++;
//    myservo.write(pos);
//  }
//    else if( right_time- left_time < 500){
//    pos--;
//    myservo.write(pos);
 // }
   else if (millis() - left_time > 0 &&  millis() - right_time > 0){    
      pos = pos;  
      
      myservo.write(pos);
   }
}

int ultrasonic(int pin) {
    //Used to read in the pulse that is being sent by the MaxSonar device.
    //Pulse Width representation with a scale factor of 147 uS per Inch.
    //Will package in Inches for now
    long pulse, inches;

    pulse = pulseIn(pin, HIGH);
    inches = pulse/147;
    return pulse;
}

int flex(int pin) {
    int sensor_value = 0;
    // read the value from the sensor:
    sensor_value = analogRead(pin);       
    return sensor_value;
}

int compass() {
    byte heading_data[2];
    int i;
    int heading_value;
    
    // Send a "A" command to the HMC6352
    // This requests the current heading data
    Wire.beginTransmission(slave_address);
    Wire.send("A");              // The "Get Data" command
    Wire.endTransmission();
    //delay(10);                   
    
    // The HMC6352 needs at least a 70us (microsecond) delay
    // after this command.  Using 10ms just makes it safe
    // Read the 2 heading bytes, MSB first
    // The resulting 16bit word is the compass heading in 10th's of a degree
    // For example: a heading of 1345 would be 134.5 degrees
    
    Wire.requestFrom(slave_address, 2);        // Request the 2 byte heading (MSB comes first)
    i = 0;
    
    while(Wire.available() && i < 2)
    { 
      heading_data[i] = Wire.receive();
      i++;
    }
    heading_value = heading_data[0]*256 + heading_data[1];  // Put the MSB and LSB together
    return heading_value;
}


/*************CREATE XML FOR BEAGLEBOARD************/
void sendSerialInfo(int left_us_val, int left_flex_val,int right_us_val, int right_flex_val, int compass_val, int pos)
{
    //  float compass =   (compass_val / 10) + (compass_val % 10); 
    sprintf(xml,"<?xml version=\"1.0\"?><sensor><c>%d</c><f><l>%d</l><r>%d</r></f><us><l>%d</l><r>%d</r></us><b>%d</b></sensor>", compass_val, left_flex_val, right_flex_val, left_us_val, right_us_val, pos); 
    Serial.println(xml);
    return;
}

//INTERRUPTS//
void left_beacon() {
 left_time = millis();
 
}

void right_beacon() {
 
    right_time = millis();
  



}
