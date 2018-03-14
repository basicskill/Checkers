from board import board
from from_camera import boardDiff
import serial

def peaceReset(b):
    turnLED(b.whitelist, b.blacklist)
    pass

def turnLED(bPolja, wPolja):
    print(bPolja)
    #ser = serial.Serial('/dev/ttyUSB0', 9600)
    for polje in bPolja:
        if polje[1] // 2 == 0:
            signal = str(polje[1]) + str((polje[0]+1) // 2)  + 'b'
        else:
            signal = str(polje[1]) + str((polje[0]) // 2) + 'b'
        #ser.write(signal)
        print(signal) # proveriti za sva polja

    for polje in wPolja:
        print((str(polje[0] // 2) + str(polje[1] //2) + 'r')) ## POGLEDAJ SERIJSKU KONEKCIJU !!!!