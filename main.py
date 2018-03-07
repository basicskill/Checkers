from board import board
from minmax import minMax2
from from_camera import boardDiff, getState
from time import sleep
from constants import DIM, firstPlayer

b = board(DIM, DIM, firstPlayer)

b.printBoard()


## TODO: exceptioni, pipe 

while b.gameWon == -1:
    
    bStanje, wStanje = getState(b)
    try:
        wMove = boardDiff(b, bStanje, wStanje, 'r')
        b.moveWhite(*wMove)
    except Exception as err:
        b.gameWon = 1 ## !!!
        print(err)
        continue
    
    b1 = minMax2(b)[0]

    print('*********KOMP*********')
    b = b1
    b.printBoard()

    if b.gameWon == b.WHITE:
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        print("Black\nGame Over")