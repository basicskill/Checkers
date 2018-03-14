import pygame.camera as cam
from pygame.image import save as sejv

def getImage():
	cam.init()
	k = cam.Camera(cam.list_cameras()[0])
	k.start()
	img = k.get_image()
	sejv(img, "tabla.jpg")
	k.stop()
