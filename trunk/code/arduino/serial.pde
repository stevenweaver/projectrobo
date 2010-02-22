//This uses a voltage divider. Put into analog
const int flexPin = 0;  // select the input pin for flex sensor 
const int urPin = 7;    // select the input pin for ultransonic range sensor 
int sensorValue = 0;    // variable to store the value coming from the sensor

//This variable is a constant because the pin will not change throughout execution of this code.
//variables needed to store values
long pulse, inches, cm;

void setup() {
  Serial.begin(9600);
}

void loop() {
    ultrasonic();
    flex();
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
}
