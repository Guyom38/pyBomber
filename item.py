import time
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
        
    def iX(self): return int(round(self.x, 0))   
    def iY(self): return int(round(self.y, 0))