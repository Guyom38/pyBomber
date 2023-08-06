
import pygame
from pygame.locals import *

import threading, time

import variables as VAR
import fonctions as FCT

from enums import *

class CHighscore:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        self.init = False
        
    def Initialiser(self):
        self.liste_joueurs_tries = sorted(self.MOTEUR.JOUEURS.LISTE, key=lambda joueur: joueur.score)
        
        self.nbJoueurs = 0
        for joueur in self.liste_joueurs_tries:
            if joueur.actif: self.nbJoueurs +=1
            joueur.x = 0.0
            
        self.temps = time.time()
        self.delais = 6
        
    def Afficher_Highscore(self):
        if not self.init:
            self.Initialiser()
            self.init = True
            
        couleur_titre_texte = (255,255,255)
        couleur_titre_fond = (0,0,0)
        couleur_joueurs_cadre = (64, 64, 64, 200)
        couleur_joueurs_bordure = (255, 255, 255, 255)        
        
        hauteur_titre = 100
        
        
        
        marge = 64
        espacement = 8
        largeur_course = VAR.resolution[0] - (marge * 2)
        hauteur_course = (int((VAR.resolution[1] - hauteur_titre - (espacement * 2)) / self.nbJoueurs)) - espacement
        posCourseDepart = 240
        pasCourse = (largeur_course - posCourseDepart) / (VAR.nb_parties + 1)
        
        # --- Image fond
        VAR.fenetre.blit(VAR.image["r"], (0, 0))
        
        # --- Cadre Titre
        pygame.draw.rect(VAR.fenetre, couleur_titre_fond, (0, 0, VAR.resolution[0], hauteur_titre))
        image_titre = FCT.Image_Texte("TABLEAU DES SCORES", couleur_titre_texte, int(hauteur_titre / 2))
        centreX, centreY = int((VAR.resolution[0] - image_titre.get_width()) / 2), int((hauteur_titre - image_titre.get_height()) /2)
        VAR.fenetre.blit(image_titre, (centreX, centreY))
        
        # --- Cadre Joueurs
        
        x, y = marge, hauteur_titre + espacement
        
        #self.INTERFACE.Dessiner_Cadre(x + 256, y - 16, VAR.resolution[0] - 400, (len(self.MOTEUR.JOUEURS.LISTE)*80) + 22, (0, 0, 255, 64), couleur_bordure, 4)
        rang = 1
        for joueur in self.liste_joueurs_tries:
            if joueur.actif:
                
                # --- affiche cadre
                self.INTERFACE.Dessiner_Cadre(x, y, largeur_course, hauteur_course, couleur_joueurs_cadre, couleur_joueurs_bordure, 4)
                
                # --- affiche depart
                VAR.fenetre.blit(pygame.transform.scale(VAR.image["start"], (hauteur_course - 8, hauteur_course - 8)) , (x + posCourseDepart, y+4))
                VAR.fenetre.blit(pygame.transform.scale(VAR.image["start"], (hauteur_course - 8, hauteur_course - 8)) , (x + largeur_course - marge - (hauteur_course), y+4))
                
                # --- affiche manche
                xc = x + posCourseDepart + (hauteur_course /2)
                for i in range(VAR.nb_parties -1):
                    rect_surface = pygame.Surface((16, hauteur_course), pygame.SRCALPHA)
                    pygame.draw.rect(rect_surface, (16,16,16, 64), rect_surface.get_rect(), border_radius=10)
                    VAR.fenetre.blit(rect_surface, (xc + ((i + 1) * pasCourse), y))
        
                
                # --- affiche joueur
                if joueur.x == 0.0: joueur.x = x + (posCourseDepart) + int(hauteur_course * 0.8)
                xj = x + (posCourseDepart) + (joueur.score * pasCourse) + int(hauteur_course * 0.8)
                vitesse = (VAR.nb_parties * pasCourse) / 150
                if joueur.x < xj:
                    joueur.x += vitesse
                    joueur.direction = C_DIRECTION.DROITE
                    animationId = FCT.Animation(10, 3)
                else:
                    joueur.direction = C_DIRECTION.BAS
                    animationId = 0
                    
                
                image = FCT.image_decoupe(joueur.image, animationId, joueur.direction.value, VAR.tailleCellule, VAR.tailleCellule*2)
                image = pygame.transform.scale(image, (int(hauteur_course * 0.8), hauteur_course * 1.6)) 
                
                    
                VAR.fenetre.blit( image , (joueur.x, y - (hauteur_course / 3)))
                
                # --- affiche position
                image_texte = FCT.Image_Texte(str(rang)+"P", (255,255,255,255), 50)
                VAR.fenetre.blit(image_texte, (x+16, y+16))
                y += hauteur_course + espacement
                rang +=1
                
        if time.time() - self.temps > self.delais:
            self.MOTEUR.Relancer_Une_Partie()

  