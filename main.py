from board import board
from minmax import minMax2 as minMax
from from_camera import boardDiff, getState, getPlayerMove, getPlayerMoveInverse
from to_arduino import peaceReset
from time import sleep
from constants import DIM, firstPlayer, t

b = board(DIM, DIM, firstPlayer)

b.printBoard()


## TODO: exceptioni, pipe 

while b.gameWon == -1:
    
    print('*********PLAYER*********')
    bState, wState = getState(b)
    difference = boardDiff(b, bState, wState)

    if difference == 0:
        sleep(t)
        continue
    elif difference > 2:
        peaceReset(b)
        continue
    
    
    wMove = getPlayerMove(b, bState, wState)
    try:
        b.moveWhite(*wMove)
    except Exception as err:
        print(err)
        wMove = getPlayerMoveInverse(b, bState, wState)
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

    while difference != 0:
        bState, wState = getState(b)
        difference = boardDiff(b, bState, wState)
        if difference > 2:
            peaceReset(b)
            continue
        print('Cekam!')
        sleep(t)

    if b.gameWon == b.WHITE:
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        print("Black\nGame Over")