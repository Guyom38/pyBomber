import pygame
from pygame.locals import *

from Classes.moteur import *

import variables as VAR
import fonctions as FCT
from random import *

import time

class Joueur():
    
    def __init__(self, _moteur, _id, _pseudo):
         
        self.MOTEUR = _moteur      
        self.id = _id
        self.pseudo = _pseudo
          
        self.Initialiser()
       
    def Initialiser(self):
        
        self.x, self.y = 1, 1
        self.Libere_Zone()
        
        self.direction = "BAS"
        self.enMouvement = False     
        self.vitesse = 0.05
        self.mort = False
        
        self.ancienAjustement = -1
        
    def direction_y_image(self):
        if self.direction == "BAS": return 0
        if self.direction == "HAUT": return 2
        if self.direction == "DROITE": return 3
        if self.direction == "GAUCHE": return 1
        
    def Libere_Zone(self):
        for y in range(-1, 2):
            for x in range(-1, 2):          
                xPos = int(self.x) + x
                yPos = int(self.y) + y  
                if self.MOTEUR.TERRAIN.GRILLE[xPos][yPos] > 1:
                    self.MOTEUR.TERRAIN.GRILLE[xPos][yPos] = 0  
    
    def Afficher(self):
        if self.mort == False:
            self.Gestion_Deplacement()
            
            taille = VAR.tailleCellule
            posX = VAR.offSet[0] + (self.x * taille) 
            posY = VAR.offSet[1] + (self.y * taille) - 20

            t = (time.time()*10) % 3

            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3) +t, self.direction_y_image(), 32, 40), (posX, posY))
            self.Detection_Collision_Decors()
    
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return
        
        oldX = self.x
        oldY = self.y
        
        if self.direction == "HAUT":
            self.y -= self.vitesse
        elif self.direction == "BAS":
            self.y += self.vitesse
        elif self.direction == "GAUCHE":
            self.x -= self.vitesse
        elif self.direction == "DROITE":
            self.x += self.vitesse
        
        collision = self.Detection_Collision_Decors()
        if collision:
            self.enMouvement = False            
            if not int(self.x) == int(oldX) : 
                self.x = int(oldX)
                return
            if not int(self.y) == int(oldY) : 
                self.y = int(oldY)
                return       
        
            self.x = oldX
            self.y = oldY            
        

    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY] == VAR.C_SOL)
    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        if pX == -1 and pY == -1: 
            objet1 = ((self.x * 40), (self.y * 40), 24, 24)
        else:
            objet1 = ((pX * 40), (pY * 40), 24, 24)
        
        pygame.draw.rect(VAR.fenetre, (0,255,0), objet1)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3), self.direction_y_image(), 32, 40), (objet1[0], objet1[1]-20))
        
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            x, y = coord                
            gX = int(self.x + x)
            gY = int(self.y + y)
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    
                    objet2 = (gX * 40, gY * 40, 40,40)                
                    pygame.draw.rect(VAR.fenetre, (255,0,0), objet2)
                    
                    if FCT.Collision(objet1, objet2):                     
                        return True
            else:
                return True
            
        return False
