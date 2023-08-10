import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT
import time, math
import item

from enums import *

class CObjet(item.CItem):  
    def __init__(self, _moteur, _x, _y, _objet_hasard):
        super().__init__(_moteur, _x, _y, "")    
        

        self.xDest, self.yDest, self.etape = 0.0, 0.0, 0           
        self.objet = _objet_hasard
        self.couleur = [(255,0,0), (0, 255, 0), (0, 0, 255)]
            
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
        if not self.enMouvement: return
        
        if (time.time() - self.temps > 0.05):
            self.temps = time.time()
            pret_A_Etre_Place = False
            self.etape += 1
            amplitude = 0.4
            
            if self.direction == C_DIRECTION.GAUCHE:                
                self.x -= 0.2                
                self.y += math.cos(self.etape) * amplitude                 
                if self.x < 0.0: self.x, self.xDest = VAR.nbColonnes+1, VAR.nbColonnes -1
                if self.x < self.xDest: pret_A_Etre_Place = True
                
            elif self.direction == C_DIRECTION.DROITE:
                self.x += 0.2                
                self.y += math.cos(self.etape) * amplitude                  
                if self.x > VAR.nbColonnes+1: self.x, self.xDest = 0.0, 0.0
                if self.x > self.xDest: pret_A_Etre_Place = True

            elif self.direction == C_DIRECTION.HAUT:
                self.y -= 0.2                
                self.x += math.cos(self.etape) * amplitude                  
                if self.y < 0.0: self.y, self.yDest = VAR.nbLignes+1, VAR.nbLignes -1                        
                if self.y < self.yDest: pret_A_Etre_Place = True               
            
            elif self.direction == C_DIRECTION.BAS:
                self.y += 0.2                
                self.x += math.cos(self.etape) * amplitude                  
                if self.y > VAR.nbLignes+1 : self.y, self.yDest = 0.0, 0.0                          
                if self.y > self.yDest: pret_A_Etre_Place = True  
                               
            if pret_A_Etre_Place:
                posX, posY = self.celluleX(), self.celluleY()  
                
                if 0 <= posX < VAR.nbColonnes and 0 <= posY < VAR.nbLignes:
                    deja_Occupe = self.Objet_Present_Sur_Place(posX, posY)    
                    zone_Libre = (self.TERRAIN.GRILLE[posX][posY].objet == C_TERRAIN.SOL)   
                        
                    if not deja_Occupe and zone_Libre:
                        self.x, self.y = posX, posY
                        self.enMouvement = False

