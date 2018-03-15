from board import board
from subprocess import Popen, PIPE
from constants import DIM, tPotez
from time import sleep
from pygame.image import save as sejv
from collections import Counter
import os

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
    sejv(img, "tabla.jpg")
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
def parsuj(geter):
    blist = []
    wlist = []
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

def getState(b, kamera):
    """
        Vraca listu crnih pa crvenih figura
    """    

    getImage(kamera)    
    
    # PARAMETRI:
    binDL = ['11', '21', '31']
    binCL = ['10', '20', '30']
    wvL = ['150', '175', '200']
    wsL = ['80', '100', '120', '150']
    bvL = ['80', '100', '120', '150']
    
    #for binD in binDL: 
    #    for binC in binCL:
    #        for wv in wvL:
    #            for ws in wsL:
    #                for bv in bvL:
    #komanda = './output' + ' ' + binD + ' ' + binC + ' ' + wv + ' ' + ws + ' ' + bv
    komanda = './output 11 100 150 120 100'
    geter = os.popen(komanda).read()
    #print(geter)
    if geter == '-1':
        print('Neispravna detekcija!' + komanda)
        return getState(b, kamera)
        #continue
    kaunter = Counter(geter)
    if not((kaunter['b'] == 6) and (kaunter['r'] == 6) and (kaunter['w'] == 24)):
        print('Los broj figura!' + komanda)
        pomocni_print(geter)
        return getState(b, kamera)
        #continue
    print('FOTOGRAFISANO!')
    geter1 = [x for x in reversed(geter)]
    #pomocni_print(geter)
    #print(b.blacklist)
    #print(b.whitelist)
    return parsuj(geter1)



