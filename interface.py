import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

class CInterface:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
    
    def Initialiser(self):
        VAR.image["titre"] = pygame.transform.scale(pygame.image.load("images/R.jpg"), VAR.resolution)
        
        FCT.Init_Texte(150)
    
    def Afficher(self):
        if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.TITRE:
            #self.Afficher_Cadre()
            self.Afficher_Fond()
            
            image = FCT.Image_Texte("PyBomber", (32,0,0,0), 150)
            x = (VAR.resolution[0] - image.get_width()) / 2
            VAR.fenetre.blit(image, (x, 100))
            
            image = FCT.Image_Texte("PyBomber", (255,255,255,255), 150)            
            VAR.fenetre.blit(image, (x-10, 100-10))
            
            
    
    def Afficher_Fond(self):        
        VAR.fenetre.blit(VAR.image["titre"] , (0, 0))
        
 
           
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