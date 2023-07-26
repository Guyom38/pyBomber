import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

from Classes.moteur import *
from Classes.bombe import *

from random import *

import time
import pygame.mixer

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
        
        self.vitesseBase = 0.10
        self.vitesse = self.vitesseBase
        self.pasVitesse = 0.02
        
        self.puissance = 2
        self.bombes = 1
        
        self.mort = False
        self.MOTEUR.TERRAIN.Libere_Zone(self.x, self.y, 2)    
        
        
         
        
    def direction_y_image(self):
        if self.direction == "BAS": return 1
        if self.direction == "HAUT": return 3
        if self.direction == "DROITE": return 4
        if self.direction == "GAUCHE": return 2      
        
        
          
    
    
    def Afficher(self):
        if self.mort == False:              
            posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
            posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule)             
           
            if (self.enMouvement):
                animationId = int((time.time()*10) % 3)
            else:
                animationId = 0
                
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["joueur0"], (self.id * 3) + animationId, self.direction_y_image(), 16, 32), (posX, posY-12))
            self.Gestion_Deplacement()  
            self.Detection_Collision_Decors()    
            
            
            

    def Poser_Une_Bombe(self):
        posX = int(self.x + self.xD)
        posY = int(self.y + self.yD)                        
        self.MOTEUR.BOMBES.Ajouter(posX, posY, self.puissance)
        
        FCT.jouer_sons("poser_bombe")
        
        
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return
        
        # --- Mémorisation des coordonnées avant modification
        old = self.x, self.y, self.xD, self.yD        
        
        # --- mouvement en fonction de la direction
        if self.direction == "HAUT":   self.yD -= self.vitesse
        if self.direction == "BAS":    self.yD += self.vitesse
        if self.direction == "GAUCHE": self.xD -= self.vitesse
        if self.direction == "DROITE": self.xD += self.vitesse

        if (self.yD < 0.0):
            self.yD = 1.0 #- self.vitesse
            self.y -=1
        elif (self.yD > 1.0):
            self.yD = 0.0 #+ self.vitesse
            self.y +=1
        
        if (self.xD < 0.0):
            self.xD = 1.0 #- self.vitesse
            self.x -=1
        elif (self.xD > 1.0):
            self.xD = 0.0 #+ self.vitesse
            self.x +=1

        # --- controle si collision
        coord_collision = self.Detection_Collision_Decors()
        if not coord_collision == VAR.C_AUCUNE_COLLISION:
            # --- retablissement position initiale car collision
            self.x, self.y, self.xD, self.yD = old
            
            if not coord_collision == VAR.C_HORS_TERRAIN:  
                self.Algorithme_Drift(coord_collision)  
             
        self.Detection_Collision_Objets()            
        self.enMouvement = False     
        
        
        
        
        
        
    




        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    
    
    
    
    
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY].Traversable())
    
    
    def Detection_Collision_Objets(self):
        joueur = (((self.x + self.xD) * VAR.tailleCellule), ((self.y + self.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        objet_attrape = self.MOTEUR.OBJETS.Detection_Collision_Avec_Objets(joueur)
        if not (objet_attrape == None):
            if (objet_attrape.objet == VAR.C_OBJ_BOMBE): self.bombes += 1
            if (objet_attrape.objet == VAR.C_OBJ_FLAMME): self.puissance += 1
           # if (objet_attrape.objet == VAR.C_OBJ_COUP): self.bombes += 1
            if (objet_attrape.objet == VAR.C_OBJ_ROLLER): self.vitesse += self.pasVitesse
            self.MOTEUR.OBJETS.Detruire_Objet(objet_attrape)
            FCT.jouer_sons("prendre_objet")
    
    def Detection_Collision_Bombes(self):
        joueur = (((self.x + self.xD) * VAR.tailleCellule), ((self.y + self.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        return self.MOTEUR.BOMBES.Detection_Collision_Avec_Bombes(joueur)
        
                    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        if pX == -1 and pY == -1: 
            joueur = (((self.x + self.xD) * VAR.tailleCellule), ((self.y + self.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        else:
            joueur = ((pX * VAR.tailleCellule), (pY * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        
        collision = VAR.C_AUCUNE_COLLISION
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            x, y = coord                
            gX, gY = int(self.x + x), int(self.y + y)
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    
                    pygame.draw.rect(VAR.fenetre, (128,255,0,0), ((x+2) * VAR.tailleCellule, (y+2) * VAR.tailleCellule, VAR.tailleCellule-1, VAR.tailleCellule-1))
                    decors = (gX * VAR.tailleCellule, gY * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)                
                    
                    if FCT.Collision(joueur, decors):    
                        return (gX, gY)
                    
                    #if coord == (0,0) and self.Detection_Collision_Bombes():
                    #    return (gX, gY)
            else:
                pygame.draw.rect(VAR.fenetre, (64,255,255,0), ((x+2) * VAR.tailleCellule, (y+2) * VAR.tailleCellule, VAR.tailleCellule-1, VAR.tailleCellule-1))
                collision = VAR.C_HORS_TERRAIN
                break
        
        pygame.draw.rect(VAR.fenetre, (128,0,255,0), (int((2+self.xD)*VAR.tailleCellule), int((2+self.yD)*VAR.tailleCellule), VAR.tailleCellule-1, VAR.tailleCellule-1))  
        print(round(self.xD,2), round(self.yD,2))
        return collision



    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        x, y = self.x + self.xD, self.y + self.yD
        xCollision, yCollision = _collision_coord
        limit = 1
        
        # --- Test le Passage a empreinter pour contourner
        if d == "DROITE": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        if d == "GAUCHE": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision-1].Traversable())      
        if d == "HAUT": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision+1].Traversable())      
        if d == "BAS": bloc1 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        
        # --- Test le passage final
        if d == "DROITE" or d == "GAUCHE":           
            # --- Passage au dessus
            if y > (yCollision-limit) and y < (yCollision): 
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision-1].Traversable())
                if bloc1 and bloc2:
                    self.yD -= self.vitesseBase
            # --- Passage au dessous
            elif y > (yCollision ) and y < (yCollision + limit):
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision+1].Traversable())
                if bloc1 and bloc2:
                    self.yD += self.vitesseBase

        if d == "HAUT" or d == "BAS":           
            # --- Passage au dessus
            if x > (xCollision-limit) and x < (xCollision): 
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision].Traversable())
                if bloc1 and bloc2:
                    self.xD -= self.vitesseBase
            # --- Passage au dessous
            elif x > (xCollision ) and x < (xCollision + limit):
                bloc2 = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision].Traversable())
                if bloc1 and bloc2:
                    self.xD += self.vitesseBase