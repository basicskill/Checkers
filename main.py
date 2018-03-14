from board import board
from minmax import minMax2 as minMax
from from_camera import boardDiff, getState, getPlayerMove, getPlayerMoveInverse, getComputerMove
from to_arduino import peaceReset, turnLED
from time import sleep
from constants import DIM, firstPlayer, t
import pygame.camera as cam

b = board(DIM, DIM, firstPlayer)

b.printBoard()

def spremiKameru(): 
    cam.init()
    kamera = cam.Camera(cam.list_cameras()[0])
    return kamera

while b.gameWon == -1:

    kamera = spremiKameru()

    print('*********PLAYER*********')
    bState, wState = getState(b, kamera)
    difference = boardDiff(b, bState, wState)

    if difference == 0:
        sleep(t)
        print('CEKAM')
        continue
    elif difference > 2:
        peaceReset(b)
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
            peaceReset(b)
        finally:
            pass
    finally:
        pass

    print('*********COMPUTER*********')
    b = minMax(b)[0]
    b.printBoard()
    bState, wState = getState(b, kamera)
    difference = boardDiff(b, bState, wState)
    
    computerMove = getComputerMove(b, bState)
    turnLED(computerMove, [])


    while difference != 0:
        if difference > 2:
            peaceReset(b)
            continue
        print('Cekam!')
        sleep(t)

    if b.gameWon == b.WHITE:
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        print("Black\nGame Over")