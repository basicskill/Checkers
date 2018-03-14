from board import board
from subprocess import Popen, PIPE
from constants import DIM, tPotez
from time import sleep


def boardDiff(b, blist, wlist):
    """
        Returns number of different peace placements on the board
    """

    bDiff = list(set(b.blacklist) - set(blist)) + list(set(blist) - set(b.blacklist))
    wDiff = list(set(b.whitelist) - set(wlist)) + list(set(wlist) - set(b.whitelist))

    return len(wDiff) + len(bDiff)

def getPlayerMove(b, wList):
    wMove = list(set(b.whitelist) - set(wList)) + list(set(wList) - set(b.whitelist))
    if abs(wMove[0][0] - wMove[1][0] == 2) and abs(wMove[0][1] - wMove[1][1] == 2):
        return wMove[0], wMove[1], b.WHITE
    return wMove[0], wMove[1], b.NOTDONE

def getPlayerMoveInverse(b, wList):
    wMove = list(set(b.whitelist) - set(wList)) + list(set(wList) - set(b.whitelist))
    if abs(wMove[0][0] - wMove[1][0] == 2) and abs(wMove[0][1] - wMove[1][1] == 2):
        return wMove[1], wMove[0], b.WHITE
    return wMove[1], wMove[0], b.NOTDONE

def getComputerMove(b, bList):
    bMove = list(set(b.blacklist) - set(bList)) + list(set(bList) - set(b.blacklist))
    if abs(bMove[0][0] - bMove[1][0] == 2) and abs(bMove[0][1] - bMove[1][1] == 2):
        return bMove[0], bMove[1], b.BLACK
    return bMove[0], bMove[1], b.NOTDONE

def getState(b):
    """
        Vraca listu crnih pa crvenih figura
    """    

    blist = []
    wlist = []

    geter = Popen(["./output"], stdout=PIPE).communicate()[0].lower().split()
    if geter == ['-1']:
        sleep(tPotez)
        return getState(b)
    geter = [x.decode("utf-8") for x in geter]
    for char in range(0, len(geter)):
        if geter[char] == 'w':
            continue
        y = char // DIM
        x = char % DIM                
        if geter[char] == 'c':
            blist.append((x, y))
        if geter[char] == 'r':
            wlist.append((x, y))

    return blist, wlist


