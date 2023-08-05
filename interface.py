import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

import particules as CP
import time, random

class CInterface:
    def __init__(self, _moteur):        
        self.MOTEUR = _moteur
        self.PARTICULES = CP.CParticules(_moteur)        
     
    def Initialiser(self):
        self.x, self.y = 0.0, 0.0
        self.temps = -1
        self.etat = ""
        self.image = None
                
        self.temps_compte_a_rebours = -1
        self.delais_compte_a_rebours = 3
        
        self.message_temps = -1
        self.message_etape = C_MESSAGE.NON_INITIALISE    
        
        self.zone_particules = []
        self.zone_particules.append((0, 0, VAR.offSet[0], VAR.resolution[1]))    # Zone Gauche
        self.zone_particules.append((VAR.resolution[0] - VAR.offSet[0], 0, VAR.resolution[0], VAR.resolution[1]))    # Zone Droite   
             
        self.temps_particules = time.time()
        self.temps_delais = 0.2
        
    def Afficher_Fond(self):        
        VAR.fenetre.fill((16,16,16))
        
        if time.time() - self.temps_particules > self.temps_delais:
            self.temps_particules = time.time()
            
            for (x, y, w, h) in self.zone_particules:
                for _ in range(4):
                    self.PARTICULES.Ajouter_Particule(random.randint(x, w), random.randint(y, h), (162, 104, 254))
        self.PARTICULES.Afficher_Les_Particules()
        
    
    def Afficher_Barre_Information_Partie(self):
        x, y = 0, 4
        
        # --- cadre information en haut
        pygame.draw.rect(VAR.fenetre, (255, 137, 58, 64), (x, y, VAR.resolution[0], VAR.tailleCellule * 1.8), 0)
        pygame.draw.rect(VAR.fenetre, (255, 180, 112, 64), (x, y, VAR.resolution[0], VAR.tailleCellule * 1.8), 4)
        
        # --- chrono
        image = FCT.Image_Texte(FCT.convert_seconds_to_time(self.MOTEUR.tempsRestant()), (255,255,255,255), 50)   
        x, y = VAR.resolution[0] - VAR.tailleCellule - image.get_width(), y + 8    
        pygame.draw.rect(VAR.fenetre, (0, 0, 0, 32), (x-2, y-2, image.get_width(), image.get_height()), 0)     
        VAR.fenetre.blit(image, (x, y))
        
        # --- joueurs et scores
        x= VAR.tailleCellule
        nbJoueurs = self.MOTEUR.JOUEURS.nbJoueurs()+1
        largeur = (VAR.resolution[0] - image.get_width() - (VAR.tailleCellule * (nbJoueurs))) / nbJoueurs       
        
        for joueur in self.MOTEUR.JOUEURS.LISTE:
            imgId, indexId = C_DIRECTION.BAS.value, 0
            if joueur.mort: imgId, indexId = 5, 5
            VAR.fenetre.blit(FCT.image_decoupe(joueur.image,  indexId, imgId, VAR.tailleCellule, VAR.tailleCellule*2), (x, 4)) 
             
            image = FCT.Image_Texte(str(joueur.score), (0,0,0,255), 30)            
            VAR.fenetre.blit(image, (x + VAR.tailleCellule, VAR.tailleCellule-8))
            image = FCT.Image_Texte(str(joueur.score), (255,255,255,255), 30)            
            VAR.fenetre.blit(image, (x + VAR.tailleCellule+2, VAR.tailleCellule+2-8))
            x += (largeur + VAR.tailleCellule)
        
        
        

                    
    def Afficher_Compte_A_Rebours(self):       
        temps = int(round(self.delais_compte_a_rebours - (time.time() - self.temps_compte_a_rebours), 0))
        if temps < 0: temps = 0
        
        texte_ombre = FCT.Image_Texte(str(temps), (0,0,0,32), int(VAR.resolution[1] / 4))
        centreY = (VAR.resolution[1] - texte_ombre.get_height()) /2
        centreX = (VAR.resolution[0] - texte_ombre.get_width()) /2
        
        texte = FCT.Image_Texte(str(temps), (255,255,255,128), int(VAR.resolution[1] / 4))
        VAR.fenetre.blit(texte_ombre, (centreX+8, centreY+8))
        VAR.fenetre.blit(texte, (centreX, centreY))
    
    
    def Victoire_Afficher(self):   
        joueur = self.MOTEUR.JOUEURS.quiGagne()
        self.Victoire_Dessiner_Bandeau(joueur)
        
        if self.message_etape == C_MESSAGE.COMPTE_A_REBOURS:
            if self.temps_compte_a_rebours == -1:
                self.temps_compte_a_rebours = time.time()
                FCT.Charge_Musique('23')
                pygame.mixer.music.play()
            
            self.Afficher_Compte_A_Rebours()            
                
            if time.time() - self.temps_compte_a_rebours > self.delais_compte_a_rebours:
                joueur.score += 1
                self.MOTEUR.Relancer_Une_Partie()                
                self.message_etape = C_MESSAGE.NON_INITIALISE
                
        
        
    def Victoire_Dessiner_Bandeau(self, _joueur):
        if not _joueur == None:
            icone = VAR.image['avatar' + str(_joueur.id)]
            message = "Victoire du joueur " + _joueur.pseudo
        else:
            icone = None
            message = "Egalité"
                
        self.Afficher_Message(icone, message, 0)
            
            
    def Dessiner_Cadre(self, _x, _y, _largeur, _hauteur, _couleurFond, _couleurBordure, _epaisseurBordure=2):
        pygame.draw.rect(VAR.fenetre, _couleurFond, (_x, _y, _largeur, _hauteur), 0)  
        pygame.draw.rect(VAR.fenetre, _couleurBordure, (_x, _y, _largeur, _hauteur), _epaisseurBordure) 
        
    
    def Attendre_Pression_Bouton(self):
        boucle_pause = True
        while boucle_pause:
            # --- récupére l'ensemble des évènements
            for event in pygame.event.get():        
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: VAR.boucle_jeu = False     
                if event.type == KEYDOWN:  
                    if event.key == K_SPACE: 
                        boucle_pause = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if (event.button == 1):
                        boucle_pause = False
                        
            pygame.display.update()
                    
    def Afficher_Message(self, _icone, _texte, _delais):
        couleur_fond, couleur_bordure = (0, 0, 0, 64), (255, 255, 255, 255)
        hauteur = 140
        largeur = VAR.resolution[0]
        
        if self.message_etape == C_MESSAGE.NON_INITIALISE:
            self.MOTEUR.Arreter_Partie()
            self.x = -largeur
            self.y = VAR.resolution[1] - hauteur - (VAR.tailleCellule  * 3)
            self.message_temps = time.time()
            self.message_etape = C_MESSAGE.SCROLLX
            self.temps_compte_a_rebours = -1
        
        if self.message_etape == C_MESSAGE.SCROLLX:  
            if (time.time() - self.message_temps > 0.01):
                self.message_temps = time.time()
                self.x += VAR.tailleCellule
                
            
            if self.x >= 0:
                self.x, self.message_temps = 0, -1
                self.message_etape = C_MESSAGE.EN_ATTENTE_START
            
        # --- Dessine cadre
        self.Dessiner_Cadre(self.x, self.y, largeur, hauteur, couleur_fond, couleur_bordure, 4)
        
        # --- Dessine image
        if _icone == None:
            imageW = 0
        else:
            image = pygame.transform.scale(_icone, (hauteur, hauteur))
            imageW = image.get_width()
            VAR.fenetre.blit(image, (self.x + VAR.tailleCellule, self.y))
            
        
        # --- Dessine texte
        texte = FCT.Image_Texte(_texte, (255,255,255,255), int(40))
        centreY = (hauteur - texte.get_height()) /2
        centreX = (largeur - imageW - texte.get_width()) / 2
        VAR.fenetre.blit(texte, (self.x + imageW + centreX, self.y + centreY))
        
        if self.message_etape == C_MESSAGE.EN_ATTENTE_START:
            self.Attendre_Pression_Bouton()
            self.message_etape = C_MESSAGE.COMPTE_A_REBOURS
       