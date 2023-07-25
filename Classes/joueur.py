import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

from Classes.moteur import *
from Classes.bombe import *

from random import *

import time

class CJoueur():
    
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
        self.vitesse = 0.20
        
        self.puissance = 5
        self.bombes = 2
        
        self.mort = False
        self.MOTEUR.TERRAIN.Libere_Zone(self.x, self.y, 2)    
        
        
         
        
    def direction_y_image(self):
        if self.direction == "BAS": return 1
        if self.direction == "HAUT": return 3
        if self.direction == "DROITE": return 4
        if self.direction == "GAUCHE": return 2      
        
        
          
    
    
    def Afficher(self):
        if self.mort == False:
            self.Gestion_Deplacement()            

            posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
            posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule)             
           
            animationId = int((time.time()*10) % 3)
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3) + animationId, self.direction_y_image(), 16, 32), (posX, posY-12))
            
            
            

    def Poser_Une_Bombe(self):
        posX = int(self.x + self.xD)
        posY = int(self.y + self.yD)                        
        self.MOTEUR.BOMBES.append(CBombe(self.MOTEUR, posX, posY, self.puissance))
        
        
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
        
        if (self.xD < 0.0):
            self.xD = 1.0 - self.vitesse
            self.x -=1
        elif (self.xD > 1.0):
            self.xD = 0.0 + self.vitesse
            self.x +=1

        # --- controle si collision
        coord_collision = self.Detection_Collision_Decors()
        if not coord_collision == VAR.C_AUCUNE_COLLISION:
            # --- retablissement position initiale car collision
            self.x, self.y, self.xD, self.yD = old
            
            if not coord_collision == VAR.C_HORS_TERRAIN:  
                self.Algorithme_Drift(coord_collision)  
             
        self.enMouvement = False     
        
        
        
        
        
        
    




        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    
    
    
    
    
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY].Traversable())
    
    
    
    
    def Detection_Collision_Bombes(self):
        for bombe in self.MOTEUR.BOMBES:
            objet1 = (((self.x + self.xD) * VAR.tailleCellule), ((self.y + self.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            objet2 = (((bombe.x + bombe.xD) * VAR.tailleCellule), ((bombe.y + bombe.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if FCT.Collision(objet1, objet2):    
                return True
        return False
                    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        if pX == -1 and pY == -1: 
            objet1 = (((self.x + self.xD) * VAR.tailleCellule), ((self.y + self.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        else:
            objet1 = ((pX * VAR.tailleCellule), (pY * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            x, y = coord                
            gX = int(self.x + x)
            gY = int(self.y + y)
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    
                    objet2 = (gX * VAR.tailleCellule, gY * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)                
                    
                    if FCT.Collision(objet1, objet2):    
                        return (gX, gY)
                    
                    #if coord == (0,0) and self.Detection_Collision_Bombes():
                    #    return (gX, gY)
            else:
                return VAR.C_HORS_TERRAIN
            
        return VAR.C_AUCUNE_COLLISION



    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        x, y = self.x + self.xD, self.y + self.yD
        xCollision, yCollision = _collision_coord

        # --- Test le Passage a empreinter pour contourner
        if d == "DROITE": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        if d == "GAUCHE": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision-1].Traversable())      
        if d == "HAUT": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision+1].Traversable())      
        if d == "BAS": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        
        # --- Test le passage final
        if d == "DROITE" or d == "GAUCHE":           
            # --- Passage au dessus
            if y > (yCollision-1) and y < (yCollision): 
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision-1].Traversable())
                if bloc1 and bloc2:
                    self.yD -= self.vitesse
            # --- Passage au dessous
            elif y > (yCollision ) and y < (yCollision + 1):
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision+1].Traversable())
                if bloc1 and bloc2:
                    self.yD += self.vitesse

        if d == "HAUT" or d == "BAS":           
            # --- Passage au dessus
            if x > (xCollision-1) and x < (xCollision): 
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision].Traversable())
                if bloc1 and bloc2:
                    self.xD -= self.vitesse
            # --- Passage au dessous
            elif x > (xCollision ) and x < (xCollision + 1):
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision].Traversable())
                if bloc1 and bloc2:
                    self.xD += self.vitesse