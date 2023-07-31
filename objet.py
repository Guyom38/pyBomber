import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT
import time, math

class CObjet:  
    def __init__(self, _objets, _x, _y, _objet_hasard):
        self.OBJETS = _objets
        self.MOTEUR = _objets.MOTEUR
        
        self.x, self.y = _x, _y
        self.xDest, self.yDest, self.etape = 0.0, 0.0, 0
        self.direction = "DROITE"
        self.animationTemps = time.time()
        self.etat = "A EXPLOS"
        
        self.objet = _objet_hasard
        self.couleur = [(255,0,0), (0, 255, 0), (0, 0, 255)]
        
    def iX(self): return int(round(self.x, 0))   
    def iY(self): return int(round(self.y, 0))
    
    def Afficher(self):
        self.Gestion_Rebonds()
        
        posX = int(VAR.offSet[0] + (self.x * VAR.tailleCellule)) 
        posY = int(VAR.offSet[1] + (self.y * VAR.tailleCellule))         

        VAR.fenetre.blit(FCT.image_decoupe(VAR.image[self.objet], 0, 0, VAR.tailleCellule, VAR.tailleCellule), (posX, posY))
        pygame.draw.rect(VAR.fenetre, self.couleur[FCT.Animation(10, 3)], (posX, posY, VAR.tailleCellule, VAR.tailleCellule), VAR.zoom)
    
    def Objet_Present_Sur_Place(self, _x, _y):
        for objet in self.OBJETS.LISTE:
            if objet != self:
                if int(round(objet.x, 0)) == _x and int(round(objet.y, 0)) == _y:
                    return True
        return False
    
    
    def Gestion_Rebonds(self):
        if (self.xDest, self.yDest) == (0.0, 0.0) or self.direction == "": return
        
        if (time.time() - self.animationTemps > 0.05):
            self.animationTemps = time.time()
            pret_A_Etre_Place = False
            self.etape += 1
            amplitude = 0.4
            
            if self.direction == "GAUCHE":                
                self.x -= 0.2                
                self.y += math.cos(self.etape) * amplitude                 
                if self.x < 0.0: self.x, self.xDest = VAR.nbColonnes+1, VAR.nbColonnes -1
                if self.x < self.xDest: pret_A_Etre_Place = True
                
            elif self.direction == "DROITE":
                self.x += 0.2                
                self.y += math.cos(self.etape) * amplitude                  
                if self.x > VAR.nbColonnes+1: self.x, self.xDest = 0.0, 0.0
                if self.x > self.xDest: pret_A_Etre_Place = True

            elif self.direction == "HAUT":
                self.y -= 0.2                
                self.x += math.cos(self.etape) * amplitude                  
                if self.y < 0.0: self.y, self.yDest = VAR.nbLignes+1, VAR.nbLignes -1                        
                if self.y < self.yDest: pret_A_Etre_Place = True               
            
            elif self.direction == "BAS":
                self.y += 0.2                
                self.x += math.cos(self.etape) * amplitude                  
                if self.y > VAR.nbLignes+1 : self.y, self.yDest = 0.0, 0.0                          
                if self.y > self.yDest: pret_A_Etre_Place = True  
                               
            if pret_A_Etre_Place:
                posX, posY = int(round(self.x, 0)), int(round(self.y, 0))  
                
                if 0 <= posX < VAR.nbColonnes and 0 <= posY < VAR.nbLignes:
                    deja_Occupe = self.Objet_Present_Sur_Place(posX, posY)    
                    zone_Libre = (self.MOTEUR.TERRAIN.GRILLE[posX][posY].objet == VAR.C_SOL)   
                        
                    if not deja_Occupe and zone_Libre:
                        self.x, self.y = posX, posY
                        self.xDest, self.yDest,self.direction = 0.0, 0.0, ""

