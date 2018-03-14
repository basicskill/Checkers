from board import board
from from_camera import boardDiff
from time import sleep
from constants import tPotez
from from_camera import getState
import serial

def peaceReset(ser, b, kamera):
    difference = 2
    while difference != 0:
        turnLED(ser, b.whitelist, b.blacklist)
        sleep(tPotez)
        turnOffLED(ser)
        bState, wState = getState(b, kamera)
        difference = boardDiff(b, bState, wState)
        

def turnLED(ser, bPolja, wPolja):
    for polje in bPolja:
        if polje[1] // 2 == 0:
            signal = str(polje[1]) + str((polje[0]+1) // 2)  + 'b'
        else:
            signal = str(polje[1]) + str((polje[0]) // 2) + 'b'
        ser.write(signal)

    for polje in wPolja:
        if polje[1] // 2 == 0:
            signal = str(polje[1]) + str((polje[0]+1) // 2)  + 'c' # !!
        else:
            signal = str(polje[1]) + str((polje[0]) // 2) + 'c' # !!
        serial = bytes(signal, 'utf-8')
        ser.write(serial)

def turnOffLED(ser):
    ser.write(b'k')