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
        VAR.nbColonnes = int((self.largeurZone / VAR.tailleCellule)) +1
        VAR.nbLignes = int((VAR.resolution[1] / VAR.tailleCellule)) - 2        
        
        
        
        self.LISTE = {}
        self.menu = "PRINCIPAL"
        self.menu_sous = ""
        self.id = 0
        
        MENU1 = []
        MENU1.append(CBouton(self.MOTEUR, 0, "NORMAL"))
        MENU1.append(CBouton(self.MOTEUR, 1, "BATTLE MODE"))
        MENU1.append(CBouton(self.MOTEUR, 2, "OPTION"))
        MENU1.append(CBouton(self.MOTEUR, 3, ""))
        MENU1.append(CBouton(self.MOTEUR, 4, "QUITTER"))
        self.LISTE["PRINCIPAL"] = MENU1
        
        MENU2 = []
        MENU2.append(CBouton(self.MOTEUR, 0,  "NOMBRE PARTIES (3)"))
        MENU2.append(CBouton(self.MOTEUR, 1,  "DUREE PARTIE (3:30)"))
        MENU2.append(CBouton(self.MOTEUR, 2,  "MALADIES (ON)"))
        MENU2.append(CBouton(self.MOTEUR, 3,  "HERITAGE (ON)"))        
        self.LISTE["PARTIE"] = MENU2

        MENU3 = []
        MENU3.append(CBouton(self.MOTEUR, 0,  "RESOLUTION (1024x768)"))
        MENU3.append(CBouton(self.MOTEUR, 1,  "ZOOM (x2)"))
        MENU3.append(CBouton(self.MOTEUR, 2,  "MUSIC (ON)"))
        MENU3.append(CBouton(self.MOTEUR, 3,  "PARTICULE (ON)"))
        self.LISTE["OPTIONS"] = MENU3

        MENU4 = []
        MENU4.append(CBouton(self.MOTEUR, 0, "ORGINAL (15x13)"))
        MENU4.append(CBouton(self.MOTEUR, 1, "NORMAL"))
        MENU4.append(CBouton(self.MOTEUR, 2, "LARGE"))
        MENU4.append(CBouton(self.MOTEUR, 3, "AU TAQUET"))
        self.LISTE["NIVEAU"] = MENU3
        
        self.Initialiser_Cadre_Menu()
        

    def Initialiser_Cadre_Menu(self):

        
   
        
        self.largeurBouton, self.hauteurBouton = (VAR.nbColonnes - 2) * VAR.tailleCellule, 100
        self.x, self.y = (VAR.resolution[0] - self.largeurZone) - 96,  int((VAR.resolution[1] - len(self.LISTE[self.menu]) * (self.hauteurBouton+10))  / 2)
        
        # -- Terrain
        
             
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
            if not bouton.texte == "":
                presse = bouton.Afficher_Bouton(self.x, self.y)
                
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
    def __init__(self, _moteur, _id, _texte):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        
        self.id = _id
        
        self.activer = False
        self.texte = _texte
        
        self.largeurZoneOk = VAR.tailleCellule * 2
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        
    def Afficher_Bouton(self, _x, _y):
        self.largeur = self.MOTEUR.MENU.largeurBouton
        self.hauteur = self.MOTEUR.MENU.hauteurBouton
        
        
        x = _x + VAR.tailleCellule
        y = _y + (self.id * (self.hauteur+10))
        if self.id == 99: y += VAR.tailleCellule
        
        texte = FCT.Image_Texte(self.texte, (255,255,255,255), int(20))
        centreX = (self.largeur - texte.get_width()-self.largeurZoneOk) / 2
        centreY = (self.hauteur - texte.get_height()) /2
        
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeur, self.hauteur, self.couleur_fond, self.couleur_bordure, 4)
        
        joueur = self.MOTEUR.JOUEURS.LISTE[0]
        coord_joueur = (joueur.oX(), joueur.oY(), VAR.tailleCellule /2, VAR.tailleCellule/2)
        coord_bouton = (x, y, self.largeurZoneOk, self.hauteur)
        if FCT.ContientDans(coord_joueur, coord_bouton):
            couleur = (255,0,0)
        else:
            couleur = (128,128,128)
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeurZoneOk, self.hauteur, couleur, self.couleur_bordure, 4)    
        VAR.fenetre.blit(texte, (x + centreX + self.largeurZoneOk, y + centreY))
        
        return False
    
