from sensorData import *
#from sendData import *

sxml= "<sensor><gps>rawdata</gps><compass>degree</compass><flex><left>number</left><right>number</right></flex><ultrasonic><left>6</left><right>7</right></ultrasonic><beacon>???</beacon><wheelencoder>???</wheelencoder></sensor>"

sd = sensorData(sxml)

print sd.us['right']
print sd.us['left']
