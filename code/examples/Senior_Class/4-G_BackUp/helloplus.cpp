#include <iostream>
#include <SerialPort.h>
#include <SerialStream.h>

using namespace LibSerial;
using namespace std;

// Creates a LibSeria object
SerialStream serialStream;
SerialPort * serialPort;

// OPen Uart2
//serialPort = new SerialPort("/dev/ttyS1");

//serialPort->Open(SerialPort::BAUD_9600, SerialPort::CHAR_SIZE_DEFAULT,
//SerialPort::PARITY_DEFAULT, SerialPort::STOP_BITS_DEFAULT, 
//SerialPort::FLOW_CONTROL_NONE);

void initSerialPort( const string& serialDevString, SerialPort::BaudRate baudRate);


int main(void)
{
	initSerialPort("/dev/ttyS1", SerialPort::BAUD_115200);
	cout << "Hello, C++ in a Beagleboard" << endl;
	
	unsigned char status = 0x39;
	for(int x = 0; x < 1; x++)
		serialPort->WriteByte(status);

	for(int i = 0; i < 10000; i++)
	{
		for(int j=0; j< 10000; j++)
		{

		}
	}

	cout << "End for loop() " << endl;

	try
	{
		if(serialPort->IsOpen())
		{
			serialPort->Close();
		}
	}
	catch(...)
	{
		cout << "Could not close serial port" << endl;
	}

	cout << "Exit main" << endl;	
	return 0;
}

void initSerialPort( const string& serialDevString, SerialPort::BaudRate baudRate)
{
	
	serialPort = new SerialPort( serialDevString);

	try
	{
	serialPort->Open(baudRate, SerialPort::CHAR_SIZE_DEFAULT,
	SerialPort::PARITY_DEFAULT, SerialPort::STOP_BITS_DEFAULT, 
	SerialPort::FLOW_CONTROL_NONE);
	}
	catch(...)
	{
		cout << "Caught" << endl;


	}
	cout << "Serial port: " << serialDevString << " opened succesfully" << endl;

}


