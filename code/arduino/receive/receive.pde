#include <string.h>
#include <Messenger.h>
#define MAXSIZE 30 

Messenger message = Messenger(); 
char string[MAXSIZE];


void setup() {
  //Serial Communication
  Serial.begin(9600);  
  message.attach(messageReady);
}

void loop() {
    //sendSerialInfo(us_val,flex_val,right_us_val,right_flex_val,compass_val);
    receiveData();
}


void receiveData() {
  while ( Serial.available() )  message.process(Serial.read () );
}

void messageReady() {
    int pin = 0;
       // Loop through all the available elements of the message
       while ( message.available() ) {
         message.copyString(string,MAXSIZE);
         Serial.print(string);
         Serial.println();
       }
}



