import pygame
from pygame.locals import *

from Classes.terrrain import *
from Classes.joueur import *

import variables as VAR
import fonctions as FCT

class CMoteur():
    def __init__(self):
        pygame.init()   
    
    def Initialisation(self):
        self.TERRAIN = CTerrain(self)      
        self.JOUEURS = []
        self.JOUEURS.append(Joueur(self, 0, "Guyom"))
          
        self.Chargement_Graphismes()
        
        VAR.offSet = ( (VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2,
                        (VAR.resolution[1] - (VAR.nbLignes* VAR.tailleCellule)) /2 )
        
    
    def Chargement_Graphismes(self):
        # --- Decors
        tmp = pygame.image.load("images/decors2.png").convert_alpha()   
        VAR.image["cassable"] = FCT.image_decoupe(tmp, 0, 0, 40, 40 )
        VAR.image["sol0"] = FCT.image_decoupe(tmp, 0, 1, 40, 40 )
        VAR.image["sol1"] = FCT.image_decoupe(tmp, 1, 1, 40, 40 )
        VAR.image["mur"] = FCT.image_decoupe(tmp, 0, 2, 40, 40 )
        
        # --- Joueurs
        VAR.image["joueur0"] = pygame.image.load("images/sprite0.png").convert_alpha()     
         
    def Demarrer(self):
        VAR.fenetre = pygame.display.set_mode(VAR.resolution, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBomber 0.1")        
        self.horloge = pygame.time.Clock()
        
        self.Initialisation()
        self.Boucle()
    
    def Boucle(self):
        VAR.boucle_jeu = True
        while VAR.boucle_jeu:
            # --- récupére l'ensemble des évènements
            for event in pygame.event.get():        
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: VAR.boucle_jeu = False        
                if event.type == KEYDOWN:  
                    if event.key == K_LEFT: 
                        self.JOUEURS[0].direction = "GAUCHE"
                        self.JOUEURS[0].enMouvement = True
                    if event.key == K_RIGHT: 
                        self.JOUEURS[0].direction = "DROITE"
                        self.JOUEURS[0].enMouvement = True
                    if event.key == K_UP: 
                        self.JOUEURS[0].direction = "HAUT"
                        self.JOUEURS[0].enMouvement = True
                    if event.key == K_DOWN: 
                        self.JOUEURS[0].direction = "BAS"
                        self.JOUEURS[0].enMouvement = True

            # --- remplissage de la fenetre avec une couleur proche du noir
            VAR.fenetre.fill((16,16,16))
            self.TERRAIN.Afficher()
            self.JOUEURS[0].Afficher()            

            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(25)           
               

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 