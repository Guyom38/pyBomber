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
        self.direction = "BAS"
        self.enMouvement = False
        self.xD, self.yD = 0.0, 0.0  
        self.vitesse = 0.10
        
        self.mort = False
        self.MOTEUR.TERRAIN.Libere_Zone(self.x, self.y, 2)     
        
    def direction_y_image(self):
        if self.direction == "BAS": return 0
        if self.direction == "HAUT": return 2
        if self.direction == "DROITE": return 3
        if self.direction == "GAUCHE": return 1        
    
    
    def Afficher(self):
        if self.mort == False:
            self.Gestion_Deplacement()            

            posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
            posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule) - 20
            
           
            animationId = (time.time()*10) % 3
            
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3) + animationId, self.direction_y_image(), 32, 40), (posX+4, posY+4))
            self.Detection_Collision_Decors()

            
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return
        
        # --- Mémorisation des coordonnées avant modification
        old = self.x, self.y, self.xD, self.yD
        
        
        # --- mouvement en fonction de la direction
        if self.direction == "HAUT":
            self.yD -= self.vitesse
        elif self.direction == "BAS":
            self.yD += self.vitesse
        elif self.direction == "GAUCHE":
            self.xD -= self.vitesse
        elif self.direction == "DROITE":
            self.xD += self.vitesse
        
        if (self.yD < 0.0):
            self.yD = 1.0 - self.vitesse
            self.y -=1
        elif (self.yD > 1.0):
            self.yD = 0.0 + self.vitesse
            self.y +=1
        elif (self.xD < 1.0):
            self.xD = 1.0 - self.vitesse
            self.x -=1
        elif (self.xD > 1.0):
            self.xD = 0.0 + self.vitesse
            self.x +=1
            
        # --- controle si collision
        coord_collision = self.Detection_Collision_Decors()
        collision = not coord_collision == VAR.C_AUCUNE_COLLISION
        if collision:
            # --- retablissement position initiale car collision
            self.x, self.y, self.xD, self.yD = old
            
        if collision:  
            self.Algorithme_Drift(coord_collision)   
              
        
            
        
            
        self.enMouvement = False     
        
    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        x, y = self.x + self.xD, self.y + self.yD

        xCollision, yCollision = _collision_coord
        print("Y:"+ str(round(y,2))+" >" + str(yCollision-1) + " // " + "Y:"+ str(round(y,2)) + " < " + str(yCollision))
            
    
        if d == "DROITE":           
            # --- Passage au dessus
            if y > (yCollision-1) and y < (yCollision): 
                if self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision-1] == VAR.C_SOL:
                    self.yD -= self.vitesse

            # --- Passage au dessous
            elif y > (yCollision + 0.35) and y < (yCollision + 1):
                if self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision+1] == VAR.C_SOL:
                    self.yD += self.vitesse

        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY] == VAR.C_SOL)
    
    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        if pX == -1 and pY == -1: 
            objet1 = (((self.x + self.xD) * 40), ((self.y + self.yD) * 40), 40, 40)
        else:
            objet1 = ((pX * 40), (pY * 40), 40, 40)
        
        pygame.draw.rect(VAR.fenetre, (0,255,0), objet1)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3), self.direction_y_image(), 32, 40), (objet1[0]+4, objet1[1]-16))
        
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
                        return (gX, gY)
            else:
                return VAR.C_HORS_TERRAIN
            
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3), self.direction_y_image(), 32, 40), (objet1[0]+4, objet1[1]-16))
        return VAR.C_AUCUNE_COLLISION
