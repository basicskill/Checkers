from board import board
from minmax import minMax2 as minMax
from from_camera import boardDiff, getState, getPlayerMove, getPlayerMoveInverse, getComputerMove
from to_arduino import peaceReset, turnLED
from time import sleep
from constants import DIM, firstPlayer, t
import pygame.camera as cam
import serial

b = board(DIM, DIM, firstPlayer)


def spremiKameru(): 
    cam.init()
    kamera = cam.Camera(cam.list_cameras()[1])
    return kamera

kamera = spremiKameru()
ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.write(b'k')

### MAIN PROGRAM ###
while b.gameWon == -1:

    print('*********PLAYER*********')
    b.printBoard()
    bState, wState = getState(b, kamera)
    difference = boardDiff(b, bState, wState)

    while difference == 0:
        print('CEKAM')
        sleep(t)
        bState, wState = getState(b, kamera)
        difference = boardDiff(b, bState, wState)
        continue
    if difference > 2:
        peaceReset(ser, b)
        continue
    
    
    wMove = getPlayerMove(b, wState)
    try:
        b.moveWhite(*wMove)
    except Exception as err:
        print(err)
        wMove = getPlayerMoveInverse(b, wState)
        try:
            b.moveWhite(*wMove)
            b.printBoard()
        except Exception:
            peaceReset(ser, b)
        finally:
            pass
    finally:
        pass

    print('*********COMPUTER*********')
    b = minMax(b)[0]
    b.printBoard()

    difference = 2
    while difference != 0:
        bState, wState = getState(b, kamera)
        difference = boardDiff(b, bState, wState)
        if difference == 2:
            computerMove = getComputerMove(b, bState)
            turnLED(ser, computerMove, [])
        if difference > 2:
            peaceReset(ser, b)
        print('Cekam!')

    if b.gameWon == b.WHITE:
        ser.write(b'q')
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        ser.write(b'w')
        print("Black\nGame Over")