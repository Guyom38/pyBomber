import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

class CJoueurs():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur

        
    def nbJoueurs_enVie(self):
        return len([1 for joueur in self.LISTE if not joueur.vraimentMort()])
    
    def quiGagne(self):
        for joueur in self.LISTE:
            if not joueur.mort: return joueur
        return None
     
    def Initialiser(self):
        self.LISTE = []
        
        self.Recolorisation_Joueurs()
        self.image_masque = FCT.Colorisation_Masque(VAR.image["joueur0"])   
    
    def Reinitaliser(self):
        for joueur in self.LISTE:
            joueur.Initialiser()
                
    def Afficher_Tous_Les_Joueurs(self):
        # --- retri les joueurs pour que si un joueur s'affiche devant l'autre, il soit afficher apres
        liste_joueurs_tries = sorted(self.LISTE, key=lambda joueur: joueur.y)
        self.joueurs_EnVie = 0
        
        for joueur in liste_joueurs_tries:
            joueur.Afficher() 
            
            if not joueur.mort: self.joueurs_EnVie += 1
            
    def Recolorisation_Joueurs(self):
        for key, value in VAR.LISTE_COLOR_COEFF.items():
            VAR.LISTE_COLOR[key] = []
            for r,g,b in VAR.LISTE_COLOR_JOUEURS:
                new_valeur_r = int(r * value)
                if new_valeur_r > 255: new_valeur_r = 255
                if new_valeur_r < 0: new_valeur_r = 0
                
                new_valeur_g = int(g * value)
                if new_valeur_g > 255: new_valeur_g = 255
                if new_valeur_g < 0: new_valeur_g = 0
                
                new_valeur_b = int(b * value)
                if new_valeur_b > 255: new_valeur_b = 255
                if new_valeur_b < 0: new_valeur_b = 0
                
                VAR.LISTE_COLOR[key].append((new_valeur_r, new_valeur_g, new_valeur_b, 255))
            
