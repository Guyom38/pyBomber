import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

class CBouton():
    def __init__(self, _moteur, _id, _texte, _fonction = None):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        
        self.id = _id
        
        self.activer = False
        self.texte = _texte
        
        self.fonction = _fonction
        
            
        
        self.largeurZoneOk = VAR.tailleCellule * 2
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        
        
        
    def Afficher_Bouton(self, _x, _y):
        bouton_presse = False
        
        self.largeur = self.MOTEUR.MENU.largeurBouton
        self.hauteur = self.MOTEUR.MENU.hauteurBouton
        
        
        x = _x + VAR.tailleCellule
        y = _y + (self.id * (self.hauteur+10))
        if self.id == 99: y += VAR.tailleCellule
        txt = self.texte
        if not self.fonction == None: txt += " ("+str(self.fonction(True))+")"
        
        texte = FCT.Image_Texte(txt, (255,255,255,255), int(20))
        centreX = (self.largeur - texte.get_width()-self.largeurZoneOk) / 2
        centreY = (self.hauteur - texte.get_height()) /2
        
        
        
        joueur = self.MOTEUR.JOUEURS.LISTE[0]
        coord_joueur = (joueur.oX() + (VAR.tailleCellule/2), joueur.oY()+(VAR.tailleCellule/2), VAR.tailleCellule/2 , VAR.tailleCellule/2)
        coord_bouton = (x, y, self.largeur, self.hauteur)
        if FCT.ContientDans(coord_joueur, coord_bouton):
            couleur = (237,0,140)
            couleur2 = (75,107,220) 
            
            if self.MOTEUR.CONTROLLEUR.action_bouton == True:
                bouton_presse = True
                if not self.fonction == None :
                    self.fonction(False)
        else:
            couleur = (128,128,128)
            couleur2 = (0,0,0)
        
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeur, self.hauteur, couleur2, self.couleur_bordure, 4)    
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeurZoneOk, self.hauteur, couleur, self.couleur_bordure, 4)    
        VAR.fenetre.blit(texte, (x + centreX + self.largeurZoneOk, y + centreY))
        
        return bouton_presse