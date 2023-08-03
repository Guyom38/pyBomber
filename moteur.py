import pygame
import pygame.midi
import pygame.mixer
from pygame.locals import *

import terrain as CT
import joueurs as CJS
import bombes as CBS
import particules as CP
import controlleur as CC
import objets as COS
import interface as CI

import variables as VAR
import fonctions as FCT

from enums import *

import random, time

class CMoteur():
    def __init__(self):
        self.INTERFACE = CI.CInterface(self)
        self.TERRAIN = CT.CTerrain(self)   
        self.BOMBES = CBS.CBombes(self)   
        self.OBJETS = COS.CObjets(self)      
        self.JOUEURS = CJS.CJoueurs(self)
        self.CONTROLLEUR = CC.CCControlleur(self)   
        self.PARTICULES = CP.CParticules(self)   
          
        pygame.init()   
        pygame.mixer.init()     
        

    
    def Initialisation(self):
        
        
        self.INTERFACE.Initialiser()
        self.TERRAIN.Initialiser()
        self.BOMBES.Initialiser()
        self.OBJETS.Initialiser()
        self.JOUEURS.Initialiser()
        self.CONTROLLEUR.Initialiser()
        
        VAR.offSet = ( ((VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2) ,
                       ((VAR.resolution[1] - (VAR.nbLignes* VAR.tailleCellule)) /2) + VAR.tailleCellule) 
        
        #self.CONTROLLEUR.Creer_Joueurs_Clavier_Manettes()
        self.phase_jeu = C_PHASE_DE_JEU.JEU
        self.nbSecondes_Restantes_AvPause = -1
        
    def Chargement_Ressources(self):
        VAR.tailleCellule = 16 * VAR.zoom
        
        # --- Decors
        tmp = pygame.image.load("images/decors.png").convert_alpha() 
        if VAR.zoom > 1: tmp = pygame.transform.scale(tmp, (tmp.get_width() * VAR.zoom, tmp.get_height() * VAR.zoom))  
        
        VAR.image["cassable"] = FCT.image_decoupe(tmp, 0, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["cassable0"] = FCT.image_decoupe(tmp, 1, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["cassable1"] = FCT.image_decoupe(tmp, 2, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["cassable2"] = FCT.image_decoupe(tmp, 2, 1, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["sol0"] = FCT.image_decoupe(tmp, 0, 2, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["sol1"] = FCT.image_decoupe(tmp, 0, 2, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["ombre"] = FCT.image_decoupe(tmp, 1, 2, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image["mur"] = FCT.image_decoupe(tmp, 0, 1, VAR.tailleCellule, VAR.tailleCellule )

        # --- Joueurs
        VAR.image["joueur0"] = pygame.image.load("images/sprite1.png").convert_alpha() 
        if VAR.zoom > 1: VAR.image["joueur0"] = pygame.transform.scale(VAR.image["joueur0"], (VAR.image["joueur0"].get_width() * VAR.zoom, VAR.image["joueur0"].get_height() * VAR.zoom)) 
        
        VAR.image["objets"] = pygame.image.load("images/objets.png").convert_alpha() 
        if VAR.zoom > 1: VAR.image["objets"] = pygame.transform.scale(VAR.image["objets"], (VAR.image["objets"].get_width() * VAR.zoom, VAR.image["objets"].get_height() * VAR.zoom)) 
        VAR.image["explosion"] = pygame.image.load("images/explosion2.png").convert_alpha() 
        if VAR.zoom > 1: VAR.image["explosion"] = pygame.transform.scale(VAR.image["explosion"], (VAR.image["explosion"].get_width() * VAR.zoom, VAR.image["explosion"].get_height() * VAR.zoom)) 
        
        VAR.image["avatar0"] = pygame.image.load("images/avatar_blanc.png").convert_alpha() 
        VAR.image["avatar1"] = pygame.image.load("images/avatar_noir.png").convert_alpha() 
        VAR.image["avatar2"] = pygame.image.load("images/avatar_rouge.png").convert_alpha() 
        VAR.image["avatar3"] = pygame.image.load("images/avatar_jaune.png").convert_alpha() 
        VAR.image["avatar4"] = pygame.image.load("images/avatar_bleu.png").convert_alpha() 
        VAR.image["avatar5"] = pygame.image.load("images/avatar_vert.png").convert_alpha() 
        VAR.image["avatar6"] = pygame.image.load("images/avatar_ciel.png").convert_alpha() 
        VAR.image["avatar7"] = pygame.image.load("images/avatar_rose.png").convert_alpha() 

        VAR.image[C_OBJET.BOMBE] =        FCT.image_decoupe(VAR.image["objets"], 0, 0, VAR.tailleCellule, VAR.tailleCellule  )
        VAR.image[C_OBJET.COUP_PIED] =    FCT.image_decoupe(VAR.image["objets"], 1, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[C_OBJET.ROLLER] =       FCT.image_decoupe(VAR.image["objets"], 2, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[C_OBJET.FLAMME] =       FCT.image_decoupe(VAR.image["objets"], 3, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[C_OBJET.COUP_POING] =   FCT.image_decoupe(VAR.image["objets"], 4, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[C_OBJET.MALADIE] =      FCT.image_decoupe(VAR.image["objets"], 5, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[C_OBJET.SUPER_FLAMME] = FCT.image_decoupe(VAR.image["objets"], 6, 0, VAR.tailleCellule, VAR.tailleCellule )
        
        VAR.sons["poser_bombe"] = pygame.mixer.Sound('audios/bomb.wav')
        VAR.sons["prendre_objet"] = pygame.mixer.Sound('audios/prendre.wav')
        VAR.sons["explosion"] = pygame.mixer.Sound('audios/boom2.wav')
    
    def Charge_Musique(self, _fichier):  
        pygame.mixer.music.load("musics/" + _fichier + ".mp3")
        
        
        
    def Demarrer(self):
        VAR.fenetre = pygame.display.set_mode(VAR.resolution, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBomber 0.1")        
        self.horloge = pygame.time.Clock()
        
        self.Chargement_Ressources()
        self.Charge_Musique(random.choice(['78','41','25']) )
        self.Initialisation()
        self.Boucle()
        
    def Relancer_Une_Partie(self):
        
        self.BOMBES.Initialiser()
        self.OBJETS.Initialiser()
        self.TERRAIN.Initialiser()
        self.JOUEURS.Reinitaliser()
        
        self.Charge_Musique(random.choice(['78','41','25']) )
        pygame.mixer.music.play()
        
        VAR.temps_jeu = time.time()
        VAR.pause = False
        self.nbSecondes_Restantes_AvPause = -1
    
    def Arreter_Partie(self):
        self.nbSecondes_Restantes_AvPause = self.tempsRestant() 
        VAR.pause = True
    
    def Reprendre_Partie(self):         
        VAR.temps_jeu = time.time() - self.nbSecondes_Restantes_AvPause
        self.nbSecondes_Restantes_AvPause = -1
        VAR.pause = False
        
        
    def tempsRestant(self):
        if VAR.pause:
            nbSecondes = self.nbSecondes_Restantes_AvPause
        else:
            nbSecondes = int(VAR.duree_partie - (time.time() - VAR.temps_jeu))
        if nbSecondes < 0: nbSecondes = 0            
        return nbSecondes
    
 
         
    def Boucle(self):
        pygame.mixer.music.play()
        
        
        VAR.temps_jeu = time.time()
        
        VAR.boucle_jeu = True
        while VAR.boucle_jeu:
            self.CONTROLLEUR.Gestion_Utilisateurs()
            
            if self.phase_jeu != C_PHASE_DE_JEU.JEU:
                self.INTERFACE.Afficher()
   
            else:                

                # --- remplissage de la fenetre avec une couleur proche du noir
                self.INTERFACE.Afficher_Fond()
                # --- afficher le résultat
                self.INTERFACE.Afficher_Barre_Information_Partie()
                
                self.TERRAIN.Afficher()  
                
                self.BOMBES.Afficher_Toutes_Les_Bombes()
                self.OBJETS.Afficher_Tous_Les_Objets()
                
                self.PARTICULES.Afficher_Les_Particules()
                self.JOUEURS.Afficher_Tous_Les_Joueurs()
                
                self.TERRAIN.TimeOut_Resserage_Du_Terrain()   
    
                if self.JOUEURS.nbJoueurs_enVie() == 1:                    
                    self.INTERFACE.Victoire_Afficher()
                    
                
                   
                    
            

            
            
            pygame.display.update()
            self.horloge.tick(60)     
               

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 