import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

class CInterface:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        
        FCT.Init_Texte(50)
    
    def Afficher(self):
        if VAR.phase_jeu == "TITRE":
            self.Afficher_Cadre()
            FCT.Texte("PyBomber", (255,255,255), 50, 100, 100)
    
    def Afficher_Fond(self):        
        self.Afficher_Cadre()
        
 
           
    def Afficher_Cadre(self, _largeur = -1, _hauteur = -1):
        if _largeur == -1 and _hauteur == -1:
            _largeur, _hauteur = int(VAR.resolution[0] / VAR.tailleCellule), int(VAR.resolution[1] / VAR.tailleCellule) 
            
        image_contour = VAR.image["mur"]
        image_fond = VAR.image["sol0"]
        
        offSet = ( (VAR.resolution[0] - (_largeur* VAR.tailleCellule)) /2, (VAR.resolution[1] - (_hauteur* VAR.tailleCellule)) /2 )  
         
        for y in range(_hauteur):
            for x in range(_largeur):
                posX = offSet[0] + (x * VAR.tailleCellule)
                posY = offSet[1] + (y * VAR.tailleCellule)
                
                if x == 0 or y == 0 or x == _largeur-1 or y == _hauteur-1:
                    VAR.fenetre.blit(image_contour, (posX, posY))
                else:
                    VAR.fenetre.blit(image_fond, (posX, posY))