import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT
import time, random

class CObjet:
    
    
    def __init__(self):
        self.x, self.y = 0, 0
        self.xD, self.yD = 0.0, 0.0
        self.objet = random.choice([VAR.C_OBJ_BOMBE, VAR.C_OBJ_COUP, VAR.C_OBJ_ROLLER, VAR.C_OBJ_FLAMME])
    
    def Afficher(self):
        posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
        posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule)             
           
        animationId = int((time.time()*10) % 3)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["objets"], 0, 0, VAR.tailleCellule, VAR.tailleCellule), (posX, posY))
        
        
