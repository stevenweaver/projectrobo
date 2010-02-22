import serial

ser = serial.SerialPort('/dev/ttyUSB0', 9600)
print ser.readline()
