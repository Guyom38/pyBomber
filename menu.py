import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

import cellule as CC

import time, random

class CMenu():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        self.PARTICULES = _moteur.PARTICULES
        self.TERRAIN = _moteur.TERRAIN
        self.JOUEURS = _moteur.JOUEURS
        
        
        
                 
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        self.temps_particules = time.time()
        self.temps_delais = 0.1
        
        self.select = None
        
    def Initialiser(self):
        self.largeurZone = 600
        self.largeurBouton, self.hauteurBouton = 400, 100
        self.x, self.y = (VAR.resolution[0] - self.largeurZone) - 96, 200
        
        
        
        self.LISTE = {}
        self.menu = "PRINCIPAL"
        self.menu_sous = ""
        self.id = 0
        
        MENU1 = []
        MENU1.append(CBouton(self.MOTEUR, 0, self.x, self.y, self.largeurBouton, self.hauteurBouton, "NORMAL"))
        MENU1.append(CBouton(self.MOTEUR, 1, self.x, self.y, self.largeurBouton, self.hauteurBouton, "BATTLE MODE"))
        MENU1.append(CBouton(self.MOTEUR, 2, self.x, self.y, self.largeurBouton, self.hauteurBouton, "OPTION"))
        self.LISTE["PRINCIPAL"] = MENU1
        
        MENU2 = []
        MENU2.append(CBouton(self.MOTEUR, 0, self.x, self.y, self.largeurBouton, self.hauteurBouton, "NOMBRE PARTIES (3)"))
        MENU2.append(CBouton(self.MOTEUR, 1, self.x, self.y, self.largeurBouton, self.hauteurBouton, "DUREE PARTIE (3:30)"))
        MENU2.append(CBouton(self.MOTEUR, 2, self.x, self.y, self.largeurBouton, self.hauteurBouton, "MALADIES (ON)"))
        MENU2.append(CBouton(self.MOTEUR, 3, self.x, self.y, self.largeurBouton, self.hauteurBouton, "HERITAGE (ON)"))        
        self.LISTE["PARTIE"] = MENU2

        MENU3 = []
        MENU3.append(CBouton(self.MOTEUR, 0, self.x, self.y, self.largeurBouton, self.hauteurBouton, "RESOLUTION (1024x768)"))
        MENU3.append(CBouton(self.MOTEUR, 1, self.x, self.y, self.largeurBouton, self.hauteurBouton, "ZOOM (x2)"))
        MENU3.append(CBouton(self.MOTEUR, 2, self.x, self.y, self.largeurBouton, self.hauteurBouton, "MUSIC (ON)"))
        MENU3.append(CBouton(self.MOTEUR, 3, self.x, self.y, self.largeurBouton, self.hauteurBouton, "PARTICULE (ON)"))
        self.LISTE["OPTIONS"] = MENU3

        MENU4 = []
        MENU4.append(CBouton(self.MOTEUR, 0, self.x, self.y, self.largeurBouton, self.hauteurBouton, "ORGINAL (15x13)"))
        MENU4.append(CBouton(self.MOTEUR, 1, self.x, self.y, self.largeurBouton, self.hauteurBouton, "NORMAL"))
        MENU4.append(CBouton(self.MOTEUR, 2, self.x, self.y, self.largeurBouton, self.hauteurBouton, "LARGE"))
        MENU4.append(CBouton(self.MOTEUR, 3, self.x, self.y, self.largeurBouton, self.hauteurBouton, "AU TAQUET"))
        self.LISTE["NIVEAU"] = MENU3
        
        self.Initialiser_Cadre_Menu()
        

    def Initialiser_Cadre_Menu(self):
        # -- Terrain
        VAR.nbLignes = int((VAR.resolution[1] / VAR.tailleCellule)) - 2
        VAR.nbColonnes = int((self.largeurZone / VAR.tailleCellule)) +1
             
        self.TERRAIN.GRILLE =  [[CC.CCellule(self.MOTEUR, x, y) for y in range(VAR.nbLignes)] for x in range(VAR.nbColonnes)]
        self.TERRAIN.Construire_Terrain_De_Jeu(True)
        self.TERRAIN.image = None   
        
        VAR.offSet = (self.x, VAR.tailleCellule)
        
         
    def Afficher_Menu(self):
        #self.INTERFACE.Afficher_Fond()
        VAR.fenetre.blit(VAR.image['titre'], (0, 0))
        
        self.TERRAIN.Afficher() 
        
                
        #self.INTERFACE.Dessiner_Cadre(self.x - 32, self.y - 32, self.largeurBouton + 64, (len(self.LISTE[self.menu]) * (self.hauteurBouton+10)) + 64 - 10, (255, 137, 58, 0), self.couleur_bordure, 4)
        

        
        for bouton in self.LISTE[self.menu]:
            presse = bouton.Afficher_Bouton()
            
            if presse:
                if self.menu == "PRINCIPAL":
                    if bouton.id == 0:
                        self.menu = "PARTIE"
                    elif bouton.id == 1:
                        self.menu = "PARTIE"
                    elif bouton.id == 2:
                        self.menu = "OPTIONS"
                        
        self.JOUEURS.Afficher_Tous_Les_Joueurs()
        
        if time.time() - self.temps_particules > self.temps_delais:
            self.temps_particules = time.time()            
            for _ in range(4):
                self.PARTICULES.Ajouter_Particule(random.randint(0, VAR.resolution[0]), VAR.resolution[1], (162, 104, 254))
        self.PARTICULES.Afficher_Les_Particules()
                
    
    
    
    
class CBouton():
    def __init__(self, _moteur, _id, _x, _y, _largeur, _hauteur, _texte):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        
        self.id = _id
        self.x = _x
        self.y = _y
        self.largeur = _largeur
        self.hauteur = _hauteur
        self.activer = False
        self.texte = _texte
        
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        
    def Afficher_Bouton(self):
        x = self.x + VAR.tailleCellule
        y = self.y + (self.id * (self.hauteur+10))
        
        texte = FCT.Image_Texte(self.texte, (255,255,255,255), int(20))
        centreX = (self.largeur - texte.get_width()-40) / 2
        centreY = (self.hauteur - texte.get_height()) /2
        
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeur, self.hauteur, self.couleur_fond, self.couleur_bordure, 4)
        self.INTERFACE.Dessiner_Cadre(x, y, 40, self.hauteur, (128,128,128), self.couleur_bordure, 4)
        VAR.fenetre.blit(texte, (x + centreX + 40, y + centreY))
        
        return False
    
