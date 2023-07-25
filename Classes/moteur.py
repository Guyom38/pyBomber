import pygame
from pygame.locals import *

from Classes.terrrain import *
from Classes.joueur import *
from Classes.bombe import *

import variables as VAR
import fonctions as FCT

class CMoteur():
    def __init__(self):
        pygame.init()   
    
    
    
    
    def Initialisation(self):
        self.TERRAIN = CTerrain(self)      
        self.JOUEURS = []
        self.JOUEURS.append(CJoueur(self, 0, "Guyom"))
        self.BOMBES = []
        
        self.Chargement_Graphismes()
        
        VAR.offSet = ( (VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2,
                        (VAR.resolution[1] - (VAR.nbLignes* VAR.tailleCellule)) /2 )
        
        
        
    
    def Chargement_Graphismes(self):
        # --- Decors
        tmp = pygame.image.load("images/decors.png").convert_alpha()   
        VAR.image["cassable"] = FCT.image_decoupe(tmp, 0, 0, 16, 16 )
        VAR.image["cassable0"] = FCT.image_decoupe(tmp, 1, 0, 16, 16 )
        VAR.image["cassable1"] = FCT.image_decoupe(tmp, 2, 0, 16, 16 )
        VAR.image["cassable2"] = FCT.image_decoupe(tmp, 2, 1, 16, 16 )
        VAR.image["sol0"] = FCT.image_decoupe(tmp, 0, 2, 16, 16 )
        VAR.image["sol1"] = FCT.image_decoupe(tmp, 0, 2, 16, 16 )
        VAR.image["ombre"] = FCT.image_decoupe(tmp, 1, 2, 16, 16 )
        VAR.image["mur"] = FCT.image_decoupe(tmp, 0, 1, 16, 16 )

        # --- Joueurs
        VAR.image["joueur0"] = pygame.image.load("images/sprite1.png").convert_alpha() 
        VAR.image["objets"] = pygame.image.load("images/objets.png").convert_alpha() 
         
        
        VAR.image["bombe"] = FCT.image_decoupe(VAR.image["objets"], 0, 0, 16, 16 )
        VAR.image["coup"] = FCT.image_decoupe(VAR.image["objets"], 1, 0, 16, 16 )
        VAR.image["roller"] = FCT.image_decoupe(VAR.image["objets"], 2, 0, 16, 16 )
        VAR.image["flamme"] = FCT.image_decoupe(VAR.image["objets"], 3, 0, 16, 16 )
         
         
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
                    if event.key == K_SPACE: 
                        self.JOUEURS[0].Poser_Une_Bombe()
                    
            keys = pygame.key.get_pressed()
                    
            if keys[K_LEFT] == 1:
                self.JOUEURS[0].direction = "GAUCHE"
                self.JOUEURS[0].enMouvement = True
            if keys[K_RIGHT] == 1:
                self.JOUEURS[0].direction = "DROITE"
                self.JOUEURS[0].enMouvement = True
            if keys[K_UP] == 1:
                self.JOUEURS[0].direction = "HAUT"
                self.JOUEURS[0].enMouvement = True
            if keys[K_DOWN] == 1:
                self.JOUEURS[0].direction = "BAS"
                self.JOUEURS[0].enMouvement = True

            # --- remplissage de la fenetre avec une couleur proche du noir
            VAR.fenetre.fill((16,16,16))
            self.TERRAIN.Afficher()
            for bombe in self.BOMBES:
                bombe.Afficher()     
                
            self.JOUEURS[0].Afficher() 
            
            

            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(30)           
               

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 