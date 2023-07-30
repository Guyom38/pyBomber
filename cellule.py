import variables as VAR
import time

class CCellule():
    def __init__(self, _moteur, _x, _y):
        self.MOTEUR = _moteur  
             
        self.objet = VAR.C_SOL   
        self.x, self.y = _x, _y
        
        self.animationId = 0
        self.temps = time.time()
        self.casser = False
        
        
    def Traversable(self):
        return (self.objet == VAR.C_SOL)
    
    def Cassable(self):
        return (self.objet == VAR.C_CASSABLE)
    
    def Casser_Mur(self):
        self.temps = time.time()
        self.animationId = 0
        self.casser = True
        
    def Animation_Explosion_Mur(self):
        posX = VAR.offSet[0] + (self.x * VAR.tailleCellule)  + (VAR.tailleCellule / 2)
        posY = VAR.offSet[1] + (self.y * VAR.tailleCellule)  + (VAR.tailleCellule / 2)             
        self.MOTEUR.PARTICULES.Ajouter(posX, posY, (64,64,64,255))
        
        if time.time() - self.temps > 0.1:
            self.animationId += 1
            self.temps = time.time() 
            
        if self.animationId > 1:
            self.objet = VAR.C_SOL    
            self.MOTEUR.OBJETS.Ajouter_Ou_Pas_Un_Objet(self.x, self.y)
            
    def Afficher(self, _couche):
        posX = VAR.offSet[0] + (self.x * VAR.tailleCellule)
        posY = VAR.offSet[1] + (self.y * VAR.tailleCellule)
        
        if _couche == "SOL":
            self.Afficher_Sol(posX, posY)            
        else:
            self.Afficher_Mur(posX, posY)
                        
    
    def Afficher_Sol(self, _posX, _posY):
        i = int((_posY * VAR.nbLignes) + _posX)            
        if self.objet == VAR.C_SOL: 
            if not (self.MOTEUR.TERRAIN.GRILLE[self.x][self.y-1].objet == VAR.C_SOL):
                VAR.fenetre.blit(VAR.image["ombre"], (_posX, _posY))
            else:
                VAR.fenetre.blit(VAR.image["sol"+str(i % 2)], (_posX, _posY))
                
    def Afficher_Mur(self, _posX, _posY):
        if self.objet == VAR.C_MUR: 
            VAR.fenetre.blit(VAR.image["mur"], (_posX, _posY))
                
        elif self.objet == VAR.C_CASSABLE: 
            if not self.casser:
                VAR.fenetre.blit(VAR.image["cassable"], (_posX, _posY))    
            else:
                VAR.fenetre.blit(VAR.image["cassable"+str(self.animationId)], (_posX, _posY)) 
                self.Animation_Explosion_Mur() 
                
                