#include <string.h>
#include <Messenger.h>
#define MAXSIZE 8 
//Need a string

Messenger message = Messenger(); 
char recvData[MAXSIZE];
char direction_command[MAXSIZE];
char number_ticks_command[MAXSIZE];

int incomingByte;

void setup() {
  //Serial Communication
  Serial.begin(9600);  
  //message.attach(messageReady);
}

void loop() {
    //sendSerialInfo(us_val,flex_val,right_us_val,right_flex_val,compass_val);
    Serial.println("lol1");
    receiveData();
    //Serial.println("lol2");
}

void receiveData() {
        int count = 0;
        int flag = 0;
        memset(recvData, 0, 8);       
        
        if(Serial.available()) {
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
            //We need to parse our information here
            parseRecvdData(recvData);
          }
        
        }

        //Serial.flush();
}

void parseRecvdData(char* recvData){
    int i,j = 0;
    int comma_flag = 0;
    
    //Serial.println("lol");
    memset(direction_command, 0, 8);  
    memset(number_ticks_command, 0, 8);  
    
    for(i=0;i <= MAXSIZE; i++){
      if(recvData[i] == ',') {
        i++;
        comma_flag = 1;
      }
      
      if(recvData[i] == '!') {
        break;  
      }
      
      if(!comma_flag) {
        direction_command[i] = recvData[i];
      }

      else {
        number_ticks_command[j] = recvData[i];
        j++;
      }

    }
    Serial.print("dir: ");
    Serial.println(direction_command);
    Serial.print("num_tix: ");
    Serial.println(number_ticks_command);
}

