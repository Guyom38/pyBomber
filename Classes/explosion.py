import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

from Classes.moteur import *
import time




class CExplosion():           
    def __init__(self, _moteur, _x, _y, _force):
        self.MOTEUR = _moteur
        self.progression = 0
        self.maxProgression = _force
        
        self.FOYER = []
        self.FOYER.append((_x, _y))
        self.x, self.y = _x, _y
        self.force = _force
        
        self.temps = time.time()
    
    def Gestion_Explosion(self):
        celluleD, celluleG, celluleH, celluleB = True, True, True, True
        
        for force in range(1, self.force):
           celluleD = (self.MOTEUR.TERRAIN.GRILLE[self.x-force][self.y] == VAR.C_SOL and celluleD)
           celluleG = (self.MOTEUR.TERRAIN.GRILLE[self.x+force][self.y] == VAR.C_SOL and celluleG)
           celluleH = (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-force] == VAR.C_SOL and celluleH)
           celluleB = (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y+force] == VAR.C_SOL and celluleB)
           
           if celluleD: self.FOYER.append((self.x-force, self.y))
           if celluleG: self.FOYER.append((self.x+force, self.y))
           if celluleH: self.FOYER.append((self.x, self.y-force))
           if celluleB: self.FOYER.append((self.x, self.y+force))
           


    
    def Afficher(self):
        self.Gestion_Explosion()
        
        for x, y in self.FOYER:
            posX = VAR.offSet[0] + (x * VAR.tailleCellule)
            posY = VAR.offSet[1] + (y * VAR.tailleCellule)
            pygame.draw.rect(VAR.fenetre, (255,0,0), (posX, posY, VAR.tailleCellule, VAR.tailleCellule))
    