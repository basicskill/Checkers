import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.write(b'k')
for i in range(0, 3):
	for j in range(0, 3):
			sleep(3)
			dioda = str(2*i) + str(2*j) + 'b' 
			print(dioda)
			signal = bytes(dioda, 'utf-8')
			ser.write(signal)
			sleep(3)
			ser.write(b'k')
