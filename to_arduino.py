from board import board
from from_camera import boardDiff

def peaceReset(b):
    polja = b.whitelist + b.blacklist
    turnLED(polja)
    pass

def turnLED(polja):
    for polje in polja:
        print(polje) ## POGLEDAJ SERIJSKU KONEKCIJU !!!!