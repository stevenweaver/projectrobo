//This uses a voltage divider. Put into analog
int sensorPin = 0;    // select the input pin for the potentiometer
//int ledPin = 13;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor

void setup() {
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);    
  // stop the program for <sensorValue> milliseconds:
  Serial.println();
  Serial.print(sensorValue);          
  // stop the program for for <sensorValue> milliseconds:
  delay(500);                  
}
