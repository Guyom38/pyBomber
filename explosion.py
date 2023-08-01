import time
import fonctions as FCT
import variables as VAR

import pygame
from pygame.locals import *

import foyer as CF
from enums import *


class CExplosion:
    def __init__(self, _bombe):
        self.BOMBE = _bombe
       
        self.BOMBES = _bombe.BOMBES
        self.MOTEUR = self.BOMBES.MOTEUR
        self.JOUEUR = _bombe.JOUEUR
        self.OBJETS = self.MOTEUR.OBJETS
        
        self.feuSTOP = {"" : True, C_DIRECTION.DROITE : True, C_DIRECTION.GAUCHE : True, C_DIRECTION.HAUT : True, C_DIRECTION.BAS : True}
        self.feuSTOP_nb = {"" : 0, C_DIRECTION.DROITE : 0, C_DIRECTION.GAUCHE : 0, C_DIRECTION.HAUT : 0, C_DIRECTION.BAS : 0}
        
        self.force = self.JOUEUR.puissance+1 

    def Initiatiser_Explosion(self):
        self.FOYER = {}
        #self.Ajoute_Schema_Explosion(self.BOMBE.iX(), self.BOMBE.iY(), 0)   
            
        self.initialiser = False
        self.BOMBE.etat = C_ETAPE_BOMBE.EXPLOSE
        self.JOUEUR.bombes_posees -= 1  
        
    def Afficher_Explosion_De_La_Bombe(self):        
        self.Gestion_Explosion()
            
        for _, foyer in self.FOYER.items():
            posX = VAR.offSet[0] + (foyer.x * VAR.tailleCellule)
            posY = VAR.offSet[1] + (foyer.y * VAR.tailleCellule)
            animationId = self.BOMBE.animationId *2
            #pygame.draw.rect(VAR.fenetre, (255,0,0), (posX+(animationId/2), posY+(animationId/2), VAR.tailleCellule-animationId, VAR.tailleCellule-animationId))  
            
            VAR.fenetre.blit(FCT.image_decoupe(VAR.image["explosion"], FCT.Animation(10, 4), foyer.imageY, VAR.tailleCellule,  VAR.tailleCellule), (posX, posY))  
        
        
    def Gestion_Explosion(self):
        if not self.initialiser:
            self.feuSTOP = {"" : True, C_DIRECTION.DROITE : True, C_DIRECTION.GAUCHE : True, C_DIRECTION.HAUT : True, C_DIRECTION.BAS : True}
            self.feuSTOP_nb = {"" : 0, C_DIRECTION.DROITE : 0, C_DIRECTION.GAUCHE : 0, C_DIRECTION.HAUT : 0, C_DIRECTION.BAS : 0}
            self.initialiser = True

            # --- ajoute la position sous le joueur
            self.Detection_KesKi_Pete(self.BOMBE.iX(), self.BOMBE.iY(), "", 0) 
            
            # --- progresse tout autour
            for force in range(1, self.force):
                for sens, xD, yD in ((C_DIRECTION.DROITE, force, 0), (C_DIRECTION.GAUCHE, -force, 0), (C_DIRECTION.HAUT, 0, -force), (C_DIRECTION.BAS, 0, force)):
                    if (self.feuSTOP[sens]):
                        posX, posY = int(round(self.BOMBE.x + xD, 0)), int(round(self.BOMBE.y + yD, 0))
                        self.Detection_KesKi_Pete(posX, posY, sens, force)             
            
            self.ReDessine_Schema()

        else:
            if time.time() - self.BOMBE.temps > 0.05:
                self.BOMBE.temps = time.time()      
                self.BOMBE.animationId += 1
                
            if self.BOMBE.animationId > 5:
                self.BOMBE.etat = C_ETAPE_BOMBE.A_EXPLOSE    

    def Detection_KesKi_Pete(self, _posX, _posY, _sens, _force):               
        grille = self.MOTEUR.TERRAIN.GRILLE               
        if FCT.Position_Sur_Terrain(_posX, _posY):
            self.feuSTOP[_sens] = (grille[_posX][_posY].Traversable() and self.feuSTOP[_sens])                    
            self.BOMBES.Explosion_En_Chaine(_posX, _posY)
                        
            if self.feuSTOP[_sens]: 
                self.Ajoute_Schema_Explosion(_posX, _posY, _force)          
                self.feuSTOP_nb[_sens] = _force
                
                # --- tue les joueurs sur la zone            
                for joueur in self.BOMBES.MOTEUR.JOUEURS.LISTE:
                    if _posX == joueur.iX() and _posY == joueur.iY():
                        joueur.Mourir()                
                # --- Detruit les objets sur la zone
                for objet in self.BOMBES.MOTEUR.OBJETS.LISTE:
                    if _posX == objet.iX() and _posY == objet.iY():
                        objet.etat = C_ETAPE_BOMBE.A_EXPLOSE                    
                            
            elif self.feuSTOP_nb[_sens]+1 == _force:
                if grille[_posX][_posY].Cassable():
                    grille[_posX][_posY].Casser_Mur()  

    def Ajoute_Schema_Explosion(self, _posX, _posY, _force):
        self.FOYER[(_posX, _posY)] = CF.CFoyer(_posX, _posY)

    
    def ReDessine_Schema(self):
        for key, values in self.FOYER.items():  
            posX, posY = key  
            gauche = (posX-1, posY) in self.FOYER 
            droite = (posX+1, posY) in self.FOYER 
            haut = (posX, posY-1) in self.FOYER 
            bas = (posX, posY+1) in self.FOYER 

            codage =  "1" if gauche else "2"
            codage += "1" if droite else "2"
            codage += "1" if haut else "2"
            codage += "1" if bas else "2"
            if codage == "1222":
                self.FOYER[key].imageY = 1
            elif codage == "2122":
                self.FOYER[key].imageY = 2
            elif codage == "2212":
                self.FOYER[key].imageY = 3
            elif codage == "2221":
                self.FOYER[key].imageY = 0
            elif codage == "1122":
                self.FOYER[key].imageY = 5
            elif codage == "2211":
                self.FOYER[key].imageY = 4
            else:
                self.FOYER[key].imageY = 6
            
            
    def Raccrourci_Delais_Explosion(self):
        self.delais = 0.00
        self.temps = time.time()