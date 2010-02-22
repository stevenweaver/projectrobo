//This uses a voltage divider. Put into analog
const int flexPin = 0;  // select the input pin for flex sensor 
const int urPin = 7;    // select the input pin for ultransonic range sensor 
int sensorValue = 0;    // variable to store the value coming from the sensor

//This variable is a constant because the pin will not change throughout execution of this code.
//variables needed to store values
long pulse, inches, cm;

//Compass
#include <Wire.h>
int HMC6352Address = 0x42;

// This is calculated in the setup() function
int slaveAddress;
byte headingData[2];
int i, headingValue;


void setup() {
  Serial.begin(9600);  
  // Shift the device's documented slave address (0x42) 1 bit right
  // This compensates for how the TWI library only wants the
  // 7 most significant bits (with the high bit padded with 0)
  slaveAddress = HMC6352Address >> 1;   // This results in 0x21 as the address to pass to TWI
  Wire.begin();
}

void loop() {
    //ultrasonic();
    //flex();
    compass();
    delay(500);                  
}

void ultrasonic() {
    pinMode(urPin, INPUT);
    //Used to read in the pulse that is being sent by the MaxSonar device.
    //Pulse Width representation with a scale factor of 147 uS per Inch.

    pulse = pulseIn(urPin, HIGH);
    //147uS per inch
    inches = pulse/147;
    //change inches to centimetres
    cm = inches * 2.54;
    Serial.print(inches);
    Serial.print("in, ");
    Serial.print(cm);
    Serial.print("cm");
    Serial.println();
}

void flex() {
    // read the value from the sensor:
    sensorValue = analogRead(flexPin);    
    Serial.println();
    Serial.print("flex:");          
    Serial.print(sensorValue);
    Serial.println();    
}

void compass() {
    // Send a "A" command to the HMC6352
    // This requests the current heading data
    Wire.beginTransmission(slaveAddress);
    Wire.send("A");              // The "Get Data" command
    Wire.endTransmission();
    delay(10);                   
    
    // The HMC6352 needs at least a 70us (microsecond) delay
    // after this command.  Using 10ms just makes it safe
    // Read the 2 heading bytes, MSB first
    // The resulting 16bit word is the compass heading in 10th's of a degree
    // For example: a heading of 1345 would be 134.5 degrees
    
    Wire.requestFrom(slaveAddress, 2);        // Request the 2 byte heading (MSB comes first)
    i = 0;
    
    while(Wire.available() && i < 2)
    { 
      headingData[i] = Wire.receive();
      i++;
    }
    headingValue = headingData[0]*256 + headingData[1];  // Put the MSB and LSB together
    Serial.print("Header: ");
    Serial.print(int (headingValue / 10));     // The whole number part of the heading
    Serial.print(".");
    Serial.print(int (headingValue % 10));     // The fractional part of the heading
    Serial.println(" degrees");
}
