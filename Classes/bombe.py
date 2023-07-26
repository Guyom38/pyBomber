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
        for bombe in self.LISTE:
            bombe.Afficher()   
        
    def Ajouter(self, _x, _y, _puissance):
        self.LISTE.append(CBombe(self, _x, _y, _puissance))
        
    def Explosion_En_Chaine(self, _x, _y):
        for bombe in self.LISTE:
            if not bombe == self:
                x, y = bombe.x, bombe.y
                if x == _x and y == _y:
                    bombe.Raccrourci_Delais_Explosion()
                    
    def Detection_Collision_Avec_Bombes(self, joueur):
        for bombe in self.LISTE:            
            objet_bombe = (((bombe.x + bombe.xD) * VAR.tailleCellule), ((bombe.y + bombe.yD) * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if FCT.Collision(joueur, objet_bombe):    
                return True
        return False
        
class CBombe:   
    class CFeu:
        def __init__(self, _x, _y):
            self.x = _x
            self.y = _y
            
            
            
                
    def __init__(self, _bombes, _x, _y, _force):
        self.BOMBES = _bombes
        self.TERRAIN = _bombes.MOTEUR.TERRAIN
        
        self.delais = 3.0
        self.temps = time.time()
        self.animationId = 0
        
        self.force = _force
        
        self.x, self.y = _x, _y
        self.xD, self.yD = 0.0, 0.0

        self.etat = "VA EXPLOSER"
    
    
    
    
    def Afficher(self):       
                
        if self.etat == "VA EXPLOSER":
            posX = VAR.offSet[0] + ((self.x + self.xD) * VAR.tailleCellule) 
            posY = VAR.offSet[1] + ((self.y + self.yD) * VAR.tailleCellule)     
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
        self.FOYER.append(CBombe.CFeu(self.x, self.y))         
        self.initialiser = False
        self.etat = "EXPLOSE"
    
    def Raccrourci_Delais_Explosion(self):
        self.delais = 0.05
        self.temps = time.time()
        

          
    def Gestion_Explosion(self):
        if not self.initialiser:
            feuSTOP = {"DROITE" : True, "GAUCHE" : True, "HAUT" : True, "BAS" : True}
            feuSTOP_nb = {"DROITE" : 0, "GAUCHE" : 0, "HAUT" : 0, "BAS" : 0}
            
            grille = self.TERRAIN.GRILLE            
            for force in range(1, self.force):
                for sens, xD, yD in (("DROITE", -force, 0), ("GAUCHE", force, 0), ("HAUT", 0, -force), ("BAS", 0, force)):
                    if (self.x + xD) >=0 and (self.x + xD) < VAR.nbColonnes and (self.y + yD) >=0 and (self.y + yD) < VAR.nbLignes:
                        feuSTOP[sens] = (grille[self.x+xD][self.y+yD].Traversable() and feuSTOP[sens])                    
                        self.BOMBES.Explosion_En_Chaine(self.x+xD, self.y+yD)
                        
                        if feuSTOP[sens]: 
                            self.FOYER.append(CBombe.CFeu(self.x+xD, self.y+yD))
                            feuSTOP_nb[sens] = force
                            
                        elif feuSTOP_nb[sens]+1 == force:
                            if grille[self.x+xD][self.y+yD].Cassable():
                                grille[self.x+xD][self.y+yD].Casser_Mur()

            self.initialiser = True
            
        else:
            if time.time() - self.temps > 0.10:
                self.temps = time.time()      
                self.animationId += 1
                
            if self.animationId > 5:
                self.etat = "A EXPLOSE"
                
                
            
                
                