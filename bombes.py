import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import bombe as CB


class CBombes:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.LISTE = []
    
    def Afficher_Toutes_Les_Bombes(self):
        self.Purger_Bombes_Explosees()
        
        for bombe in self.LISTE:
            bombe.Afficher()   

    def Purger_Bombes_Explosees(self):
        self.LISTE = [bombe for bombe in self.LISTE if bombe.etat != "A EXPLOSE"]
            
    def Ajouter(self, _joueur):
        bombe = CB.CBombe(self, _joueur)
        _joueur.bombes_protection = bombe
        
        self.LISTE.append(bombe)
        _joueur.bombes_posees += 1
        
    def Explosion_En_Chaine(self, _x, _y):
        for bombe in self.LISTE:
            if not bombe == self:
                if bombe.x == _x and bombe.y == _y:
                    bombe.Raccrourci_Delais_Explosion()
                    
    def Detection_Collision_Avec_Bombes(self, _joueur):
        coordJoueur = ((_joueur.x * VAR.tailleCellule), (_joueur.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        for bombe in self.LISTE:            
            coordBombe = ((bombe.x * VAR.tailleCellule), (bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if _joueur.bombes_protection == bombe: 
                return False
            
            if FCT.Collision(coordJoueur, coordBombe):
                if _joueur.coup_de_pied and not bombe.enMouvement: 
                    bombe.direction = _joueur.direction
                    bombe.enMouvement = True
                    
                    return False  
                else: 
                    return True
        return False