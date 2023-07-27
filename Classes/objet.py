import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT
import time, random

class CObjets:    
    def __init__(self, _moteur):        
        self.MOTEUR = _moteur
        self.LISTE = []
        self.PIOCHES = []
        
        self.Generer_Liste_Objets()
    
    def Generer_Liste_Objets(self):
        for _ in range(10): self.PIOCHES.append(VAR.C_OBJ_BOMBE)
        for _ in range(10): self.PIOCHES.append(VAR.C_OBJ_FLAMME)
        for _ in range(5): self.PIOCHES.append(VAR.C_OBJ_ROLLER)
        for _ in range(2): self.PIOCHES.append(VAR.C_OBJ_COUP)
        for _ in range(10): self.PIOCHES.append(None)            
        random.shuffle(self.PIOCHES)        
            
    def Afficher_Tous_Les_Objets(self):
        for objet in self.LISTE:
            objet.Afficher()
            
    def Ajouter_Ou_Pas_Un_Objet(self, _x, _y):          
        objet_hasard = self.PIOCHES.pop(0)  
        if not (objet_hasard == None):
            self.LISTE.append(CObjet(self, _x, _y, objet_hasard))
    
    def Detection_Collision_Avec_Objets(self, joueur):
        for objet in self.LISTE:            
            objet_objet = ((objet.x * VAR.tailleCellule), (objet.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
            
            if FCT.Collision(joueur, objet_objet):    
                return objet
        return None
    
    def Detruire_Objet(self, _objet):
        self.LISTE.remove(_objet)
            
class CObjet:  
    def __init__(self, _objets, _x, _y, _objet_hasard):
        self.OBJETS = _objets
        self.MOTEUR = _objets.MOTEUR
        
        self.x, self.y = _x, _y
        self.objet = _objet_hasard
    
    def Afficher(self):
        posX = int(VAR.offSet[0] + (self.x * VAR.tailleCellule)) 
        posY = int(VAR.offSet[1] + (self.y * VAR.tailleCellule))         
           
        animationId = int((time.time()*10) % 3)
        VAR.fenetre.blit(FCT.image_decoupe(VAR.image[self.objet], 0, 0, VAR.tailleCellule, VAR.tailleCellule), (posX, posY))
        
        
