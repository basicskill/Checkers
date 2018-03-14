from board import board
from subprocess import Popen, PIPE
from constants import DIM, tPotez
from time import sleep
from pygame.image import save as sejv
from collections import Counter

def pomocni_print(geter):
    st = ''
    for figura in geter:
        st += figura
        if len(st) == 6:
            print(st)
            st = ''

def getImage(kamera):
    kamera.start()
    img = kamera.get_image()
    sejv(img, "tabla.png")
    kamera.stop()

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
    #if abs(bMove[0][0] - bMove[1][0] == 2) and abs(bMove[0][1] - bMove[1][1] == 2):
    #    return bMove[0], bMove[1], b.BLACK
    return bMove[0], bMove[1]

def getState(b, kamera):
    """
        Vraca listu crnih pa crvenih figura
    """    

    blist = []
    wlist = []

    getImage(kamera)
    binCL = []
    bwvL = []
    redSL = []
    redVL = []
    for thrash in listaTresholda: 
        for bwv in bwvL:
            for redS in redSL:
                for redV in redVL:
                    geter = Popen(["./output {}".format(thrash)], stdout=PIPE).communicate()[0].lower().split()
                    geter = [x.decode("utf-8") for x in geter]
                    if geter == ['-1']:
                        print('Neispravna detekcija!')
                        sleep(tPotez)
                        return getState(b, kamera)
                    kaunter = Counter(geter)
                    if not((kaunter['b'] == 6) and (kaunter['r'] == 6) and (kaunter['w'] == 24)):
                        print('Los broj figura!')
                        pomocni_print(geter)
                        sleep(tPotez)
                        return getState(b, kamera)
                    pomocni_print(geter)


    for char in range(0, len(geter)):
        if geter[char] == 'w':
            continue
        y = char // DIM
        x = char % DIM                
        if geter[char] == 'b':
            blist.append((x, y))
        if geter[char] == 'r':
            wlist.append((x, y))

    return blist, wlist


