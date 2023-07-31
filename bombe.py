import pygame
from pygame.locals import *


import variables as VAR
import fonctions as FCT

import time
from explosion import *

        
class CBombe:    
               
                
    def __init__(self, _bombes, _joueur):
        self.BOMBES = _bombes
        self.TERRAIN = _bombes.MOTEUR.TERRAIN
        self.OBJETS = _bombes.MOTEUR.OBJETS
        self.JOUEUR = _joueur
        
        self.EXPLOSION = CExplosion(self)
        
        self.enMouvement = False
        self.direction = "DROITE"
        
        self.delais = VAR.delaisExplosion
        self.temps = time.time()
        self.animationId = 0
        self.jouer_son_en_retard = False        
             
        self.x, self.y = _joueur.iX(), _joueur.iY()
        self.etat = "VA EXPLOSER"
        
    def iX(self): return int(round(self.x, 0))   
    def iY(self): return int(round(self.y, 0)) 
    
    def Afficher(self):  
        if self.etat == "VA EXPLOSER":
            self.Gestion_Bombe_Qui_Roule()
            self.Gestion_CompteARebourd_Bombe()  
            self.Afficher_La_Bombe()                       
                
        elif self.etat == "EXPLOSE": 
            self.EXPLOSION.Afficher_Explosion_De_La_Bombe()
            
            
    def Afficher_La_Bombe(self):
        posX = int(VAR.offSet[0] + (self.x * VAR.tailleCellule))
        posY = int(VAR.offSet[1] + (self.y * VAR.tailleCellule))                
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["objets"], FCT.Animation(10, 3), 1, VAR.tailleCellule,  VAR.tailleCellule), (posX, posY))  


    def Gestion_CompteARebourd_Bombe(self):
        if time.time() - self.temps > self.delais - 0.10 and not self.jouer_son_en_retard:
            FCT.jouer_sons("explosion")
            self.jouer_son_en_retard = True
        
        # --- si delais bombe expiré, alors BOOM    
        if time.time() - self.temps > self.delais:            
            self.EXPLOSION.Initiatiser_Explosion()

    def Gestion_Bombe_Qui_Roule(self):
        if not self.enMouvement: return
        
        oldPosition = self.x, self.y
        if self.direction == "DROITE": self.x += 0.05
        if self.direction == "GAUCHE": self.x -= 0.05
        if self.direction == "HAUT": self.y -= 0.05
        if self.direction == "BAS": self.y += 0.05
        
        if self.Detection_Collision_Avec_Decors():
            self.x, self.y = oldPosition
            self.x, self.y = self.iX(), self.iY()
            self.enMouvement = False
        
        
    def Detection_Collision_Avec_Decors(self):
        # --- Controle sortie de terrain
        if not FCT.Position_Sur_Terrain(self.iX(), self.iY()): return True
        
        # --- Collision avec mur
        if not self.TERRAIN.GRILLE[self.iX()][self.iY()].Traversable(): return True
        
        # --- Collision avec Bombe
        if self.BOMBES.Detection_Collision_Avec_Autres_Bombes(self): return True
        # --- Collision avec Objet
        
        bombe = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        if self.OBJETS.Detection_Collision_Avec_Objets(bombe): return True
        
        # --- Collision avec Joueur
       
                
                
            
                
                