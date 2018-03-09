from board import board
from minmax import minMax2 as minMax
from from_camera import boardDiff, getState
from to_arduino import peaceReset
from time import sleep
from constants import DIM, firstPlayer, t

b = board(DIM, DIM, firstPlayer)

b.printBoard()


## TODO: exceptioni, pipe 

while b.gameWon == -1:
    
    print('*********PLAYER*********')
    bState, wState = getState(b)
    wMove, difference = boardDiff(b, bState, wState, 'r')
    
    if difference == 0:
        sleep(t)
        continue
    elif difference > 2:
        peaceReset(b)
        continue

    print(wMove)
    try:
        b.moveWhite(*wMove)
    except Exception as err:
        print("###################################33")
        pass # !!!!!!1

    print('*********COMPUTER*********')
    b = minMax(b)
    print(len(b))
    b = b[0]
    b.printBoard()

    while difference != 0:
        bState, wState = getState(b)
        bMove, difference = boardDiff(b, bState, wState, 'b')
        if difference > 2:
            peaceReset(b)
            continue
        print('Cekam!')
        sleep(t)

    if b.gameWon == b.WHITE:
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        print("Black\nGame Over")