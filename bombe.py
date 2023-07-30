import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import time
        
class CBombe:   
    class CFeu:
        def __init__(self, _x, _y):
            self.x = _x
            self.y = _y            
            
    def iX(self): return int(round(self.x, 0))   
    def iY(self): return int(round(self.y, 0))            
                
    def __init__(self, _bombes, _joueur):
        self.BOMBES = _bombes
        self.TERRAIN = _bombes.MOTEUR.TERRAIN
        self.JOUEUR = _joueur
        
        self.enMouvement = False
        self.direction = "DROITE"
        
        self.delais = VAR.delaisExplosion
        self.temps = time.time()
        self.animationId = 0
        
        self.force = _joueur.puissance+1        
        self.x, self.y = round(_joueur.x, 0), round(_joueur.y, 0)
        self.etat = "VA EXPLOSER"
        
        self.feuSTOP = {"" : True, "DROITE" : True, "GAUCHE" : True, "HAUT" : True, "BAS" : True}
        self.feuSTOP_nb = {"" : 0, "DROITE" : 0, "GAUCHE" : 0, "HAUT" : 0, "BAS" : 0}
    
    def Initiatiser_Explosion(self):
        self.FOYER = []
        self.FOYER.append(CBombe.CFeu(round(self.x, 0), round(self.y, 0)))         
        self.initialiser = False
        self.etat = "EXPLOSE"
        self.JOUEUR.bombes_posees -= 1    

    
    
    
    def Afficher(self):  
        if self.etat == "VA EXPLOSER":
            self.Gestion_Bombe_Qui_Roule()
            self.Afficher_Animation_Bombe_Qui_Va_Peter()             
                
        elif self.etat == "EXPLOSE": 
            self.Afficher_Explosion_De_La_Bombe()
            
            
    def Afficher_Animation_Bombe_Qui_Va_Peter(self):
        posX = int(VAR.offSet[0] + (self.x * VAR.tailleCellule))
        posY = int(VAR.offSet[1] + (self.y * VAR.tailleCellule))                
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image["objets"], FCT.Animation(10, 3), 1, VAR.tailleCellule,  VAR.tailleCellule), (posX, posY))  
            
        # --- si delais bombe expiré, alors BOOM
        if time.time() - self.temps > self.delais:
            self.Initiatiser_Explosion()
            

    def Afficher_Explosion_De_La_Bombe(self):
        self.Gestion_Explosion()
            
        for i in range(0, len(self.FOYER)):
            posX = VAR.offSet[0] + (self.FOYER[i].x * VAR.tailleCellule)
            posY = VAR.offSet[1] + (self.FOYER[i].y * VAR.tailleCellule)
            animationId = self.animationId *2
            pygame.draw.rect(VAR.fenetre, (255,0,0), (posX+(animationId/2), posY+(animationId/2), VAR.tailleCellule-animationId, VAR.tailleCellule-animationId))  
        
    
    
    
    def Raccrourci_Delais_Explosion(self):
        self.delais = 0.00
        self.temps = time.time()
        

    def Detection_KesKi_Pete(self, _posX, _posY, _sens, _force):               
        grille = self.TERRAIN.GRILLE               
        if _posX >=0 and _posX < VAR.nbColonnes and _posY >=0 and _posY < VAR.nbLignes:
            self.feuSTOP[_sens] = (grille[_posX][_posY].Traversable() and self.feuSTOP[_sens])                    
            self.BOMBES.Explosion_En_Chaine(_posX, _posY)
                        
            if self.feuSTOP[_sens]: 
                self.FOYER.append(CBombe.CFeu(_posX, _posY))
                self.feuSTOP_nb[_sens] = _force
                            
                for joueur in self.BOMBES.MOTEUR.JOUEURS.LISTE:
                    if _posX == joueur.iX() and _posY == joueur.iY():
                        joueur.Mourir()                
                
                for objet in self.BOMBES.MOTEUR.OBJETS.LISTE:
                    if _posX == objet.iX() and _posY == objet.iY():
                        objet.etat = "A EXPLOSE"                     
                            
            elif self.feuSTOP_nb[_sens]+1 == _force:
                if grille[_posX][_posY].Cassable():
                    grille[_posX][_posY].Casser_Mur()   
    
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
        if (0 > self.iX() < VAR.nbColonnes) or (0 > self.iY() < VAR.nbLignes): return True
        
        # --- Collision avec mur
        if not self.TERRAIN.GRILLE[self.iX()][self.iY()].Traversable(): return True
        
        # --- Collision avec Bombe
        # --- Collision avec Objet
        # --- Collision avec Joueur
                                 
    def Gestion_Explosion(self):
        if not self.initialiser:
            self.feuSTOP = {"" : True, "DROITE" : True, "GAUCHE" : True, "HAUT" : True, "BAS" : True}
            self.feuSTOP_nb = {"" : 0, "DROITE" : 0, "GAUCHE" : 0, "HAUT" : 0, "BAS" : 0}
            self.initialiser = True

            # --- ajoute la position sous le joueur
            self.Detection_KesKi_Pete(int(round(self.x, 0)), int(round(self.y, 0)), "", 1) 
            
            # --- progresse tout autour
            for force in range(1, self.force):
                for sens, xD, yD in (("DROITE", -force, 0), ("GAUCHE", force, 0), ("HAUT", 0, -force), ("BAS", 0, force)):
                    posX, posY = int(round(self.x + xD, 0)), int(round(self.y + yD, 0))
                    self.Detection_KesKi_Pete(posX, posY, sens, force) 
            
            
        else:
            if time.time() - self.temps > 0.05:
                self.temps = time.time()      
                self.animationId += 1
                
            if self.animationId > 5:
                self.etat = "A EXPLOSE"
                
                
                
            
                
                