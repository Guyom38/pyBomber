import pygame
from pygame.locals import *
import pygame.mixer

import variables as VAR
import fonctions as FCT

import time, random
from enum import Enum  

class CJoueur():
    
    def __init__(self, _moteur, _id, _pseudo):         
        self.MOTEUR = _moteur  
        self.JOUEURS = _moteur.JOUEURS    
        self.OBJETS = _moteur.OBJETS 
          
        self.id = _id
        self.pseudo = _pseudo
        self.couleur = (255,255,255,255)
        
        self.animationId = 0
        self.temps = time.time()
        
        self.Initialiser()
        
        self.image = VAR.image["joueur0"].copy() 
            
        self.Colorisation()

    def iX(self): return int(round(self.x, 0))   
    def iY(self): return int(round(self.y, 0))
    def estMalade(self): return not (self.maladie == 0)
    
                        
    def Colorisation(self):
        if self.id == 0: return
        
        self.couleur = VAR.LISTE_COLOR['(232, 232, 232, 255)'][self.id]
        
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                couleur = self.image.get_at((x, y))
                if not VAR.C_COLOR_TRANSPARENT == couleur:
                    if str(couleur) in VAR.LISTE_COLOR:
                        self.image.set_at((x,y), VAR.LISTE_COLOR[str(couleur)][self.id])   
    
    def Position_Initiale(self):
        if self.id == 0:            x, y = (1.0, 1.0)             
        if self.id == 1:            x, y = (VAR.nbColonnes-2, VAR.nbLignes-2)
        if self.id == 2:            x, y = (1.0, VAR.nbLignes-2)
        if self.id == 3:            x, y = (VAR.nbColonnes-2, 1.0)
        if self.id == 4:            x, y = (round(VAR.nbColonnes/2,0), round(VAR.nbLignes/2,0))        
        if self.id == 5:            x, y = (round(VAR.nbColonnes/2,0), 1.0)
        if self.id == 6:            x, y = (1.0, round(VAR.nbLignes/2,0))
        if self.id == 7:            x, y = (VAR.nbColonnes-2, round(VAR.nbLignes/2,0))
        if self.id == 8:            x, y = (round(VAR.nbColonnes/2,0), VAR.nbLignes-2)
        
        if x % 2 == 0: x -=1
        if y % 2 == 0: y -=1
        
        return (x, y)
    
    def Initialiser(self):        
        self.x, self.y = self.Position_Initiale()        
        
        self.direction = "BAS"
        self.enMouvement = False
        
        self.vitesseBase = 0.06
        self.vitesse = self.vitesseBase
        self.pasVitesse = 0.005
        
        self.puissance = 1
        self.bombes = 2
        self.bombes_posees = 0
        self.bombes_protection = None
        
        self.coup_de_pied = False
        self.coup_de_poing = False
        self.maladie = 0
        self.maladie_Temps_fige = -1
        
        self.mort = False
        self.MOTEUR.TERRAIN.Libere_Zone(self.iX(), self.iY(), 2)    
        
        self.offSetX = 0
        self.offSetY = - 12 * VAR.zoom
        

         
        
    def direction_y_image(self):
        if self.direction == "BAS": return 1
        if self.direction == "HAUT": return 3
        if self.direction == "DROITE": return 4
        if self.direction == "GAUCHE": return 2      
        
        
          
    
    
    def Afficher(self):
        posX = VAR.offSet[0] + self.offSetX + (self.x * VAR.tailleCellule) 
        posY = VAR.offSet[1] + self.offSetY + (self.y * VAR.tailleCellule)      
            
        if not self.mort: 
            if (self.enMouvement):
                animationId = FCT.Animation(10, 3)
            else:
                animationId = 0
            
            if self.estMalade() and FCT.Animation(10, 2) == 0:
                image = self.JOUEURS.image_masque                
            else:   
                image = self.image
                
            VAR.fenetre.blit(FCT.image_decoupe(image,  animationId, self.direction_y_image(), VAR.tailleCellule, VAR.tailleCellule*2), (posX, posY))

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
            if random.randint(0,100) <25: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_BOMBE, True)
        
        for _ in range(self.puissance-1):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_FLAMME, True)
        
        nbVitesse = int(round((self.vitesse-self.vitesseBase) / self.pasVitesse,0))
        for _ in range(nbVitesse):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_ROLLER, True)
        
        
    def Action_Poser_Une_Bombe(self):
        if self.bombes_posees < self.bombes:
            self.MOTEUR.BOMBES.Ajouter(self)    
            FCT.jouer_sons("poser_bombe")
    

    def Retire_Protection_Bombe_Si_A_Cote(self):
        if self.bombes_protection == None: return
        
        if not self.MOTEUR.BOMBES.Detection_Collision_Avec_Une_Bombe(self, self.bombes_protection):
            self.bombes_protection = None
 
            
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return 
        
        vitesseDeBase = self.vitesse
        if self.maladie == VAR.C_MALADIE.RALENTISSEMENT: vitesseDeBase = 0.01
        if self.maladie == VAR.C_MALADIE.FIGER:
            if self.maladie_Temps_fige == -1: self.maladie_Temps_fige = time.time()
            if time.time() - self.maladie_Temps_fige < VAR.delaisExplosion + 1:
                return 
            else:
                self.Se_Soigne()
                

        # --- mouvement en fonction de la direction
        if self.direction == "HAUT":   self.y -= vitesseDeBase
        if self.direction == "BAS":    self.y += vitesseDeBase
        if self.direction == "GAUCHE": self.x -= vitesseDeBase
        if self.direction == "DROITE": self.x += vitesseDeBase        

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
    
    
    def Attrape_Objet(self, _objet_attrape):
        
        # --- Si malade se debarrasse de sa maladie
        if self.estMalade():
            self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), VAR.C_OBJ_MALADIE, True, 4, 4)
            self.Se_Soigne()
        
        # --- Prend le nouvel objet    
        if (_objet_attrape.objet == VAR.C_OBJ_BOMBE): self.bombes += 1
        if (_objet_attrape.objet == VAR.C_OBJ_FLAMME): self.puissance += 1
        if (_objet_attrape.objet == VAR.C_OBJ_SUPER_FLAMME): self.puissance += 5
        if (_objet_attrape.objet == VAR.C_OBJ_COUP_PIED): self.coup_de_pied = True
        if (_objet_attrape.objet == VAR.C_OBJ_COUP_POING): self.coup_de_poing = True
        if (_objet_attrape.objet == VAR.C_OBJ_ROLLER): self.vitesse += self.pasVitesse
        if (_objet_attrape.objet == VAR.C_OBJ_MALADIE): self.Tombe_Malade()

        # --- Detruit l'objet a l'écran
        self.MOTEUR.OBJETS.Detruire_Objet(_objet_attrape)
        FCT.jouer_sons("prendre_objet")
            
        
    def Detection_Collision_Objets(self):
        joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        objet_attrape = self.OBJETS.Detection_Collision_Avec_Objets(joueur)
        
        if not (objet_attrape == None):     
            if not objet_attrape.enMouvement:
                self.Attrape_Objet(objet_attrape)
        
            
    def Se_Soigne(self):
        self.maladie = 0
        self.maladie_Temps_fige == -1
           
    def Tombe_Malade(self):
        self.maladie = random.choices(list(VAR.C_MALADIE))[0]
        print(self.maladie)
        
                   
    def Detection_Collision_Decors(self, pX=-1, pY=-1):
        
        #if pX == -1 and pY == -1: 
        joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        #else:
        #    joueur = ((pX * VAR.tailleCellule), (pY * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        
        collision = VAR.C_AUCUNE_COLLISION
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            x, y = coord                
            gX, gY = self.iX() + x, self.iY() + y
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    
                    #pygame.draw.rect(VAR.fenetre, (128,255,0,0), ((x+2) * 16, (y+2 + (self.id*4)) * 16, 16-1, 16-1))
                    
                    decors = (gX * VAR.tailleCellule, gY * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)
                    if FCT.Collision(joueur, decors): return (gX, gY)
                    if self.MOTEUR.BOMBES.Detection_Collision_Avec_Les_Bombes(self): return (gX, gY)
            else:
                #pygame.draw.rect(VAR.fenetre, (64,255,255,0), ((x+2) * 16, (y+2+ (self.id*4)) * 16, 16-1, 16-1))
                collision = VAR.C_HORS_TERRAIN
                break
        
        #pX = self.x - round(self.x, 0)
        #pY = self.y - round(self.y, 0)
        #pygame.draw.rect(VAR.fenetre, (128,0,255,0), (int((2+pX)*16), int((2+pY+ (self.id*4))*16), 16-1, 16-1))  
        
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