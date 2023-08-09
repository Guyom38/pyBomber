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
        
        self.nb_morts = 0
        self.nb_manches = 0
        
        self.couleur = (255,255,255,255)        
    
        self.Initialiser(self.id)
       
    
    def Initialiser(self, _position):        
        self.x, self.y = self.Position_Initiale(_position) 
        self.direction = C_DIRECTION.BAS
        self.enMouvement = False
        
        self.vitesseBase = VAR.C_VITESSE_JOUEUR
        self.pasVitesse = VAR.C_VITESSE_PAS
        self.vitesse = self.vitesseBase
        
        self.puissance = 1
        self.bombes = 3
        self.bombes_posees = 0
        self.bombes_protection = None        
        self.coup_de_pied = True
        self.coup_de_poing = False
        
        self.maladie = 0
        self.maladie_temps = -1        
        self.maladie_temps_touche = -1
        
        self.mort = False
        self.clown = False
        
        if not self.menu:
            self.TERRAIN.Libere_Zone(self.celluleX(), self.celluleY(), 2)    
        
        self.offSetX = 0
        self.offSetY = - 12 * VAR.zoom
        self.Colorisation()
                                
    def Colorisation(self):
        print("recolorie")
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
        
        # --- Evite les murs de decors
        if x % 2 == 0: x -=1
        if y % 2 == 0: y -=1
        
        return (x, y)
    

# -----------------------------------------------------------------------------------------------------------
#
#   AFFICHAGE
#
# -----------------------------------------------------------------------------------------------------------        
    
    
    def Afficher(self, _menu = False):
        if not self.actif: return
        
        posX = self.ecranX()
        posY = self.ecranY()    
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
    

    def score(self):
        return (self.nb_manches * 1000) + (self.nb_morts * 50)
    
        
    def Action_Poser_Une_Bombe(self):
        if self.bombes_posees < self.bombes:
            if self.BOMBES.Ajouter_Une_Bombe(self):   
                if self.maladie == C_MALADIE.CHIASSE:
                    FCT.jouer_sons("pet")
                else:
                    FCT.jouer_sons("poser_bombe")
    

    def Retire_Protection_Bombe_Si_A_Cote(self):
        if self.bombes_protection == None: return
        if not FCT.Collision2((self.x, self.y), (self.bombes_protection.x, self.bombes_protection.y)):        
            self.bombes_protection = None

# -----------------------------------------------------------------------------------------------------------
#
#   MALADIES
#
# -----------------------------------------------------------------------------------------------------------

    def Gestion_Maladies(self):
        vitesseDeBase = self.vitesse
        if self.maladie == C_MALADIE.RALENTISSEMENT: vitesseDeBase = 0.02
        if self.maladie == C_MALADIE.FIGER:
            if self.maladie_temps == -1: self.maladie_temps = time.time()
            if time.time() - self.maladie_temps < VAR.maladie_delais_figer:
                self.enMouvement = False
                return 
            else:
                self.Se_Soigne()
        if self.maladie == C_MALADIE.CHIASSE:
            if self.maladie_temps == -1: self.maladie_temps = time.time()
            if time.time() - self.maladie_temps < VAR.maladie_delais_chiasse:
                self.Action_Poser_Une_Bombe() 
            else:
                self.Se_Soigne()                
        return (vitesseDeBase)   

    def Se_Soigne(self):
        self.maladie = 0
        self.maladie_Temps = -1
           
    def Tombe_Malade(self):
        FCT.jouer_sons("tete_mort")
        self.maladie = random.choices(list(C_MALADIE))[0]
        print(self.maladie)
            
    def Contamine_Autre_Joueur(self, _joueurMalade, _joueurSain):
        if (_joueurMalade.maladie_temps_touche == -1 or time.time() - _joueurMalade.maladie_temps_touche > 2):
            _joueurSain.maladie = _joueurMalade.maladie
            _joueurSain.maladie_temps_touche = time.time()
            _joueurSain.maladie_temps = time.time()
            _joueurMalade.maladie = 0
            _joueurMalade.maladie_temps_touche = -1
       
            return True        
        else:
            return False     

    def estMalade(self): return not (self.maladie == 0)
    def vraimentMort(self): return (self.mort and self.animationId == -1)                    
    def Mourir(self): self.mort = True
        
    def Transmission_Heritage_Apres_Mort(self):
        # --- jete les objets
        for _ in range(self.bombes-1):
            if random.randint(0,100) <25: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.BOMBE, True)
        
        for _ in range(self.puissance-1):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.FLAMME, True)
        
        nbVitesse = int(round((self.vitesse-self.vitesseBase) / self.pasVitesse,0))
        for _ in range(nbVitesse):
            if random.randint(0, 100) <15: self.OBJETS.Ajouter_Un_Objet(self.iX(), self.iY(), C_OBJET.ROLLER, True)
                   
