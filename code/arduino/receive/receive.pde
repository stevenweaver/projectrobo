#include <string.h>
#include <Messenger.h>
#define MAXSIZE 8 
//Need a string


Messenger message = Messenger(); 
char recvData[MAXSIZE];
int incomingByte;

void setup() {
  //Serial Communication
  Serial.begin(9600);  
  //message.attach(messageReady);
}

void loop() {
    //sendSerialInfo(us_val,flex_val,right_us_val,right_flex_val,compass_val);
    receiveData();
}


void receiveData() {
        int count = 0;
        int flag = 0;
        memset(recvData, 0, 8);       
        while(count <= 8) {
  	  while (Serial.available() > 0) {
		// read the incoming byte:
		incomingByte = Serial.read();
                recvData[count] = byte(incomingByte);
                count++;
                flag  = 1;
	  }
        }
        if(flag){
          Serial.println(recvData);
        }
        Serial.flush();
}



