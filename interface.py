import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

import particules as CP
import time, random

class CInterface:
    def __init__(self, _moteur):
        self.x, self.y = 0.0, 0.0
        self.temps = -1
        self.etat = ""
        self.image = None
        
        self.MOTEUR = _moteur
        
        self.temps_compte_a_rebours = -1
        self.delais_compte_a_rebours = 5

        self.PARTICULES = CP.CParticules(_moteur)
        
    def Initialiser(self):
        VAR.image["titre"] = pygame.transform.scale(pygame.image.load("images/R.jpg"), VAR.resolution)
        

    
    def Afficher(self):
        if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.TITRE:
            #self.Afficher_Cadre()
            self.Afficher_Fond()
            
            image = FCT.Image_Texte("PyBomber", (32,0,0,0), 150)
            x = (VAR.resolution[0] - image.get_width()) / 2
            VAR.fenetre.blit(image, (x, 100))
            
            image = FCT.Image_Texte("PyBomber", (255,255,255,255), 150)            
            VAR.fenetre.blit(image, (x-10, 100-10))
            
            
    
    def Afficher_Fond(self):        
        VAR.fenetre.fill((16,16,16))
        #for _ in range(random.randint(0, 10)):
        #     self.PARTICULES.Ajouter(random.randint(0, VAR.resolution[0]), random.randint(0, VAR.resolution[1]), (162, 104, 254))
        #self.PARTICULES.Afficher_Les_Particules()
        
    
    def Afficher_Barre_Information_Partie(self):
        pygame.draw.rect(VAR.fenetre, (255, 137, 58, 64), (0, 0, VAR.resolution[0], VAR.offSet[1] - 4), 0)
        
        nbJoueurs = self.MOTEUR.JOUEURS.nbJoueurs()
        largeur = VAR.tailleCellule * 4
        
        x= VAR.tailleCellule
        for joueur in self.MOTEUR.JOUEURS.LISTE:
            VAR.fenetre.blit(FCT.image_decoupe(joueur.image,  0, C_DIRECTION.BAS.value, VAR.tailleCellule, VAR.tailleCellule*2), (x, 0))  
            image = FCT.Image_Texte(str(joueur.score), (0,0,0,255), 30)            
            VAR.fenetre.blit(image, (x + VAR.tailleCellule, VAR.tailleCellule))
            image = FCT.Image_Texte(str(joueur.score), (255,255,255,255), 30)            
            VAR.fenetre.blit(image, (x + VAR.tailleCellule+2, VAR.tailleCellule+2))
            x += (largeur + VAR.tailleCellule)
            
    def Afficher_Cadre(self, _largeur = -1, _hauteur = -1):
        if _largeur == -1 and _hauteur == -1:
            _largeur, _hauteur = int(VAR.resolution[0] / VAR.tailleCellule), int(VAR.resolution[1] / VAR.tailleCellule) 
            
        image_contour = VAR.image["mur"]
        image_fond = VAR.image["sol0"]
        
        offSet = ( (VAR.resolution[0] - (_largeur* VAR.tailleCellule)) /2, (VAR.resolution[1] - (_hauteur* VAR.tailleCellule)) /2 )  
         
        for y in range(_hauteur):
            for x in range(_largeur):
                posX = offSet[0] + (x * VAR.tailleCellule)
                posY = offSet[1] + (y * VAR.tailleCellule)
                
                if x == 0 or y == 0 or x == _largeur-1 or y == _hauteur-1:
                    VAR.fenetre.blit(image_contour, (posX, posY))
                else:
                    VAR.fenetre.blit(image_fond, (posX, posY))
                    
    def Afficher_Compte_A_Rebours(self):
       
        temps = int(round(self.delais_compte_a_rebours - (time.time() - self.temps_compte_a_rebours), 0))
        
        texte_ombre = FCT.Image_Texte(str(temps), (0,0,0,32), int(VAR.resolution[1] / 4))
        centreY = (VAR.resolution[1] - texte_ombre.get_height()) /2
        centreX = (VAR.resolution[0] - texte_ombre.get_width()) /2
        
        texte = FCT.Image_Texte(str(temps), (255,255,255,128), int(VAR.resolution[1] / 4))
        VAR.fenetre.blit(texte_ombre, (centreX+8, centreY+8))
        VAR.fenetre.blit(texte, (centreX, centreY))
        
    def Afficher_Victoire(self):
        if self.temps_compte_a_rebours == -1:
            self.temps_compte_a_rebours = time.time()
            self.MOTEUR.Charge_Musique('23')
            pygame.mixer.music.play()
            
        joueur = self.MOTEUR.JOUEURS.quiGagne()
        self.Dessiner_Bandeau_Victoire(joueur)
        self.Afficher_Compte_A_Rebours()
        
            
        if time.time() - self.temps_compte_a_rebours > self.delais_compte_a_rebours:
            joueur.score += 1
            self.MOTEUR.Relancer_Une_Partie()
            self.temps_compte_a_rebours = -1
        
        
    def Dessiner_Bandeau_Victoire(self, _joueur):
        if self.etat != "bandeau_victoire":
            
            largeur, hauteur_pas = VAR.resolution[0], VAR.resolution[1]/20
            hauteur = hauteur_pas * 4
            
            couleur_fond, couleur_bordure = (0, 0, 0, 64), (255, 255, 255, 64)
            self.x = 0
            self.y = VAR.resolution[1] - (VAR.tailleCellule * 2) - hauteur
            self.Dessiner_Cadre(self.x, self.y, largeur, hauteur, couleur_fond, couleur_bordure, 4)
            
            if not _joueur == None:                
                image_avatar = pygame.transform.scale(VAR.image['avatar' + str(_joueur.id)], (hauteur_pas * 4, hauteur_pas * 4))
                VAR.fenetre.blit(image_avatar, (self.x + VAR.tailleCellule, self.y))
                message = "Victoire du joueur " + _joueur.pseudo
                decX = image_avatar.get_width()
            else:
                message = "Egalité !"
                decX = 0
        
            texte = FCT.Image_Texte(message, (255,255,255,255), int(hauteur_pas))
            centreY = (hauteur - texte.get_height()) /2
            centreX = (largeur - decX - texte.get_width()) / 2
            VAR.fenetre.blit(texte, (self.x + decX + centreX, self.y+centreY))
            VAR.pause = True
            
    def Dessiner_Cadre(self, _x, _y, _largeur, _hauteur, _couleurFond, _couleurBordure, _epaisseurBordure=2):
        pygame.draw.rect(VAR.fenetre, _couleurFond, (_x, _y, _largeur, _hauteur), 0)  
        pygame.draw.rect(VAR.fenetre, _couleurBordure, (_x, _y, _largeur, _hauteur), _epaisseurBordure)  