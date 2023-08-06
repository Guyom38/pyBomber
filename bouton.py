import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import time, math

class CBouton():
    def __init__(self, _moteur, _id, _texte, _fonction = None):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        
        self.id = _id
        
        self.activer = False
        self.texte = _texte
        
        self.fonction = _fonction
        
            
        
       
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        
        
        
    def Afficher_Bouton(self, _x, _y):
        bouton_presse = False
        
        self.largeur = self.MOTEUR.MENU.largeurBouton
        self.hauteur = self.MOTEUR.MENU.hauteurBouton
        self.largeurZoneOk = 0
         
        if self.id == 0: 
            self.hauteur = (self.hauteur * 2) - 20
            self.largeurZoneOk = self.hauteur
        
        x = _x + VAR.tailleCellule
        y = _y
        if self.id == 99: y += VAR.tailleCellule
        txt = self.texte
        if not self.fonction == None: txt += " ("+str(self.fonction(True))+")"
        
        texte = FCT.Image_Texte(txt, (255,255,255,255), int(20))
        centreX = (self.largeur - texte.get_width() - self.largeurZoneOk) / 2        
        centreY = (self.hauteur - texte.get_height()) /2
        
        
        couleur = (128,128,128)
        couleur2 = (0,0,0)
        
        for joueur in self.MOTEUR.JOUEURS.LISTE:            
            coord_joueur = (joueur.oX() + (VAR.tailleCellule/2), joueur.oY()+(VAR.tailleCellule/2), VAR.tailleCellule/2 , VAR.tailleCellule/2)
            coord_bouton = (x, y, self.largeur, self.hauteur)
            if FCT.ContientDans(coord_joueur, coord_bouton):
                
                
                if joueur.id == 0:
                    couleur = (237,0,140)
                    couleur2 = (75,107,220) 
                
                    if self.MOTEUR.CONTROLLEUR.action_bouton == True:
                        bouton_presse = True
                        if not self.fonction == None :
                            self.fonction(False)
                            
                joueur.clown = (self.id == 0)

                

        
        self.INTERFACE.Dessiner_Cadre(x, y, self.largeur, self.hauteur, couleur2, self.couleur_bordure, 4) 
        
        if self.id == 0: 
            #self.INTERFACE.Dessiner_Cadre(x, y, self.hauteur, self.hauteur, couleur, self.couleur_bordure, 4) 
            VAR.fenetre.blit(pygame.transform.scale(VAR.image["start"], (self.hauteur - math.cos(time.time()) * (self.hauteur / 3), (self.hauteur - 8))), (x + 4, y + 4))  
       
          
        VAR.fenetre.blit(texte, (x + centreX + self.largeurZoneOk, y + centreY))
        
        return bouton_presse