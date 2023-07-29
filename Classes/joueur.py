import pygame
from pygame.locals import *
import variables as VAR
import fonctions as FCT

from Classes.moteur import *
from Classes.bombe import *

from random import *

import time
import pygame.mixer

class CJoueurs():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.LISTE = []
        
        self.joueurs_EnVie  = 0
        
    def Afficher_Tous_Les_Joueurs(self):
        # --- retri les joueurs pour que si un joueur s'affiche devant l'autre, il soit afficher apres
        liste_joueurs_tries = sorted(self.LISTE, key=lambda joueur: joueur.y)
        self.joueurs_EnVie = 0
        
        for joueur in liste_joueurs_tries:
            joueur.Afficher() 
            
            if joueur.mort: self.joueurs_EnVie += 1
            
class CJoueur():
    
    def __init__(self, _moteur, _id, _pseudo):         
        self.MOTEUR = _moteur     
                 
        self.id = _id
        self.pseudo = _pseudo
        self.couleur = (255,255,255,255)
        
        self.animationId = 0
        self.temps = time.time()
        
        self.Initialiser()
        
        self.image = VAR.image["joueur0"].copy()        
        self.Colorisation()
        
    def Colorisation(self):
        if self.id == 0: return
        
        C_COLOR_TRANSPARENT = (255, 255, 255, 0)
        self.couleur = VAR.LISTE_COLOR['(232, 232, 232, 255)'][self.id]
        
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                couleur = self.image.get_at((x, y))
                if not C_COLOR_TRANSPARENT == couleur:
                    if str(couleur) in VAR.LISTE_COLOR:
                        self.image.set_at((x,y), VAR.LISTE_COLOR[str(couleur)][self.id])   
    
    def Position_Initiale(self):
        if self.id == 0:            return (1.0, 1.0)             
        if self.id == 1:            return (VAR.nbColonnes-2, VAR.nbLignes-2)
        if self.id == 2:            return (1.0, VAR.nbLignes-2)
        if self.id == 3:            return (VAR.nbColonnes-2, 1.0)
        if self.id == 4:            return (round(VAR.nbColonnes/2,0), round(VAR.nbLignes/2,0))
        
        if self.id == 5:            return (round(VAR.nbColonnes/2,0), 1.0)
        if self.id == 6:            return (1.0, round(VAR.nbLignes/2,0))
        if self.id == 7:            return (VAR.nbColonnes-2, round(VAR.nbLignes/2,0))
        if self.id == 8:            return (round(VAR.nbColonnes/2,0), VAR.nbLignes-2)
        
    def Initialiser(self):        
        self.x, self.y = self.Position_Initiale()
        if self.x % 2 == 0: self.x -=1
        if self.y % 2 == 0: self.y -=1
        
        self.direction = "BAS"
        self.enMouvement = False
        
        self.vitesseBase = 0.10
        self.vitesse = self.vitesseBase
        self.pasVitesse = 0.005
        
        self.puissance = 1
        self.bombes = 1
        self.bombes_posees = 0
        self.bombes_protection = None
        
        self.coup_de_point = False
        self.mort = False
        self.MOTEUR.TERRAIN.Libere_Zone(self.iX(), self.iY(), 2)    
        
        self.offSetX = 0
        self.offSetY = - 12 * VAR.zoom
        
    def iX(self): return int(round(self.x, 0) )   
    def iY(self): return int(round(self.y, 0))
         
        
    def direction_y_image(self):
        if self.direction == "BAS": return 1
        if self.direction == "HAUT": return 3
        if self.direction == "DROITE": return 4
        if self.direction == "GAUCHE": return 2      
        
        
          
    
    
    def Afficher(self):
        posX = VAR.offSet[0] + self.offSetX + (self.x * VAR.tailleCellule) 
        posY = VAR.offSet[1] + self.offSetY + (self.y * VAR.tailleCellule)      
            
        if self.mort == False: 
            if (self.enMouvement):
                animationId = int((time.time()*10) % 3)
            else:
                animationId = 0
                
            VAR.fenetre.blit(FCT.image_decoupe(self.image,  animationId, self.direction_y_image(), VAR.tailleCellule, VAR.tailleCellule*2), (posX, posY))

            self.Gestion_Deplacement()  
            self.Detection_Collision_Decors()    
        
        elif self.animationId >= 0:
            if self.animationId < VAR.animation_MortFrameMax+1:
                if time.time() - self.temps > 0.20:
                    self.temps = time.time()
                    self.animationId +=1
                    
                VAR.fenetre.blit(FCT.image_decoupe(self.image,  self.animationId, 5, VAR.tailleCellule, VAR.tailleCellule*2), (posX, posY))
                
            else:
                self.Transmission_Heritage_Apres_Mort()
                self.animationId = -1
                
    def Mourir(self):
        # --- active l'animation de la mort
        self.mort = True
        
        
    def Transmission_Heritage_Apres_Mort(self):
        # --- jete les objets
        for _ in range(self.bombes-1):
            if randint(0,100) <25: self.MOTEUR.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_BOMBE, True)
        
        for _ in range(self.puissance-1):
            if randint(0, 100) <15: self.MOTEUR.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_FLAMME, True)
        
        nbVitesse = int(round((self.vitesse-self.vitesseBase) / self.pasVitesse,0))
        for _ in range(nbVitesse):
            if randint(0, 100) <15: self.MOTEUR.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_ROLLER, True)
        
        
    def Poser_Une_Bombe(self):
        if self.bombes_posees < self.bombes:
            self.MOTEUR.BOMBES.Ajouter(self)    
            FCT.jouer_sons("poser_bombe")
        
    def Retire_Protection_Bombe_Si_A_Cote(self):
        if self.bombes_protection == None: return
        if not(self.bombes_protection.iX() == self.iX() and self.bombes_protection.iY() == self.iY()):            
            self.bombes_protection = None
            
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return 
        
        # --- mouvement en fonction de la direction
        if self.direction == "HAUT":   self.y -= self.vitesse
        if self.direction == "BAS":    self.y += self.vitesse
        if self.direction == "GAUCHE": self.x -= self.vitesse
        if self.direction == "DROITE": self.x += self.vitesse        

        posX = VAR.offSet[0] + self.offSetX + (self.x * VAR.tailleCellule)  + (VAR.tailleCellule / 2)
        posY = VAR.offSet[1] + self.offSetY + (self.y * VAR.tailleCellule)  + (VAR.tailleCellule / 2)             
        self.MOTEUR.PARTICULES.Ajouter(posX, posY, self.couleur)
        
        # --- controle si collision
        coord_collision = self.Detection_Collision_Decors()
        if not coord_collision == VAR.C_AUCUNE_COLLISION:
            # --- repositionne parfaitement la position du joueur sur la case qu'il occupe
            if self.direction in ["HAUT","BAS"]: self.y = round(self.y, 0)
            if self.direction in ["GAUCHE","DROITE"]: self.x = round(self.x, 0)
            
            if not coord_collision == VAR.C_HORS_TERRAIN:  
                self.Algorithme_Drift(coord_collision)  
        
        self.Retire_Protection_Bombe_Si_A_Cote()
        self.Detection_Collision_Objets()            
        self.enMouvement = False             
        
        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    def Zone_Traversable(self, gX, gY):
        return (self.MOTEUR.TERRAIN.GRILLE[gX][gY].Traversable())
    
    
    def Detection_Collision_Objets(self):
        joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        objet_attrape = self.MOTEUR.OBJETS.Detection_Collision_Avec_Objets(joueur)
        if not (objet_attrape == None):
            if (objet_attrape.objet == VAR.C_OBJ_BOMBE): self.bombes += 1
            if (objet_attrape.objet == VAR.C_OBJ_FLAMME): self.puissance += 1
           # if (objet_attrape.objet == VAR.C_OBJ_COUP): self.bombes += 1
            if (objet_attrape.objet == VAR.C_OBJ_ROLLER): self.vitesse += self.pasVitesse
            self.MOTEUR.OBJETS.Detruire_Objet(objet_attrape)
            FCT.jouer_sons("prendre_objet")
    
    def Detection_Collision_Bombes(self):        
        return self.MOTEUR.BOMBES.Detection_Collision_Avec_Bombes(self)
        
                    
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        
        if pX == -1 and pY == -1: 
            joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        else:
            joueur = ((pX * VAR.tailleCellule), (pY * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        
        collision = VAR.C_AUCUNE_COLLISION
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            x, y = coord                
            gX, gY = self.iX() + x, self.iY() + y
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    
                    pygame.draw.rect(VAR.fenetre, (128,255,0,0), ((x+2) * 16, (y+2 + (self.id*4)) * 16, 16-1, 16-1))
                    decors = ((gX) * VAR.tailleCellule, (gY) * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)                
                    
                    if FCT.Collision(joueur, decors): 
                        return (gX, gY)
                    
                    if self.Detection_Collision_Bombes():
                        print("BOMBE")
                        return (gX, gY)
            else:
                pygame.draw.rect(VAR.fenetre, (64,255,255,0), ((x+2) * 16, (y+2+ (self.id*4)) * 16, 16-1, 16-1))
                collision = VAR.C_HORS_TERRAIN
                break
        
        pX = self.x - round(self.x, 0)
        pY = self.y - round(self.y, 0)
        pygame.draw.rect(VAR.fenetre, (128,0,255,0), (int((2+pX)*16), int((2+pY+ (self.id*4))*16), 16-1, 16-1))  
        
        return collision



    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        xOld, yOld = self.x, self.y
        xCollision, yCollision = _collision_coord
        
        limit = 0.5
        limitx2 = limit *2
        
        # --- Test le Passage a empreinter pour contourner
        if d == "DROITE": cellule_Sur_Chemin = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        if d == "GAUCHE": cellule_Sur_Chemin = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision-1].Traversable())      
        if d == "HAUT": cellule_Sur_Chemin = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision+1].Traversable())      
        if d == "BAS": cellule_Sur_Chemin = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        
        # --- Test le passage final
        if d in ["DROITE","GAUCHE"]:                      
            # --- Passage au dessus            
            if  (yCollision-limitx2) <= self.y <= (yCollision-limit): 
                cellule_Destination = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision-1].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.y -= self.vitesseBase  
                    
            # --- Passage au dessous
            elif (yCollision+limit ) <= self.y <= (yCollision+limitx2):
                cellule_Destination = (self.MOTEUR.TERRAIN.GRILLE[xCollision][yCollision+1].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.y += self.vitesseBase

        if d in ["HAUT","BAS"]:     
            # --- Passage au droite
            if (xCollision-limitx2) <= self.x <= (xCollision-limit): 
                cellule_Destination = (self.MOTEUR.TERRAIN.GRILLE[xCollision-1][yCollision].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.x -= self.vitesseBase
                    
            # --- Passage au gauche
            elif (xCollision+limit ) <= self.x <= (xCollision + limitx2):
                cellule_Destination = (self.MOTEUR.TERRAIN.GRILLE[xCollision+1][yCollision].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.x += self.vitesseBase
        
        # --- Ajustement du mouvement
        if not (yOld == self.y):
            if self.y-round(self.y,0) < self.vitesseBase: self.y = round(self.y, 0)
        if not (xOld == self.x):
            if self.x-round(self.x,0) < self.vitesseBase: self.x = round(self.x, 0)