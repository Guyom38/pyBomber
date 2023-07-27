import variables as VAR
import random

from Classes.cellule import *


                
class CTerrain():       
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.Initialiser()
        
        
        
        
    def Initialiser(self):
        self.GRILLE =  [[CCellule(self.MOTEUR, x, y) for y in range(VAR.nbLignes)] for x in range(VAR.nbColonnes)]
        self.Construire_Terrain_De_Jeu()
        
        
        
        
    def Construire_Terrain_De_Jeu(self):
        
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):
                mur = VAR.C_SOL
                if (random.randint(0, 100) < VAR.tauxRemplissage) : mur = VAR.C_CASSABLE
                
                if x in (0, VAR.nbColonnes-1): mur = VAR.C_MUR  
                if y in (0, VAR.nbLignes-1): mur = VAR.C_MUR
                if x % 2 == 0 and y % 2 == 0: mur = VAR.C_MUR             
                
                self.GRILLE[x][y].objet = mur
                
                
                
                
    def Libere_Zone(self, _x, _y, _nb):
        for y in range(-_nb, _nb+1):
            for x in range(-_nb, _nb+1):    
                xPos = _x + x
                yPos = _y + y 
                if (0 <= xPos < VAR.nbColonnes) and (0 <= yPos < VAR.nbLignes):
                    if self.GRILLE[xPos][yPos].objet == VAR.C_CASSABLE:
                        self.GRILLE[xPos][yPos].objet = VAR.C_SOL
                   
                   
                   
                    
    def Afficher(self):
        # --- affiche première couche, le sol !
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes): 
                self.GRILLE[x][y].Afficher("SOL")
        
        # --- affiche couches suivantes, murs ...      
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):               
                self.GRILLE[x][y].Afficher("DECORS")
                          
    