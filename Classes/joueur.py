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
        self.MOTEUR.TERRAIN.Libere_Zone(self.x, self.y, 2)
        
        self.direction = "BAS"
        self.enMouvement = False     
        self.vitesse = 0.05
        self.mort = False
        
    def direction_y_image(self):
        if self.direction == "BAS": return 0
        if self.direction == "HAUT": return 2
        if self.direction == "DROITE": return 3
        if self.direction == "GAUCHE": return 1
        
    
    
    def Afficher(self):
        if self.mort == False:
            self.Gestion_Deplacement()            

            posX = VAR.offSet[0] + (self.x * VAR.tailleCellule) 
            posY = VAR.offSet[1] + (self.y * VAR.tailleCellule) - 20
            
            animationId = 0
            if self.enMouvement: animationId = (time.time()*10) % 3
            
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3) + animationId, self.direction_y_image(), 32, 40), (posX+4, posY+4))
            self.Detection_Collision_Decors()
           
            ecriture = pygame.font.SysFont('arial', 20) 
            image_texte = ecriture.render("x=" + str(round(self.x,2)) + "; y=" + str(round(self.y,2)) + "; direction = "+str(self.direction), True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, ((self.x + 2)*40, self.y * 40))
            image_texte = ecriture.render("x=" + str(round(self.x,0)) + "; y=" + str(round(self.y,0)) + "; direction = "+str(self.direction), True, (255,0,0)) 
            VAR.fenetre.blit(image_texte, ((self.x + 2)*40, (self.y * 40)+15))

            
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return
        
        # --- Mémorisation des coordonnées avant modification
        oldX = self.x
        oldY = self.y
        
        # --- mouvement en fonction de la direction
        if self.direction == "HAUT":
            self.y -= self.vitesse
        elif self.direction == "BAS":
            self.y += self.vitesse
        elif self.direction == "GAUCHE":
            self.x -= self.vitesse
        elif self.direction == "DROITE":
            self.x += self.vitesse
        
        # --- controle si collision
        collision = self.Detection_Collision_Decors()
        if not collision == VAR.C_AUCUNE_COLLISION:
            self.enMouvement = False            
            if not int(self.x) == int(oldX) : 
                self.x = round(oldX, 0)
                return
            if not int(self.y) == int(oldY) : 
                self.y = round(oldY, 0)
                return       

            # --- retablissement position initiale car collision
            self.x = oldX
            self.y = oldY  
            
        if not collision == VAR.C_AUCUNE_COLLISION:
            

            self.Algorithme_Drift(collision)          
        
    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        x, y = self.x, self.y
        
        xCollision, yCollision = _collision_coord
        print("Y:"+ str(round(y,2))+" >" + str(yCollision-1) + " // " + "Y:"+ str(round(y,2)) + " < " + str(yCollision))
            
    
        if d == "DROITE":           
            # --- Passage au dessus
            if y > (yCollision-1) and y < (yCollision): 
                if self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision-1] == VAR.C_SOL:
                    self.y -= self.vitesse
                    self.enMouvement = True
            # --- Passage au dessous
            elif y > (yCollision + 0.35) and y < (yCollision + 1):
                if self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision+1] == VAR.C_SOL:
                    self.y += self.vitesse
                    self.enMouvement = True
        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY] == VAR.C_SOL)
    
    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        if pX == -1 and pY == -1: 
            objet1 = ((self.x * 40), (self.y * 40), 38, 38)
        else:
            objet1 = ((pX * 40), (pY * 40), 38, 38)
        
        pygame.draw.rect(VAR.fenetre, (0,255,0), objet1)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3), self.direction_y_image(), 32, 40), (objet1[0]+4, objet1[1]+4))
        
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
            
        return VAR.C_AUCUNE_COLLISION
