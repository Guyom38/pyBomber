import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT
import random
import objet as CO

from enums import *

class CObjets:    
    def __init__(self, _moteur):        
        self.MOTEUR = _moteur
        self.LISTE = []
        self.PIOCHES = []
    
    def Initialiser(self):
        for _ in range(10): self.PIOCHES.append(C_OBJET.BOMBE)
        for _ in range(10): self.PIOCHES.append(C_OBJET.FLAMME)
        for _ in range(5): self.PIOCHES.append(C_OBJET.ROLLER)
        for _ in range(2): self.PIOCHES.append(C_OBJET.COUP_PIED)
        for _ in range(2): self.PIOCHES.append(C_OBJET.COUP_POING)
        for _ in range(10): self.PIOCHES.append(C_OBJET.MALADIE)
        for _ in range(2): self.PIOCHES.append(C_OBJET.SUPER_FLAMME)
        for _ in range(30): self.PIOCHES.append(None)            
        random.shuffle(self.PIOCHES)  
    
            
    def Afficher_Tous_Les_Objets(self):
        self.Purger_Objets_Exploses()
        
        for objet in self.LISTE:
            objet.Afficher()
            
    def Ajouter_Ou_Pas_Un_Objet(self, _x, _y):          
        objet_hasard = self.PIOCHES.pop(0)  
        if not (objet_hasard == None):
            self.Ajouter_Un_Objet(_x, _y, objet_hasard)
    
    
    def Purger_Objets_Exploses(self):
        self.LISTE = [objet for objet in self.LISTE if objet.etat != "A EXPLOSE"]
        
    def Ajouter_Un_Objet(self, _x, _y, _objet_hasard, _jeter = False, _oX = 0, _oY =0):
        objet = CO.CObjet(self.MOTEUR, _x, _y, _objet_hasard)
        
        if (_jeter):
            sens, dX, dY = random.choice([(C_DIRECTION.DROITE,_oX,0), (C_DIRECTION.GAUCHE,-_oX,0) , (C_DIRECTION.HAUT,0,-_oY), (C_DIRECTION.BAS,0,_oY)])
            objet.xDest, objet.yDest = _x+dX, _y+dY
            objet.direction = sens
            objet.etape = random.randint(0,4)     
            objet.enMouvement = True
              
        self.LISTE.append(objet)
        
        
        
    def Detection_Collision_Avec_Objets(self, joueur):
        for objet in self.LISTE:            
            objet_objet = ((objet.x * VAR.tailleCellule), (objet.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if FCT.Collision(joueur, objet_objet):    
                return objet
        return None
    
    def Detruire_Objet(self, _objet):
        self.LISTE.remove(_objet)