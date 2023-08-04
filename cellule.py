import pygame
from pygame.locals import *

import variables as VAR
import time, random
import item
class CCellule(item.CItem):
    def __init__(self, _moteur, _x, _y):
        super().__init__(_moteur, _x,_y, "")      
           
        self.objet = VAR.C_SOL   
        self.casser = False
        
        
    def Traversable(self):
        return (self.objet == VAR.C_SOL)
    
    def Cassable(self):
        return (self.objet == VAR.C_CASSABLE)
    
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
            self.objet = VAR.C_SOL    
            self.MOTEUR.OBJETS.Ajouter_Ou_Pas_Un_Objet(self.x, self.y)
    

             
    def Afficher_Mur_Cassable(self):
        posX = VAR.offSet[0] + (self.x * VAR.tailleCellule)
        posY = VAR.offSet[1] + (self.y * VAR.tailleCellule)
        
        if self.objet == VAR.C_CASSABLE: 
            if not self.casser:
                VAR.fenetre.blit(VAR.image["cassable"], (posX, posY))    
            else:
                VAR.fenetre.blit(VAR.image["cassable"+str(self.animationId)], (posX, posY)) 
                self.Animation_Explosion_Mur() 
                
        elif self.objet == VAR.C_BLOC:
            #pygame.draw.rect(VAR.fenetre, (random.randint(0, 255),255,255), (posX, posY, VAR.tailleCellule, VAR.tailleCellule), 0)
            VAR.fenetre.blit(VAR.image["mur"], (posX, posY))
            
               
        elif not self.objet == VAR.C_MUR: 
            if (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-1].objet == VAR.C_CASSABLE):
                VAR.fenetre.blit(VAR.image["ombre"], (posX, posY))         
    
    def Dessiner_Sol(self, _fenetre = None):
        posX = (self.x * VAR.tailleCellule) + self.TERRAIN.contour
        posY = (self.y * VAR.tailleCellule) + self.TERRAIN.contour
        i = int((posY * VAR.nbLignes) + posX)    
       
        if not self.objet == VAR.C_MUR: 
            if (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-1].objet == VAR.C_MUR):
                _fenetre.blit(VAR.image["ombre"], (posX, posY))
            else:
                _fenetre.blit(VAR.image["sol"+str(i % 2)], (posX, posY))
                
    def Dessiner_Mur_Fixe(self, _fenetre = None):        
        if self.objet == VAR.C_MUR: 
            posX = (self.x * VAR.tailleCellule) + self.TERRAIN.contour 
            posY = (self.y * VAR.tailleCellule) + self.TERRAIN.contour
            _fenetre.blit(VAR.image["mur"], (posX, posY))
                      

                