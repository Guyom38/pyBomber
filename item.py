import time

import variables as VAR
import fonctions as FCT
from enums import *

class CItem:
    def __init__(self, _moteur, _x = 0.0, _y = 0.0, _etat = ""):     
        self.MOTEUR = _moteur
        self.TERRAIN = self.MOTEUR.TERRAIN
        self.JOUEURS = self.MOTEUR.JOUEURS
        self.BOMBES = self.MOTEUR.BOMBES
        self.OBJETS = self.MOTEUR.OBJETS
           
        self.x, self.y = _x, _y
        self.etat = _etat
        
        self.enMouvement = False
        self.direction = C_DIRECTION.DROITE
        
        self.animationId = 0
        self.temps = time.time()
        
        self.offSetX, self.offSetY = 0, 0
        
    def celluleX(self): return int(round(self.x, 0))   
    def celluleY(self): return int(round(self.y, 0))
    
    def ecranX(self): return VAR.offSet[0] + self.offSetX + (self.x * VAR.tailleCellule) 
    def ecranY(self): return VAR.offSet[1] + self.offSetY + (self.y * VAR.tailleCellule) 
    
    def toujours_Sur_Le_Terrain(self, x, y): return (x >= 0 and y >=0 and x < VAR.nbColonnes and y < VAR.nbLignes) 
    def zone_Traversable(self, gX, gY): return (self.TERRAIN.GRILLE[gX][gY].traversable())   
     
    def Detection_Collision_Murs_Autour(self):        
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            xDecalage, yDecalage = coord                
            murX, murY = self.celluleX() + xDecalage, self.celluleY() + yDecalage
            
            if self.toujours_Sur_Le_Terrain(murX, murY):
                if not self.zone_Traversable(murX, murY):
                    if FCT.Collision2((self.x, self.y), (murX, murY)): 
                        return (murX, murY)
            else:
                return VAR.C_HORS_TERRAIN
        return VAR.C_AUCUNE_COLLISION