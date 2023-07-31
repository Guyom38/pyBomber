import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

class CJoueurs():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.LISTE = []
        
        self.joueurs_EnVie  = 0
        self.image_masque = VAR.image["joueur0"].copy()    
        self.Colorisation_Masque()
        
    def Afficher_Tous_Les_Joueurs(self):
        # --- retri les joueurs pour que si un joueur s'affiche devant l'autre, il soit afficher apres
        liste_joueurs_tries = sorted(self.LISTE, key=lambda joueur: joueur.y)
        self.joueurs_EnVie = 0
        
        for joueur in liste_joueurs_tries:
            joueur.Afficher() 
            
            if not joueur.mort: self.joueurs_EnVie += 1
            
    # -- image rempli de blanc, lorsque le joueur clignotte !    
    def Colorisation_Masque(self):
        for y in range(self.image_masque.get_height()):
            for x in range(self.image_masque.get_width()):
                couleur = self.image_masque.get_at((x, y))
                if not VAR.C_COLOR_TRANSPARENT == couleur:
                    self.image_masque.set_at((x,y), (255,255,255,255))   