import pygame
from pygame.locals import *

import variables as VAR
import time, random
import item

import terrain as CT
from enums import *

class CCellule(item.CItem):
    def __init__(self, _moteur, _x, _y):
        super().__init__(_moteur, _x,_y, "")      
           
        self.objet = C_TERRAIN.SOL 
        self.casser = False
        
        
    def Traversable(self):
        return (self.objet == C_TERRAIN.SOL)
    
    def Cassable(self):
        return (self.objet == C_TERRAIN.CASSABLE)
    
    def Casser_Mur(self):
        self.temps = time.time()
        self.animationId = 0
        self.casser = True
        
    def Animation_Explosion_Mur(self):
        posX = VAR.offSet[0] + (self.x * VAR.tailleCellule)  + (VAR.tailleCellule / 2)
        posY = VAR.offSet[1] + (self.y * VAR.tailleCellule)  + (VAR.tailleCellule / 2)             
        self.MOTEUR.PARTICULES.Ajouter_Particule(posX, posY, (64,64,64,255))
        
        if time.time() - self.temps > 0.1:
            self.animationId += 1
            self.temps = time.time() 
            
        if self.animationId > 1:
            self.objet = C_TERRAIN.SOL   
            self.MOTEUR.OBJETS.Ajouter_Ou_Pas_Un_Objet(self.x, self.y)
    

             
    def Afficher_Mur_Cassable(self):
        posX = self.ecranX()
        posY = self.ecranY()
        
        if self.objet == C_TERRAIN.CASSABLE: 
            if not self.casser:
                VAR.fenetre.blit(VAR.image["cassable"], (posX, posY))    
            else:
                VAR.fenetre.blit(VAR.image["cassable"+str(self.animationId)], (posX, posY)) 
                self.Animation_Explosion_Mur() 
                
        elif self.objet == C_TERRAIN.BLOC:
            VAR.fenetre.blit(VAR.image["mur"], (posX, posY))
            
               
        elif not self.objet == C_TERRAIN.MUR: 
            if (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-1].objet == C_TERRAIN.CASSABLE):
                VAR.fenetre.blit(VAR.image["ombre"], (posX, posY))         
    
    def Dessiner_Sol(self, _fenetre = None):
        posX = (self.x * VAR.tailleCellule) + CT.C_CONTOUR
        posY = (self.y * VAR.tailleCellule) + CT.C_CONTOUR
        i = int((posY * VAR.nbLignes) + posX)    
       
        if not self.objet == C_TERRAIN.MUR: 
            if (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-1].objet == C_TERRAIN.MUR):
                _fenetre.blit(VAR.image["ombre"], (posX, posY))
            else:
                _fenetre.blit(VAR.image["sol"+str(i % 2)], (posX, posY))
                
    def Dessiner_Mur_Fixe(self, _fenetre = None):        
        if self.objet == C_TERRAIN.MUR: 
            posX = (self.x * VAR.tailleCellule) + CT.C_CONTOUR 
            posY = (self.y * VAR.tailleCellule) + CT.C_CONTOUR
            _fenetre.blit(VAR.image["mur"], (posX, posY))
                      

                