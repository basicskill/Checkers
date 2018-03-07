from board import board
from subprocess import Popen, PIPE
from constants import DIM, DEBUG

def boardDiff(b, blist, wlist, boja):
    """
        Vraca promenu crnih ili crvenih figura.
        Ako je pomereno vise figura vraca gresku.
    """

    bmove = list(set(b.blacklist) - set(blist)) + list(set(blist) - set(b.blacklist))
    wmove = list(set(b.whitelist) - set(wlist)) + list(set(wlist) - set(b.whitelist))

    if (len(bmove) == 2 and 
        len(wmove) == 0) or (len(wmove) == 2 and len(bmove) == 0):
        if boja == 'b':
            return bmove[0], bmove[1], b.NOTDONE
        else:
            return wmove[0], wmove[1], b.NOTDONE
    if len(bmove) + len(wmove) == 0:
        raise Exception("Nepomereno!")
    if len(bmove) + len(wmove) == 2:
        raise Exception("1 razlika")
    raise Exception("Invalid move!")

def getState(b):
    """
        Vraca listu crnih pa crvenih figura
    """    

    blist = []
    wlist = []

    geter = Popen(["./output"], stdout=PIPE).communicate()[0].lower().split()
    if geter == '':
        return None
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


