import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import bombe as CB
import random, time

from enums import *

class CBombes:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur        
    
    def Initialiser(self):
        self.LISTE = []
        
    def Afficher_Toutes_Les_Bombes(self):
        self.Purger_Bombes_Explosees()
        
        for bombe in self.LISTE:
            bombe.Afficher()   

    def Purger_Bombes_Explosees(self):
        self.LISTE = [bombe for bombe in self.LISTE if bombe.etat != C_ETAPE_BOMBE.A_EXPLOSE]
    
    # retourne Vrai si aucune bombe
    def Controle_Emplacement_Libre(self, _x, _y):
        for bombe in self.LISTE:
            if bombe.celluleX() == _x and bombe.celluleY() == _y: return False            
        return True
            
    def Ajouter_Une_Bombe(self, _joueur):
        if self.Controle_Emplacement_Libre(_joueur.celluleX(), _joueur.celluleY()):         
            bombe = CB.CBombe(self, _joueur)
            if _joueur.maladie == C_MALADIE.BOMBES_A_RETARDEMENT: bombe.delais = random.randint(4, 20)
            
            _joueur.bombes_protection = bombe
            _joueur.bombes_posees += 1            
            self.LISTE.append(bombe)
            
            return True
        return False        
        
    def Explosion_En_Chaine(self, _x, _y):
        for bombe in self.LISTE:
            if not bombe == self:
                if bombe.x == _x and bombe.y == _y:
                    bombe.delais = 0.00
                    bombe.temps = time.time()
    

