import pygame
import pygame.midi
from pygame.locals import *

from Classes.terrrain import *
from Classes.joueur import *
from Classes.bombe import *
from Classes.particules import *
from Classes.controlleur import *

import variables as VAR
import fonctions as FCT
import pygame.mixer

class CMoteur():
    def __init__(self):
        pygame.init()   
        pygame.mixer.init()

    
    def Initialisation(self):
        self.Chargement_Ressources()
        
        
        self.TERRAIN = CTerrain(self)              
        self.JOUEURS = CJoueurs(self)
        self.CONTROLLEUR = CCControlleur(self)
        
        self.PARTICULES = CParticules(self)
        
        
        self.BOMBES = CBombes(self)   
        self.OBJETS = CObjets(self)
       
        
        
        VAR.offSet = ( (VAR.resolution[0] - (VAR.nbColonnes* VAR.tailleCellule)) /2,
                        (VAR.resolution[1] - (VAR.nbLignes* VAR.tailleCellule)) /2 )
        
        #self.CONTROLLEUR.Creer_Joueurs_Clavier_Manettes()
        
    
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
     
        
        VAR.image[VAR.C_OBJ_BOMBE] = FCT.image_decoupe(VAR.image["objets"], 0, 0, VAR.tailleCellule, VAR.tailleCellule  )
        VAR.image[VAR.C_OBJ_COUP] = FCT.image_decoupe(VAR.image["objets"], 1, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[VAR.C_OBJ_ROLLER] = FCT.image_decoupe(VAR.image["objets"], 2, 0, VAR.tailleCellule, VAR.tailleCellule )
        VAR.image[VAR.C_OBJ_FLAMME] = FCT.image_decoupe(VAR.image["objets"], 3, 0, VAR.tailleCellule, VAR.tailleCellule )
        
        VAR.sons["poser_bombe"] = pygame.mixer.Sound('audios/bomb.wav')
        VAR.sons["prendre_objet"] = pygame.mixer.Sound('audios/prendre.wav')
         
        pygame.mixer.music.load("musics/" + choice(['78','41','25']) + ".mp3")
        
    def Demarrer(self):
        VAR.fenetre = pygame.display.set_mode(VAR.resolution, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("PyBomber 0.1")        
        self.horloge = pygame.time.Clock()
        
        self.Initialisation()
        self.Boucle()
        
    def Boucle(self):
        pygame.mixer.music.play()
        
        VAR.boucle_jeu = True
        while VAR.boucle_jeu:
            self.CONTROLLEUR.Gestion_Utilisateurs()

            # --- remplissage de la fenetre avec une couleur proche du noir
            VAR.fenetre.fill((16,16,16))
            self.TERRAIN.Afficher()  
            
            self.BOMBES.Afficher_Toutes_Les_Bombes()
            self.OBJETS.Afficher_Tous_Les_Objets()
            
            self.PARTICULES.Afficher_Les_Particules()
            self.JOUEURS.Afficher_Tous_Les_Joueurs()
            
            
            # --- afficher le résultat
            pygame.display.update()

            # --- limite la fréquence de raffraichissement a 25 images seconde
            self.horloge.tick(60)           
               

        # --- en sortie de boucle, quitte le programme
        pygame.quit() 