import pygame
from pygame.locals import *


import variables as VAR
import fonctions as FCT

import time
from explosion import *
import item
       
class CBombe(item.CItem):    
               
                
    def __init__(self, _bombes, _joueur):
        super().__init__(_bombes.MOTEUR, _joueur.celluleX(), _joueur.celluleY(), C_ETAPE_BOMBE.VA_PETER)    
        
        self.JOUEUR = _joueur        
        self.EXPLOSION = CExplosion(self)
        
        self.delais = VAR.delaisExplosion
        self.jouer_son_en_retard = False        
             
    
    def Afficher(self):  
        if self.etat == C_ETAPE_BOMBE.VA_PETER:
            self.Gestion_Bombe_Qui_Roule()
            self.Gestion_CompteARebourd_Bombe()  
            self.Afficher_La_Bombe()                       
                
        elif self.etat == C_ETAPE_BOMBE.EXPLOSE: 
            self.EXPLOSION.Afficher_Explosion_De_La_Bombe()            
            
    def Afficher_La_Bombe(self):
        image = FCT.image_decoupe(VAR.image["objets"], FCT.Animation(10, 3), 1, VAR.tailleCellule,  VAR.tailleCellule)
        VAR.fenetre.blit(image, (self.ecranX(), self.ecranY()))  


    def Gestion_Bombe_Qui_Roule(self):
        if not self.enMouvement: return
        
        oldPosition = self.x, self.y
        if self.direction == C_DIRECTION.DROITE: self.x += VAR.C_VITESSE_BOMBE_ROULE
        if self.direction == C_DIRECTION.GAUCHE: self.x -= VAR.C_VITESSE_BOMBE_ROULE
        if self.direction == C_DIRECTION.HAUT: self.y -= VAR.C_VITESSE_BOMBE_ROULE
        if self.direction == C_DIRECTION.BAS: self.y += VAR.C_VITESSE_BOMBE_ROULE
        
        if self.Detection_Collisions():
            self.x, self.y = oldPosition
            self.x, self.y = self.celluleX(), self.celluleY()
            self.enMouvement = False
            
    def Gestion_CompteARebourd_Bombe(self):
        # --- anticipe le son du jeu
        if time.time() - self.temps > self.delais - 0.10 and not self.jouer_son_en_retard:
            FCT.jouer_sons("explosion")
            self.jouer_son_en_retard = True
        
        # --- si delais bombe expiré, alors BOOM    
        if time.time() - self.temps > self.delais:                        
            self.EXPLOSION.Initiatiser_Explosion()

    def Detection_Collisions(self):
        # --- Controle sortie de terrain
        if not FCT.Position_Sur_Terrain(self.celluleX(), self.celluleY()): return True
        
        # --- Collision avec mur
        if not self.TERRAIN.GRILLE[self.celluleX()][self.celluleY()].Traversable(): return True
        
        # --- Collision avec Bombe
        if not FCT.Detection_Collision(self.BOMBES, self) == None: return True
        
        # --- Collision avec Objet        
        #bombe = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        if FCT.Detection_Collision(self.OBJETS, self): return True
        
        # --- Collision avec Joueur
       
                
                
            
                
                