#For on robot or from flex
#import serial

#ser = serial.SerialPort('/dev/ttyUSB0', 9600)

#For dev
ser = open('../libs/sample_serial', 'r+')
sd = sensorData(sxml)
print flex_check

def flex_check(x): 

    result = {
    'RED ALERT': lambda x: x > 5,
      'b': lambda x: x + 7,
      'c': lambda x: x - 2
     }[value](x)

return result

