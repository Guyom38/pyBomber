import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

import time

class CBombe:
    def __init__(self, _x, _y, _force):
        self.delais = 5.0
        self.temps = time.time()
        self.force = _force
        
        self.x, self.y = _x, _y
        self.xD, self.yD = 0.0, 0.0
    
    def Afficher(self):
        posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
        posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule)             
           
        animationId = int((time.time()*10) % 3)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["objets"], animationId, 1, VAR.tailleCellule,  VAR.tailleCellule), (posX, posY))
