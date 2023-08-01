import pygame
from pygame.locals import *

import joueur as CJ
import variables as VAR

from enums import *

class CCControlleur:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.JOUEURS = _moteur.JOUEURS
        
    def Initialiser(self):
        self.nbManettes = pygame.joystick.get_count()
        
        self.MANETTES = []
        for i in range(self.nbManettes):
            self.MANETTES.append(pygame.joystick.Joystick(i))
            pygame.joystick.Joystick(i).init()            
            print("Manette "+str(i)+" :", pygame.joystick.Joystick(i).get_name())
        
        self.Creer_Joueurs_Clavier_Manettes()
        
    def Creer_Joueurs_Clavier_Manettes(self):
        self.JOUEURS.LISTE.append(CJ.CJoueur(self.MOTEUR, 0, ""))  
        for i in range(1, self.nbManettes):
            self.JOUEURS.LISTE.append(CJ.CJoueur(self.MOTEUR, i, ""))  
    
    def Gestion_Utilisateurs(self):
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: VAR.boucle_jeu = False        
                
            self.Gestion_Manettes_Boutons(event)
                        
        # --- Gestion Clavier Joueur #1  
        self.Gestion_Clavier()

        # --- Gestion Manettes Joueur #1 a #9
        self.Gestion_Manettes_Directions()
    
    def Gestion_Clavier(self):
        if not self.JOUEURS.LISTE[0].mort:     
            BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
            if self.JOUEURS.LISTE[0].maladie == C_MALADIE.TOUCHES_INVERSEES:
                BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                        
            keys = pygame.key.get_pressed()                    
            if keys[K_LEFT] == 1:
                self.JOUEURS.LISTE[0].direction = BONNE_DIRECTION[0]
                self.JOUEURS.LISTE[0].enMouvement = True
            if keys[K_RIGHT] == 1:
                self.JOUEURS.LISTE[0].direction = BONNE_DIRECTION[1]
                self.JOUEURS.LISTE[0].enMouvement = True
            if keys[K_UP] == 1:
                self.JOUEURS.LISTE[0].direction = BONNE_DIRECTION[2]
                self.JOUEURS.LISTE[0].enMouvement = True
            if keys[K_DOWN] == 1:
                self.JOUEURS.LISTE[0].direction = BONNE_DIRECTION[3]
                self.JOUEURS.LISTE[0].enMouvement = True
                
    def Gestion_Manettes_Boutons(self, _event):
        if _event.type == KEYDOWN:  
            if _event.key == K_SPACE: 
                self.JOUEURS.LISTE[0].Action_Poser_Une_Bombe()
            if _event.key == K_LCTRL: 
                self.JOUEURS.LISTE[0].Action_Pousser_La_Bombe()
                
                    
        if _event.type == pygame.JOYBUTTONDOWN:
            if not self.JOUEURS.LISTE[_event.joy].mort:
                if (_event.button == 2):
                    self.JOUEURS.LISTE[_event.joy].Action_Poser_Une_Bombe()
                if (_event.button == 1):
                    self.JOUEURS.LISTE[_event.joy].Action_Pousser_La_Bombe()
    
    def Gestion_Manettes_Directions(self):
       
        
        for manette in self.MANETTES:
            axis_id, axis_x, axis_y = manette.get_id(), manette.get_axis(0), manette.get_axis(1)
            if not self.JOUEURS.LISTE[axis_id].mort:                
                if round(axis_x,0) != 0 or round(axis_y,0) != 0: self.JOUEURS.LISTE[axis_id].enMouvement = True 
                
                BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
                if self.JOUEURS.LISTE[axis_id].maladie == C_MALADIE.TOUCHES_INVERSEES:
                    BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                
                if axis_x < -0.5: self.JOUEURS.LISTE[axis_id].direction = BONNE_DIRECTION[0]
                if axis_x > 0.5: self.JOUEURS.LISTE[axis_id].direction =  BONNE_DIRECTION[1]
                if axis_y < -0.5: self.JOUEURS.LISTE[axis_id].direction = BONNE_DIRECTION[2]
                if axis_y > 0.5: self.JOUEURS.LISTE[axis_id].direction =  BONNE_DIRECTION[3]                