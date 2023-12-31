import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT
import random

import cellule as CC
import time

from enums import *

C_CONTOUR = 16  
         
class CTerrain():  
       
    def __init__(self, _moteur):
        self.MOTEUR = _moteur        
        
        self.contour_fond = (0, 0, 0)
        self.contour_bordure = (255,255,255)
    
    def Reconfigurer_Terrain():
        VAR.nbColonnes = int(((VAR.resolution[0] - (C_CONTOUR * 2)) / VAR.tailleCellule) )-5 
        if VAR.nbColonnes % 2 == 0: VAR.nbColonnes +=1        
        VAR.nbLignes = int(((VAR.resolution[1] - VAR.hauteur_cadre_joueurs - (C_CONTOUR * 2) ) / VAR.tailleCellule) )    
        if VAR.nbLignes % 2 == 0: VAR.nbLignes -=1       
        
        print("Dimension Terrain : ", VAR.nbColonnes, VAR.nbLignes)
        VAR.offSet = ( ((VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2) ,
                        VAR.hauteur_cadre_joueurs + (((VAR.resolution[1] - VAR.hauteur_cadre_joueurs) - (VAR.nbLignes* VAR.tailleCellule)) /2) ) 
        
    def Initialiser(self, _menu = False):
        self.GRILLE =  [[CC.CCellule(self.MOTEUR, x, y) for y in range(VAR.nbLignes)] for x in range(VAR.nbColonnes)]
        self.Construire_Terrain_De_Jeu(_menu)
        self.image = None
        
        self.x, self.y, self.xD, self.yD = 0, 1, 1, 1
        self.direction = C_DIRECTION.DROITE
        self.temps_ecrasement = time.time()
        self.delais_ecrasement = 0.1
        self.tour = 0
        self.timeOut = False
    
     
        
    def Preparation_Couches_Fixes(self):
        largeur = (VAR.nbColonnes * VAR.tailleCellule) + (C_CONTOUR * 2)
        hauteur = (VAR.nbLignes * VAR.tailleCellule) + (C_CONTOUR * 2)
        
        self.image = pygame.Surface((largeur, hauteur),pygame.SRCALPHA,32)
        pygame.draw.rect(self.image, self.contour_fond , (0, 0, largeur, hauteur), 0)        
        pygame.draw.rect(self.image, self.contour_bordure , (0, 0, largeur, hauteur), 4)        
       
        # --- affiche première couche, le sol !
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes): 
                self.GRILLE[x][y].Dessiner_Sol(self.image)
                self.GRILLE[x][y].Dessiner_Mur_Fixe(self.image)
        

    def Afficher(self):
        #temps_ref = time.time()
        if self.image == None :
            self.Preparation_Couches_Fixes()       
        VAR.fenetre.blit(self.image, (VAR.offSet[0] - C_CONTOUR, VAR.offSet[1] - C_CONTOUR))
        
        # --- affiche couches suivantes, murs ...      
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):
                self.GRILLE[x][y].Afficher_Mur_Cassable()
        
        #print(round(time.time() - temps_ref, 3))     
                              
    def Construire_Terrain_De_Jeu(self, _menu = False):        
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):
                mur = C_TERRAIN.SOL
                
                if not _menu:
                    if (random.randint(0, 100) < VAR.tauxRemplissage) : mur = C_TERRAIN.CASSABLE
                    if x % 2 == 0 and y % 2 == 0: mur = C_TERRAIN.MUR  
                    
                if x in (0, VAR.nbColonnes-1): mur = C_TERRAIN.MUR
                if y in (0, VAR.nbLignes-1): mur = C_TERRAIN.MUR
                          
                
                self.GRILLE[x][y].objet = mur
                       
                       
    def Libere_Zone(self, _x, _y, _nb):
        for y in range(-_nb, _nb+1):
            for x in range(-_nb, _nb+1):    
                xPos = _x + x
                yPos = _y + y 
                if (0 <= xPos < VAR.nbColonnes) and (0 <= yPos < VAR.nbLignes):
                    if self.GRILLE[xPos][yPos].objet == C_TERRAIN.CASSABLE:
                        self.GRILLE[xPos][yPos].objet = C_TERRAIN.SOL
                        
    
    def TimeOut_Resserage_Du_Terrain(self):
        if self.timeOut or VAR.pause: return
        
        if self.MOTEUR.tempsRestant() == 0:
            if (time.time() - self.temps_ecrasement > self.delais_ecrasement):
                self.temps_ecrasement = time.time()
                        
                if self.direction == C_DIRECTION.DROITE:
                    if self.x < VAR.nbColonnes - self.xD - 1: 
                        self.x+=1
                    else:
                        self.direction = C_DIRECTION.BAS
                        self.y = self.yD + 1
                        self.xD += 1
                                
                elif self.direction == C_DIRECTION.BAS:
                    if self.y < VAR.nbLignes - self.yD - 1:
                        self.y+=1
                    else:
                        self.direction = C_DIRECTION.GAUCHE
                        self.x=VAR.nbColonnes - self.xD - 1
                        self.yD +=1
                                
                elif self.direction == C_DIRECTION.GAUCHE:
                    if self.x >= self.xD :
                        self.x -= 1
                    else:
                        self.direction = C_DIRECTION.HAUT
                        self.y = VAR.nbLignes - self.yD -1
                                
                        
                elif self.direction == C_DIRECTION.HAUT:
                    if self.y > self.yD -1:
                        self.y -=1
                    else:
                        self.direction = C_DIRECTION.DROITE
                        self.x = self.xD 
                        self.y +=1
                        self.tour += 1
                                
                                
                
                max_lignes = int((VAR.nbLignes - 6) / 2)
                if self.tour == max_lignes:
                    self.timeOut = True
                else:
                    self.GRILLE[self.x][self.y].objet = C_TERRAIN.BLOC
                    FCT.jouer_sons("bloc_timeout")
                    
                    for joueur in self.MOTEUR.JOUEURS.LISTE:
                        coord_joueur = (joueur.x * VAR.tailleCellule, joueur.y * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)
                        coord_terrain = (self.x * VAR.tailleCellule, self.y * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)
   
                        
                        if FCT.Collision(coord_joueur, coord_terrain) and not joueur.mort:
                            joueur.Mourir()

                    
                          
    