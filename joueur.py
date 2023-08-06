import pygame
from pygame.locals import *
import pygame.mixer

import variables as VAR
from enums import *

import fonctions as FCT

import time, random
from enum import Enum  
import item

class CJoueur(item.CItem):
    
    def __init__(self, _moteur, _id, _pseudo, _menu = False):  
        super().__init__(_moteur, 0.0, 0.0, "")      
          
        self.id = _id
        self.pseudo = _pseudo
        self.actif = True
        self.clown = False
        
        self.menu = _menu
        self.score = 0
        
        self.couleur = (255,255,255,255)        
    
        self.Initialiser(self.id)
        self.Colorisation()

    
    def estMalade(self): return not (self.maladie == 0)
    def vraimentMort(self): return (self.mort and self.animationId == -1)
    
    def Initialiser(self, _position):        
        self.x, self.y = self.Position_Initiale(_position)        
        
        self.direction = C_DIRECTION.BAS
        self.enMouvement = False
        
        self.vitesseBase = 0.06
        self.vitesse = self.vitesseBase
        self.pasVitesse = 0.005
        
        self.puissance = 1
        self.bombes = 1
        self.bombes_posees = 0
        self.bombes_protection = None
        
        self.coup_de_pied = False
        self.coup_de_poing = False
        self.maladie = 0
        self.maladie_Temps_fige = -1
        
        self.maladie_temps_touche = -1
        
        self.mort = False
        self.clown = False

        
        if not self.menu:
            self.TERRAIN.Libere_Zone(self.iX(), self.iY(), 2)    
        
        self.offSetX = 0
        self.offSetY = - 12 * VAR.zoom
        
                                
    def Colorisation(self):
        self.image = VAR.image["joueur0"].copy()      
        if self.id == 0: return
        
        self.couleur = VAR.LISTE_COLOR['(232, 232, 232, 255)'][self.id-1]
        
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                couleur = self.image.get_at((x, y))
                if not VAR.C_COLOR_TRANSPARENT == couleur:
                    if str(couleur) in VAR.LISTE_COLOR:
                        self.image.set_at((x,y), VAR.LISTE_COLOR[str(couleur)][self.id-1])   
    
    def Position_Initiale(self, _position):
        x, y = 0, 0
        
        if _position == 0 and self.actif: x, y = (1.0, 1.0)             
        if _position == 1 and self.actif: x, y = (VAR.nbColonnes-2, VAR.nbLignes-2)
        if _position == 2 and self.actif: x, y = (1.0, VAR.nbLignes-2)
        if _position == 3 and self.actif: x, y = (VAR.nbColonnes-2, 1.0)
        if _position == 4 and self.actif: x, y = (round(VAR.nbColonnes/2,0), round(VAR.nbLignes/2,0))        
        if _position == 5 and self.actif: x, y = (round(VAR.nbColonnes/2,0), 1.0)
        if _position == 6 and self.actif: x, y = (1.0, round(VAR.nbLignes/2,0))
        if _position == 7 and self.actif: x, y = (VAR.nbColonnes-2, round(VAR.nbLignes/2,0))
        if _position == 8 and self.actif: x, y = (round(VAR.nbColonnes/2,0), VAR.nbLignes-2)
        
        if x % 2 == 0: x -=1
        if y % 2 == 0: y -=1
        
        return (x, y)
    

        
    
    
    def Afficher(self, _menu = False):
        if not self.actif: return
        
        posX = VAR.offSet[0] + self.offSetX + (self.x * VAR.tailleCellule) 
        posY = VAR.offSet[1] + self.offSetY + (self.y * VAR.tailleCellule)      
        directionImage = self.direction.value
        
        if not self.mort: 
            if (self.enMouvement):
                animationId = FCT.Animation(10, 3)
            else:
                animationId = 0
            
            if self.estMalade() and FCT.Animation(10, 2) == 0:
                image = self.JOUEURS.image_masque                
            else:   
                image = self.image
                
                # --- animation lors du menu pour activer le joueur
                if self.clown: directionImage, animationId = 5, FCT.Animation(10, 3)
                
            VAR.fenetre.blit(FCT.image_decoupe(image,  animationId, directionImage, VAR.tailleCellule, VAR.tailleCellule*2), (posX, posY))

            if not _menu:
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
            if random.randint(0,100) <25: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.BOMBE, True)
        
        for _ in range(self.puissance-1):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.FLAMME, True)
        
        nbVitesse = int(round((self.vitesse-self.vitesseBase) / self.pasVitesse,0))
        for _ in range(nbVitesse):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.ROLLER, True)
        
        
    def Action_Poser_Une_Bombe(self):
        if self.bombes_posees < self.bombes:
            self.BOMBES.Ajouter(self)    
            FCT.jouer_sons("poser_bombe")
    

    def Retire_Protection_Bombe_Si_A_Cote(self):
        if self.bombes_protection == None: return
        
        if not self.BOMBES.Detection_Collision_Avec_Une_Bombe(self, self.bombes_protection):
            self.bombes_protection = None
 
            
    def Gestion_Deplacement(self):
        if self.enMouvement == False: return 
        
        vitesseDeBase = self.vitesse
        if self.maladie == C_MALADIE.RALENTISSEMENT: vitesseDeBase = 0.02
        if self.maladie == C_MALADIE.FIGER:
            if self.maladie_Temps_fige == -1: self.maladie_Temps_fige = time.time()
            if time.time() - self.maladie_Temps_fige < VAR.delaisExplosion + 1:
                return 
            else:
                self.Se_Soigne()
                

        # --- mouvement en fonction de la direction
        if self.direction == C_DIRECTION.HAUT:   self.y -= vitesseDeBase
        if self.direction == C_DIRECTION.BAS:    self.y += vitesseDeBase
        if self.direction == C_DIRECTION.GAUCHE: self.x -= vitesseDeBase
        if self.direction == C_DIRECTION.DROITE: self.x += vitesseDeBase        

        # --- controle si collision
        coord_collision = self.Detection_Collision_Decors()
        if not coord_collision == VAR.C_AUCUNE_COLLISION:
            # --- repositionne parfaitement la position du joueur sur la case qu'il occupe
            if self.direction in [C_DIRECTION.HAUT,C_DIRECTION.BAS]: self.y = self.iY()
            if self.direction in [C_DIRECTION.GAUCHE,C_DIRECTION.DROITE]: self.x = self.iX()
            
            if not coord_collision == VAR.C_HORS_TERRAIN:  
                self.Algorithme_Drift(coord_collision)  
        
        self.Retire_Protection_Bombe_Si_A_Cote()
        self.Detection_Collision_Objets()            
        self.enMouvement = False             
        
    def Detection_Collision_Avec_Autres_Joueurs(self):
        coord_joueur = (self.x, self.y, VAR.tailleCellule, VAR.tailleCellule)
        for joueur in self.JOUEURS.LISTE.items():
            if not joueur == self:
                coord_autre_joueur = (joueur.x, joueur.y, VAR.tailleCellule, VAR.tailleCellule)
                
                if FCT.Collision(coord_joueur, coord_autre_joueur):
                    if self.coup_de_poing: return True
                    if self.estMalade and (self.maladie_temps_touche == -1 or time.time() - self.maladie_temps_touche > 2):
                        joueur.maladie = self.maladie
                        self.maladie = 0
                        self.maladie_temps_touche = -1
                        joueur.maladie_temps_touche = time.time()
                
                
                
    def Action_Pousser_La_Bombe(self):
        pass
        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x <= VAR.nbColonnes and y <= VAR.nbLignes
    def Zone_Traversable(self, gX, gY):
        return (self.TERRAIN.GRILLE[gX][gY].Traversable())
    
    
    def Attrape_Objet(self, _objet_attrape):
        
        # --- Si malade se debarrasse de sa maladie
        if self.estMalade():
            self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.MALADIE, True, 4, 4)
            self.Se_Soigne()
        
        # --- Prend le nouvel objet    
        if (_objet_attrape.objet == C_OBJET.BOMBE): self.bombes += 1
        if (_objet_attrape.objet == C_OBJET.FLAMME): self.puissance += 1
        if (_objet_attrape.objet == C_OBJET.SUPER_FLAMME): self.puissance += 5
        if (_objet_attrape.objet == C_OBJET.COUP_PIED): self.coup_de_pied = True
        if (_objet_attrape.objet == C_OBJET.COUP_POING): self.coup_de_poing = True
        if (_objet_attrape.objet == C_OBJET.ROLLER): self.vitesse += self.pasVitesse
        if (_objet_attrape.objet == C_OBJET.MALADIE): self.Tombe_Malade()

        # --- Detruit l'objet a l'écran
        self.OBJETS.Detruire_Objet(_objet_attrape)
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
        self.maladie = random.choices(list(C_MALADIE))[0]
        print(self.maladie)
        
                   
    def Detection_Collision_Decors(self):
        
        joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)

        collision = VAR.C_AUCUNE_COLLISION
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            x, y = coord                
            gX, gY = self.iX() + x, self.iY() + y
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):

                    decors = (gX * VAR.tailleCellule, gY * VAR.tailleCellule, VAR.tailleCellule, VAR.tailleCellule)
                    if FCT.Collision(joueur, decors): return (gX, gY)
                    if self.BOMBES.Detection_Collision_Avec_Les_Bombes(self): return (gX, gY)
            else:
                collision = VAR.C_HORS_TERRAIN
                break

        return collision



    def Algorithme_Drift(self, _collision_coord):
        d = self.direction
        xOld, yOld = self.x, self.y
        xCollision, yCollision = _collision_coord
        
        limit = 0.5
        limitx2 = limit *2
        
        # --- Test le Passage a empreinter pour contourner
        if d == C_DIRECTION.DROITE: 
            cellule_Sur_Chemin = (self.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        elif d == C_DIRECTION.GAUCHE: 
            cellule_Sur_Chemin = (self.TERRAIN.GRILLE[xCollision+1][yCollision-1].Traversable())      
        elif d == C_DIRECTION.HAUT: 
            cellule_Sur_Chemin = (self.TERRAIN.GRILLE[xCollision-1][yCollision+1].Traversable())      
        elif d == C_DIRECTION.BAS: 
            cellule_Sur_Chemin = (self.TERRAIN.GRILLE[xCollision-1][yCollision-1].Traversable())      
        
        # --- Test le passage final
        if d in [C_DIRECTION.DROITE,C_DIRECTION.GAUCHE]:                      
            # --- Passage au dessus            
            if  (yCollision-limitx2) <= self.y <= (yCollision-limit): 
                cellule_Destination = (self.TERRAIN.GRILLE[xCollision][yCollision-1].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.y -= self.vitesseBase  
                    
            # --- Passage au dessous
            elif (yCollision+limit ) <= self.y <= (yCollision+limitx2):
                cellule_Destination = (self.TERRAIN.GRILLE[xCollision][yCollision+1].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.y += self.vitesseBase

        elif d in [C_DIRECTION.HAUT,C_DIRECTION.BAS]:     
            # --- Passage au droite
            if (xCollision-limitx2) <= self.x <= (xCollision-limit): 
                cellule_Destination = (self.TERRAIN.GRILLE[xCollision-1][yCollision].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.x -= self.vitesseBase
                    
            # --- Passage au gauche
            elif (xCollision+limit ) <= self.x <= (xCollision + limitx2):
                cellule_Destination = (self.TERRAIN.GRILLE[xCollision+1][yCollision].Traversable())
                if cellule_Sur_Chemin and cellule_Destination:
                    self.x += self.vitesseBase
        
        # --- Ajustement du mouvement
        if not (yOld == self.y):
            if self.y-self.iY() < self.vitesseBase: self.y = self.iY()
        if not (xOld == self.x):
            if self.x-self.iX() < self.vitesseBase: self.x = self.iX()