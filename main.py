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
    
    bStanje, wStanje = getState(b)
    try:
        wMove = boardDiff(b, bStanje, wStanje, 'r')
        b.moveWhite(*wMove)
    except Exception as err:
        ## jedna razlika
        sleep(t)
        continue
    except Exception as err:
        ## vise od jedne greske
        peaceReset(b)
        continue
    
    b1 = minMax(b)[0]

    print('*********KOMP*********')
    b = b1
    b.printBoard()
    bStanje, wStanje = getState(b)
    bMove = boardDiff(b, bStanje, wStanje, 'b')
    
    while len(bMove != 0):

        if len(bMove) == 2:
            ## jedna razlika
            ## cekaj
            sleep(t)
            ## neki while
        else:
            pass
    
    


    if b.gameWon == b.WHITE:
        print("White\nGame Over")
    if b.gameWon == b.BLACK:
        print("Black\nGame Over")