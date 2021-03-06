from board import board
from from_camera import boardDiff
from time import sleep
from constants import tPotez
from from_camera import getState
import serial

## Uputstvo:
#   k - iskljuci sve
#   q - sve crvene
#   w - sve bele
#   brojb - svetli beli
#   brojc - svetli crveno

def peaceReset(ser, b): 
    print('RESET!')
    for _ in range(0, 1):
        ser.write(b'q')
        sleep(2)
        ser.write(b'k')
        sleep(2)
        ser.write(b'w')
        sleep(2)
        ser.write(b'k')
        sleep(2)
    turnLED(ser, b.blacklist, [])
    turnLED(ser, [], b.whitelist)


def turnLED(ser, bPolja, wPolja):
    if wPolja == []:
        Polja = bPolja
        c = 'b'
    else:
        Polja = wPolja
        c = 'c'

    for polje in reversed(Polja):
        print(polje)
        sleep(2)
        dioda = str(polje[1]) + str(5 - polje[0]) + c
        signal = bytes(dioda, 'utf-8')
        print(signal)
        ser.write(signal)
        sleep(2)
        ser.write(b'k')