# -----------------------------------------------------------------------------------------------------------
#
#   DEPLACEMENTS & COLLISIONS
#
# -----------------------------------------------------------------------------------------------------------         
    def Gestion_Deplacement(self):         
        vitesseDeBase = self.Gestion_Maladies()
        if self.enMouvement == False: return        
        
        # --- mouvement en fonction de la direction
        if self.direction == C_DIRECTION.HAUT:   self.y -= vitesseDeBase
        if self.direction == C_DIRECTION.BAS:    self.y += vitesseDeBase
        if self.direction == C_DIRECTION.GAUCHE: self.x -= vitesseDeBase
        if self.direction == C_DIRECTION.DROITE: self.x += vitesseDeBase        

        self.Gestion_Collisions()
        self.Retire_Protection_Bombe_Si_A_Cote()              
        self.enMouvement = False       
              
        
    def Gestion_Collisions(self):
        # --- controle si collision
        coord_collision_mur = self.Detection_Collision_Decors()
        collision_bombe = self.Detection_Collision_Bombe()
        #coord_collision_bombe = self.Detection_Collision_Avec_Bombes()
        if (not coord_collision_mur == VAR.C_AUCUNE_COLLISION or collision_bombe): # or (not coord_collision_bombe == VAR.C_AUCUNE_COLLISION):
            # --- repositionne parfaitement la position du joueur sur la case qu'il occupe
            if self.direction in [C_DIRECTION.HAUT,C_DIRECTION.BAS]: self.y = self.celluleY()
            if self.direction in [C_DIRECTION.GAUCHE,C_DIRECTION.DROITE]: self.x = self.celluleX()
            
            if not collision_bombe: 
                self.Algorithme_Drift(coord_collision_mur)          
        
        self.Detection_Collision_Objets()
        self.Detection_Collision_Avec_Autres_Joueurs()              
                
          
    def Action_Pousser_La_Bombe(self):
        pass
        
    def Toujours_Sur_Le_Terrain(self, x, y):
        return x >= 0 and y >=0 and x < VAR.nbColonnes and y < VAR.nbLignes
    
    def Zone_Traversable(self, gX, gY):
        return (self.TERRAIN.GRILLE[gX][gY].Traversable())    
    
    def Attrape_Objet(self, _objet_attrape):        
        # --- Si malade se debarrasse de sa maladie
        if self.estMalade():
            self.OBJETS.Ajouter_Un_Objet(self.celluleX(), self.celluleY(), C_OBJET.MALADIE, True, 4, 4)
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
            
    def Detection_Collision_Decors(self):        
        collision = VAR.C_AUCUNE_COLLISION
        for coord in ((-1,-1), (0,-1), (1, -1),
                      (-1, 0), (0, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)):
            
            x, y = coord                
            gX, gY = self.celluleX() + x, self.celluleY() + y
            
            if self.Toujours_Sur_Le_Terrain(gX, gY):
                if not self.Zone_Traversable(gX, gY):
                    if FCT.Collision2((self.x, self.y), (gX, gY)): return (gX, gY)

            else:
                collision = VAR.C_HORS_TERRAIN
                break

        return collision

    # --- Reaction du joueur face a une bombe
    def Detection_Collision_Bombe(self):
        # --- recupere la bombe touchée
        bombe_touchee = FCT.Detection_Collision(self.BOMBES, self)
        
        if not bombe_touchee == None:
            if self.bombes_protection == bombe_touchee:
                return False
                        
            if self.coup_de_pied and not bombe_touchee.enMouvement:
                bombe_touchee.direction = self.direction
                bombe_touchee.enMouvement = True
                return False
            else:
                return True
        return False
              
    def Detection_Collision_Objets(self):
        #joueur = ((self.x * VAR.tailleCellule), (self.y * VAR.tailleCellule), VAR.tailleCellule, VAR.tailleCellule)
        objet_attrape = FCT.Detection_Collision(self.OBJETS, self)
        
        if not (objet_attrape == None):     
            if not objet_attrape.enMouvement:
                self.Attrape_Objet(objet_attrape)

    def Detection_Collision_Avec_Autres_Joueurs(self):
        for joueur in self.JOUEURS.LISTE:
            if not joueur == self:

                if FCT.Collision2((self.x, self.y), (joueur.x, joueur.y)):
                    if self.coup_de_poing: return True
                    
                    # --- si je suis malade
                    if self.estMalade():
                        return self.Contamine_Autre_Joueur(self, joueur)
                    elif joueur.estMalade():
                        return self.Contamine_Autre_Joueur(joueur, self)
        return False
    
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
            if self.y-self.celluleY() < self.vitesseBase: self.y = self.celluleY()
        if not (xOld == self.x):
            if self.x-self.celluleX() < self.vitesseBase: self.x = self.celluleX()