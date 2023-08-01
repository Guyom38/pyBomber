import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import bombe as CB
import random

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
            
    def Ajouter(self, _joueur):
        bombe = CB.CBombe(self, _joueur)
        if _joueur.maladie == C_MALADIE.BOMBES_A_RETARDEMENT: bombe.delais = random.randint(4, 20)
        
        _joueur.bombes_protection = bombe
        _joueur.bombes_posees += 1
        
        self.LISTE.append(bombe)
        
        
    def Explosion_En_Chaine(self, _x, _y):
        for bombe in self.LISTE:
            if not bombe == self:
                if bombe.x == _x and bombe.y == _y:
                    bombe.EXPLOSION.Raccrourci_Delais_Explosion()
    
    def Detection_Collision_Avec_Une_Bombe(self, _joueur, _bombe):
        coordBombe = ((_bombe.x * VAR.tailleCellule), (_bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        coordJoueur = ((_joueur.x * VAR.tailleCellule), (_joueur.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        return FCT.Collision(coordJoueur, coordBombe)
    
    def Detection_Collision_Avec_Autres_Bombes(self, _bombe):
        coordBombe1 = ((_bombe.x * VAR.tailleCellule), (_bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        for bombe in self.LISTE:            
            coordBombe2 = ((bombe.x * VAR.tailleCellule), (bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            if not bombe == _bombe:
                if FCT.Collision(coordBombe1, coordBombe2):
                    return True                
        return False
                           
    def Detection_Collision_Avec_Les_Bombes(self, _joueur):
        coordJoueur = ((_joueur.x * VAR.tailleCellule), (_joueur.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        for bombe in self.LISTE:            
            coordBombe = ((bombe.x * VAR.tailleCellule), (bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            # --- Joueur protection activée, le joueur passe sur la bombe
            if _joueur.bombes_protection == bombe: 
                return False
            
            # --- Teste collision entre bombe et joueur
            if FCT.Collision(coordJoueur, coordBombe):
                if _joueur.coup_de_pied and not bombe.enMouvement: 
                    bombe.direction = _joueur.direction
                    bombe.enMouvement = True
                    
                    return False  
                else: 
                    return True
        return False