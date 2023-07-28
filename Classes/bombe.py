import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT


import time

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
        self.LISTE.append(CBombe(self, _joueur))
        _joueur.bombes_posees += 1
        
    def Explosion_En_Chaine(self, _x, _y):
        for bombe in self.LISTE:
            if not bombe == self:
                if bombe.x == _x and bombe.y == _y:
                    bombe.Raccrourci_Delais_Explosion()
                    
    def Detection_Collision_Avec_Bombes(self, _joueur):
        for bombe in self.LISTE:            
            objet_bombe = ((bombe.x * VAR.tailleCellule), (bombe.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if int(round(bombe.x * VAR.tailleCellule, 0)) == int(round(_joueur[0], 0)) and int(round(bombe.y * VAR.tailleCellule, 0)) == int(round(_joueur[1], 0)): 
                print("kk")
                return False
            
            if FCT.Collision(_joueur, objet_bombe):    
                return True
        return False
        
class CBombe:   
    class CFeu:
        def __init__(self, _x, _y):
            self.x = _x
            self.y = _y
            
            
            
                
    def __init__(self, _bombes, _joueur):
        self.BOMBES = _bombes
        self.TERRAIN = _bombes.MOTEUR.TERRAIN
        self.JOUEUR = _joueur
        
        self.delais = 3.0
        self.temps = time.time()
        self.animationId = 0
        
        self.force = _joueur.puissance+1        
        self.x, self.y = round(_joueur.x, 0), round(_joueur.y, 0)
        self.etat = "VA EXPLOSER"
        
        self.feuSTOP = {"" : True, "DROITE" : True, "GAUCHE" : True, "HAUT" : True, "BAS" : True}
        self.feuSTOP_nb = {"" : 0, "DROITE" : 0, "GAUCHE" : 0, "HAUT" : 0, "BAS" : 0}
    
    
    
    
    def Afficher(self):       
                
        if self.etat == "VA EXPLOSER":
            posX = int(VAR.offSet[0] + (self.x * VAR.tailleCellule))
            posY = int(VAR.offSet[1] + (self.y * VAR.tailleCellule))    
            animationId = int((time.time()*10) % 3)
              
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["objets"], animationId, 1, VAR.tailleCellule,  VAR.tailleCellule), (posX, posY))  
            
            if time.time() - self.temps > self.delais:
                self.Initiatiser_Explosion()
               
                
        elif self.etat == "EXPLOSE": 
            self.Gestion_Explosion()
            
            for i in range(0, len(self.FOYER)):
                posX = VAR.offSet[0] + (self.FOYER[i].x * VAR.tailleCellule)
                posY = VAR.offSet[1] + (self.FOYER[i].y * VAR.tailleCellule)
                animationId = self.animationId *2
                pygame.draw.rect(VAR.fenetre, (255,0,0), (posX+(animationId/2), posY+(animationId/2), VAR.tailleCellule-animationId, VAR.tailleCellule-animationId))  
        
        

    
    def Initiatiser_Explosion(self):
        self.FOYER = []
        self.FOYER.append(CBombe.CFeu(round(self.x, 0), round(self.y, 0)))         
        self.initialiser = False
        self.etat = "EXPLOSE"
        self.JOUEUR.bombes_posees -= 1
    
    def Raccrourci_Delais_Explosion(self):
        self.delais = 0.01
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
                            
            elif self.feuSTOP_nb[_sens]+1 == _force:
                if grille[_posX][_posY].Cassable():
                    grille[_posX][_posY].Casser_Mur()   
                              
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
                
                
                
            
                
                