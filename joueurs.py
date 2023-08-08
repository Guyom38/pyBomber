import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

class CJoueurs():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.LISTE = []
    
    def Activer_Tous_Les_Joueurs(self):
        for joueur in self.LISTE:
            joueur.actif = True
            
    def nbJoueurs(self):
        return len(self.LISTE)
    
    def nbJoueurs_enVie(self):
        return len([1 for joueur in self.LISTE if not joueur.vraimentMort() and joueur.actif])
    
    def quiGagne(self):
        for joueur in self.LISTE:
            if not joueur.mort and joueur.actif: return joueur
        return None
     
    def Initialiser(self):
        self.LISTE = []
        
        self.Recolorisation_Joueurs()
        
        
        print("redessine joueurs")
    
    def Reinitaliser(self):

        position = 0
        for joueur in self.LISTE:
            if joueur.actif:                
                joueur.Initialiser(position)
                position += 1
                
        self.image_masque = FCT.Colorisation_Masque(VAR.image["joueur0"])   
                

        

                
    def Afficher_Tous_Les_Joueurs(self, _joueur_a_afficher = None):
        # --- retri les joueurs pour que si un joueur s'affiche devant l'autre, il soit afficher apres
        liste_joueurs_tries = sorted(self.LISTE, key=lambda joueur: joueur.y)
        self.joueurs_EnVie = 0
        
        if _joueur_a_afficher == None:   
            for joueur in liste_joueurs_tries:
                if joueur.actif:
                    if not joueur.mort : self.joueurs_EnVie += 1
                    joueur.Afficher()                 
                
        else:
            liste_joueurs_tries[_joueur_a_afficher].Afficher()
            
            
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
                
                
    def RePositionne_Joueurs(self):
        for joueur in self.LISTE:
            joueur.Position_Initiale()
            
            
    def Resurection_Joueurs(self):
        for joueur in self.LISTE:
            joueur.mort = True
            
