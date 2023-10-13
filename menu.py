import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *

import cellule as CC
import bouton as CB

import time, random
import ressources as CR
import qr_code as QR

class CMenu():
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.INTERFACE = _moteur.INTERFACE
        self.PARTICULES = _moteur.PARTICULES
        self.TERRAIN = _moteur.TERRAIN
        self.JOUEURS = _moteur.JOUEURS
        
        self.couleur_fond, self.couleur_bordure = (64, 64, 64, 64), (255, 255, 255, 255)
        self.temps_particules = time.time()
        self.temps_delais = 0.1
        
        self.select = None
        self.bouton_en_cours = -1
        self.oldZoom = 3
        
        self.niveau = 0
        
        self.nbColonnesRef = VAR.nbColonnes
        self.nbLignesRef = VAR.nbLignes
        
        self.imageQrCode = None
        
    def Action_NombreParties(self, _juste_valeur):
        if _juste_valeur:
            if VAR.nb_parties == 0: return "illimité"
            return VAR.nb_parties
        else:
            VAR.nb_parties += 1
            if VAR.nb_parties > 10: VAR.nb_parties = 0
            
            
    def Action_DureeParties(self, _juste_valeur):
        if _juste_valeur:
            if VAR.duree_partie == 0: return "illimité"
            return FCT.convert_seconds_to_time(VAR.duree_partie)
        else: 
            VAR.duree_partie += 30
            if VAR.duree_partie > 600: VAR.duree_partie = 0
            
            
    def Action_Active_Maladies(self, _juste_valeur):
        if _juste_valeur:
            return "ON" if VAR.active_maladies else "OFF"
        else:
            VAR.active_maladies = not VAR.active_maladies
            
            
    def Action_Active_Heritage(self, _active_heritage):
        if _active_heritage:
            return "ON" if VAR.active_heritage else "OFF"
        else:
            VAR.active_heritage = not VAR.active_heritage
    
    
    def Action_Revenir_Principal(self, _juste_valeur):
        if _juste_valeur:
            return None
            
        else:
            self.menu = "PRINCIPAL"


    def Action_Dimension_Suivante(self, _juste_valeur):
        if _juste_valeur:
            if self.niveau == 0:
                self.nbColonnesRef = 15
                self.nbLignesRef = 13
                return "ORIGINAL" + " ("+str(self.nbColonnesRef)+"x"+str(self.nbLignesRef)+")"
            elif self.niveau == 1:
                self.nbColonnesRef = 40
                self.nbLignesRef = 20
                return "LARGE" + " ("+str(self.nbColonnesRef)+"x"+str(self.nbLignesRef)+")"
            elif self.niveau == 2:
                self.nbColonnesRef = 60
                self.nbLignesRef = 30
                return "MEGA" + " ("+str(self.nbColonnesRef)+"x"+str(self.nbLignesRef)+")"
            
        else:
            self.niveau += 1
            if self.niveau > 2: self.niveau = 0
            return self.Action_Dimension_Suivante(True)  
            
            
    
    def Initialiser(self):

        FCT.Charge_Musique("menu" )  
        CR.Changement_Zoom(3)    
        
        self.largeurZone = 640
        self.hauteur_saut = 10
        self.hauteur_vide = VAR.tailleCellule
        
        ## --- dimension pour le menu
        VAR.nbColonnes = int((self.largeurZone / VAR.tailleCellule)) +1
        VAR.nbLignes = int((VAR.resolution[1] / VAR.tailleCellule)) - 2        
        self.largeurBouton, self.hauteurBouton = (VAR.nbColonnes - 2) * VAR.tailleCellule, 64
        
        self.TERRAIN.Initialiser(True)            
        self.JOUEURS.Reinitaliser()
        
        self.LISTE = {}
        self.menu = "PRINCIPAL"
        self.menu_sous = ""
        self.id = 0
        
        MENU1 = []
        MENU1.append(CB.CBouton(self.MOTEUR, 0, "DEMARRER LA PARTIE"))
        MENU1.append(CB.CBouton(self.MOTEUR, 99, ""))
        MENU1.append(CB.CBouton(self.MOTEUR, 1, "CHOIX NIVEAUX"))
        MENU1.append(CB.CBouton(self.MOTEUR, 2, "REGLES DE JEU"))
        MENU1.append(CB.CBouton(self.MOTEUR, 99, ""))
        MENU1.append(CB.CBouton(self.MOTEUR, 4, "OPTIONS"))
        MENU1.append(CB.CBouton(self.MOTEUR, 5, "QUITTER"))
        self.LISTE["PRINCIPAL"] = MENU1
        
        MENU2 = []
        MENU2.append(CB.CBouton(self.MOTEUR, 10,  "NB. MANCHES", self.Action_NombreParties))
        MENU2.append(CB.CBouton(self.MOTEUR, 11,  "DUREE", self.Action_DureeParties))
        MENU2.append(CB.CBouton(self.MOTEUR, 12,  "MALADIES", self.Action_Active_Maladies))
        MENU2.append(CB.CBouton(self.MOTEUR, 13,  "HERITAGE", self.Action_Active_Heritage))           
        MENU2.append(CB.CBouton(self.MOTEUR, 99,  ""))           
        MENU2.append(CB.CBouton(self.MOTEUR, 98,  "REVENIR"))           
        self.LISTE["PARTIE"] = MENU2
        
        MENU4 = []
        MENU4.append(CB.CBouton(self.MOTEUR, 20, "", self.Action_Dimension_Suivante))
        MENU4.append(CB.CBouton(self.MOTEUR, 99, ""))
        MENU4.append(CB.CBouton(self.MOTEUR, 21, "TERRAIN (CLASSIQUE)"))
        MENU4.append(CB.CBouton(self.MOTEUR, 22, "HAUTEUR (15) "))
        MENU4.append(CB.CBouton(self.MOTEUR, 23, "AU TAQUET"))
        MENU4.append(CB.CBouton(self.MOTEUR, 99, ""))
        MENU4.append(CB.CBouton(self.MOTEUR, 98, "REVENIR"))
        self.LISTE["NIVEAU"] = MENU4
        

        
             

        MENU3 = []
        MENU3.append(CB.CBouton(self.MOTEUR, 30,  "RESOLUTION (1024x768)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 31,  "ZOOM (x2)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 32,  "MUSIC (ON)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 33,  "PARTICULE (ON)"))
        MENU3.append(CB.CBouton(self.MOTEUR, 99,  ""))
        MENU3.append(CB.CBouton(self.MOTEUR, 98,  "REVENIR"))
        self.LISTE["OPTIONS"] = MENU3
        
        self.Positionne_Joueurs_Menu()
        
   
         
  
    def Positionne_Joueurs_Menu(self):
        
        posX_id = 2
        for joueur in self.JOUEURS.LISTE:
            joueur.actif = True
            if joueur.id == 0:
                joueur.x, joueur.y = 1, 1
            else:
                joueur.x, joueur.y = posX_id, VAR.nbLignes - 2
                posX_id += 1.5
                  
    def Dessiner_Titre(self):
        VAR.fenetre.blit(VAR.image['titre'], (0, 0))    
         
    
    def Calcul_Hauteur_Cadre(self):        
        hauteur_boutons = 0
        for bouton in self.LISTE[self.menu]:
            if not bouton.id == 99:
                hauteur_boutons += self.hauteurBouton + self.hauteur_saut
            else:
                hauteur_boutons += self.hauteur_vide
        hauteur_boutons -= self.hauteur_saut
        return hauteur_boutons
    
    def Dessiner_Bouton(self):
        
        hauteur_boutons = self.Calcul_Hauteur_Cadre()
               
        self.x, self.y = (VAR.resolution[0] - self.largeurZone) - 96,  int((VAR.resolution[1] - hauteur_boutons)  / 2)
        VAR.offSet = (self.x, VAR.tailleCellule) 
        
        for bouton in self.LISTE[self.menu]:
            if not bouton.id == 99:
                bouton_presse = bouton.Afficher_Bouton(self.x, self.y)
                self.y += self.hauteurBouton + self.hauteur_saut
                if bouton_presse:
                    if bouton.id == 0:
                        nbJoueursPourLaPartie = len([1 for joueur in self.MOTEUR.JOUEURS.LISTE if joueur.clown])                        

                        if nbJoueursPourLaPartie > 1:  
                            for joueur in self.MOTEUR.JOUEURS.LISTE:
                                joueur.actif = (joueur.clown or joueur.id == 0)
                            
                            VAR.zoom = self.oldZoom     
                            VAR.nbColonnes = self.nbColonnesRef
                            VAR.nbLignes = self.nbLignesRef
                            
                            self.MOTEUR.Relancer_Une_Partie()
                            
                    elif bouton.id == 1:
                        self.menu = "NIVEAU"                            
                    elif bouton.id == 2:
                        self.menu = "PARTIE"
                            
                    elif bouton.id == 4:
                        self.menu = "OPTIONS"    
                    elif bouton.id == 5:
                        VAR.boucle_jeu = False
                    elif bouton.id == 98:
                        self.menu = "PRINCIPAL"
            else:
                self.y += self.hauteur_vide
                                                       
                            
        self.MOTEUR.CONTROLLEUR.action_bouton = False
                            
    def Dessiner_Particules(self):
        if time.time() - self.temps_particules > self.temps_delais:
            self.temps_particules = time.time()            
            for _ in range(4):
                self.PARTICULES.Ajouter_Particule(random.randint(0, VAR.resolution[0]), VAR.resolution[1], (162, 104, 254))
        self.PARTICULES.Afficher_Les_Particules()  
    
    def Dessiner_QrCode(self):
        if self.imageQrCode == None:         
            # Génère le QR Code et le convertit en surface Pygame
            qrcode_image = QR.generate_qr_code("http://ladnet.net/joystick/")
            self.imageQrCode = QR.qr_image_to_pygame_surface(qrcode_image)
        VAR.fenetre.blit( self.imageQrCode, (10, VAR.resolution[1] - self.imageQrCode.get_height()-10))
       
    
    def Afficher_Menu(self):
        joueurSelect = None
        
        self.Dessiner_Titre()
        self.TERRAIN.Afficher() 
        self.Dessiner_Bouton()
        
        if self.menu != "PRINCIPAL": joueurSelect = 0            
        self.JOUEURS.Afficher_Tous_Les_Joueurs(joueurSelect)

        if VAR.web_socket: 
            self.Dessiner_QrCode()
            
        self.Dessiner_Particules()

        if self.MOTEUR.CONTROLLEUR.Recherche_Manettes():
            self.Initialiser()
                
    
    
    
    

    
