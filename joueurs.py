import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

class CJoueurs():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.LISTE = []
        
        self.joueurs_EnVie  = 0
        
    def Afficher_Tous_Les_Joueurs(self):
        # --- retri les joueurs pour que si un joueur s'affiche devant l'autre, il soit afficher apres
        liste_joueurs_tries = sorted(self.LISTE, key=lambda joueur: joueur.y)
        self.joueurs_EnVie = 0
        
        for joueur in liste_joueurs_tries:
            joueur.Afficher() 
            
            if not joueur.mort: self.joueurs_EnVie += 1