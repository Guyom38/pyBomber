import pygame
from pygame.locals import *

from Classes.terrrain import *
import variables as VAR
import fonctions as FCT

class CMoteur():
    def __init__(self):
        pygame.init()   
    
    def Initialisation(self):
        self.TERRAIN = CTerrain(self)        
        self.Chargement_Graphismes()
        
        VAR.offSet = ( (VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2,
                        (VAR.resolution[1] - (VAR.nbLignes* VAR.tailleCellule)) /2 )
        
    
    def Chargement_Graphismes(self):
        tmp = pygame.image.load("images/decors2.png").convert_alpha()   
        VAR.image["cassable"] = FCT.image_decoupe(tmp, 0, 0, 40, 40 )
        VAR.image["sol0"] = FCT.image_decoupe(tmp, 0, 1, 40, 40 )
        VAR.image["sol1"] = FCT.image_decoupe(tmp, 1, 1, 40, 40 )
        VAR.image["mur"] = FCT.image_decoupe(tmp, 0, 2, 40, 40 )

         
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
                # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    VAR.boucle_jeu = False

                # --- si l'utilisateur presse l'une des fleches de direction
                if event.type == KEYDOWN:  
                    if event.key == K_LEFT: print("la touche gauche")
                    if event.key == K_RIGHT: print("la touche droite")
                    if event.key == K_UP: print("la touche haut")
                    if event.key == K_DOWN: print("la touche bas")

            # --- remplissage de la fenetre avec une couleur proche du noir
            VAR.fenetre.fill((16,16,16))
            self.TERRAIN.Afficher()
            

            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(25)

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 