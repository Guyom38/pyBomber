import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

import cellule as CC
import bouton as CB

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
    
    def Action_NombreParties(self, _juste_valeur):
        if _juste_valeur:
            if VAR.nb_parties == 0: return "illimité"
            return VAR.nb_parties
        else:
            VAR.nb_parties += 1
            if VAR.nb_parties > 10: VAR.nb_parties = 0
    def Action_DureeParties(self, _juste_valeur):
        if _juste_valeur:
            if VAR.duree_partie == 0: return "illimité"
            return FCT.convert_seconds_to_time(VAR.duree_partie)
        else: 
            VAR.duree_partie += 30
            if VAR.duree_partie > 600: VAR.duree_partie = 0
    def Action_Active_Maladies(self, _juste_valeur):
        if _juste_valeur:
            return "ON" if VAR.active_maladies else "OFF"
        else:
            VAR.active_maladies = not VAR.active_maladies
    def Action_Active_Heritage(self, _juste_valeur):
        if _juste_valeur:
            return "ON" if VAR.active_heritage else "OFF"
        else:
            VAR.active_heritage = not VAR.active_heritage
            
    
    def Initialiser(self):
        self.largeurZone = 640
        VAR.nbColonnes = int((self.largeurZone / VAR.tailleCellule)) +1
        VAR.nbLignes = int((VAR.resolution[1] / VAR.tailleCellule)) - 2        
        self.largeurBouton, self.hauteurBouton = (VAR.nbColonnes - 2) * VAR.tailleCellule, 64
        
        self.TERRAIN.GRILLE =  [[CC.CCellule(self.MOTEUR, x, y) for y in range(VAR.nbLignes)] for x in range(VAR.nbColonnes)]
        self.TERRAIN.Construire_Terrain_De_Jeu(True)
        self.TERRAIN.image = None           
               
        
        
        self.LISTE = {}
        self.menu = "PRINCIPAL"
        self.menu_sous = ""
        self.id = 0
        
        MENU1 = []
        MENU1.append(CB.CBouton(self.MOTEUR, 0, "PARTIE RAPIDE"))
        MENU1.append(CB.CBouton(self.MOTEUR, 1, "PERSONNALISER"))
        MENU1.append(CB.CBouton(self.MOTEUR, 2, "OPTIONS"))
        MENU1.append(CB.CBouton(self.MOTEUR, 3, ""))
        MENU1.append(CB.CBouton(self.MOTEUR, 4, "QUITTER"))
        self.LISTE["PRINCIPAL"] = MENU1
        
        MENU2 = []
        MENU2.append(CB.CBouton(self.MOTEUR, 0,  "NB. MANCHES", self.Action_NombreParties))
        MENU2.append(CB.CBouton(self.MOTEUR, 1,  "DUREE", self.Action_DureeParties))
        MENU2.append(CB.CBouton(self.MOTEUR, 2,  "MALADIES", self.Action_Active_Maladies))
        MENU2.append(CB.CBouton(self.MOTEUR, 3,  "HERITAGE", self.Action_Active_Heritage))           
        self.LISTE["PARTIE"] = MENU2
        
        MENU4 = []
        MENU4.append(CB.CBouton(self.MOTEUR, 0, "ORGINAL (15x13)"))
        MENU4.append(CB.CBouton(self.MOTEUR, 1, "NORMAL"))
        MENU4.append(CB.CBouton(self.MOTEUR, 2, "LARGE"))
        MENU4.append(CB.CBouton(self.MOTEUR, 3, "AU TAQUET"))
        self.LISTE["NIVEAU"] = MENU4
        
       

        MENU3 = []
        MENU3.append(CB.CBouton(self.MOTEUR, 0,  "RESOLUTION (1024x768)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 1,  "ZOOM (x2)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 2,  "MUSIC (ON)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 3,  "PARTICULE (ON)"))
        self.LISTE["OPTIONS"] = MENU3

        
        
   
         
  
        
    def Dessiner_Titre(self):
        VAR.fenetre.blit(VAR.image['titre'], (0, 0))    
         
    
    def Dessiner_Bouton(self):
        self.x, self.y = (VAR.resolution[0] - self.largeurZone) - 96,  int((VAR.resolution[1] - len(self.LISTE[self.menu]) * (self.hauteurBouton+10))  / 2)
        VAR.offSet = (self.x, VAR.tailleCellule) 
        
        for bouton in self.LISTE[self.menu]:
            if not bouton.texte == "":
                bouton_presse = bouton.Afficher_Bouton(self.x, self.y)
                
                if bouton_presse:
                    if self.menu == "PRINCIPAL":
                        if bouton.id == 0:
                            self.MOTEUR.phase_jeu = C_PHASE_DE_JEU.JEU
                            self.MOTEUR.Relancer_Une_Partie()
                            
                        elif bouton.id == 1:
                            self.menu = "PARTIE"
                            
                        elif bouton.id == 2:
                            self.menu = "OPTIONS"
                        elif bouton.id == 4:
                            VAR.boucle_jeu = False
                            
                            
                            
        self.MOTEUR.CONTROLLEUR.action_bouton = False
                            
    def Dessiner_Particules(self):
        if time.time() - self.temps_particules > self.temps_delais:
            self.temps_particules = time.time()            
            for _ in range(4):
                self.PARTICULES.Ajouter_Particule(random.randint(0, VAR.resolution[0]), VAR.resolution[1], (162, 104, 254))
        self.PARTICULES.Afficher_Les_Particules()  
           
    def Afficher_Menu(self):
        self.Dessiner_Titre()
        self.TERRAIN.Afficher() 
        self.Dessiner_Bouton()
        self.JOUEURS.Afficher_Tous_Les_Joueurs()
        self.Dessiner_Particules()

                
    
    
    
    

    
