import variables as VAR
import random




class CTerrain():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.Initialiser()
        
        
        
        
    def Initialiser(self):
        self.GRILLE =  [[0 for _ in range(VAR.nbLignes)] for _ in range(VAR.nbColonnes)]
        self.Construire_Terrain_De_Jeu()
        
        
        
        
    def Construire_Terrain_De_Jeu(self):
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):
                mur = VAR.C_SOL
                if (random.randint(0, 100) > VAR.tauxRemplissage) : mur = VAR.C_CASSABLE
                
                if x in (0, VAR.nbColonnes-1): mur = VAR.C_MUR  
                if y in (0, VAR.nbLignes-1): mur = VAR.C_MUR
                if x % 2 == 0 and y % 2 == 0: mur = VAR.C_MUR             
                
                self.GRILLE[x][y] = mur
                
                
                
                
    def Libere_Zone(self, _x, _y, _nb):
        for y in range(-_nb, _nb+1):
            for x in range(-_nb, _nb+1):    
                xPos = _x + x
                yPos = _y + y  
                if self.MOTEUR.TERRAIN.GRILLE[xPos][yPos] > VAR.C_MUR:
                    self.MOTEUR.TERRAIN.GRILLE[xPos][yPos] = VAR.C_SOL
                   
                   
                   
                    
    def Afficher(self):
        i=0
        
        # --- affiche première couche, le sol !
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):               

                posX = VAR.offSet[0] + (x * VAR.tailleCellule)
                posY = VAR.offSet[1] + (y * VAR.tailleCellule)
                
                cellule = self.GRILLE[x][y]
                if cellule == VAR.C_SOL: VAR.fenetre.blit(VAR.image["sol"+str(i % 2)], (posX, posY))
                i+=1
        
        # --- affiche couches suivantes, murs ...      
        for y in range(VAR.nbLignes):
            for x in range(VAR.nbColonnes):               

                posX = VAR.offSet[0] + (x * VAR.tailleCellule)
                posY = VAR.offSet[1] + (y * VAR.tailleCellule)
                
                cellule = self.GRILLE[x][y]
                if cellule == VAR.C_MUR: VAR.fenetre.blit(VAR.image["mur"], (posX, posY))
                if cellule == VAR.C_CASSABLE: VAR.fenetre.blit(VAR.image["cassable"], (posX, posY))              
    