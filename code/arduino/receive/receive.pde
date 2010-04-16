#include <string.h>

int drive=0; 
int ticks=0; 

char buff[]= "0000000000";

int incomingByte;

void setup() {
  //Serial Communication
  Serial.begin(9600);  
  //message.attach(messageReady);
}

void loop() {
    //sendSerialInfo(us_val,flex_val,right_us_val,right_flex_val,compass_val);
    //Serial.println("lol1");
    receiveData();
    Serial.println(drive);
}

void receiveData() {
  while (Serial.available()>0) {
    for (int i=0; i<10; i++) {
      buff[i]=buff[i+1];
    }
    buff[10]=Serial.read();
    if (buff[10]=='D') {
      drive=int(buff[9]) - 48;
    }
    if (buff[10]=='T') {
      ticks=int(buff[9]) - 48;
    }

  }
}
