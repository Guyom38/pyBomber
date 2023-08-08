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
import menu as CM
import ressources as CR
import chargement as CCH
import highscore as CH

import variables as VAR
import fonctions as FCT

from enums import *

import random, time

class CMoteur():
    def __init__(self):
        pygame.init()   
        pygame.mixer.init()
        
        
        
        self.PARTICULES = CP.CParticules(self) 
        self.INTERFACE = CI.CInterface(self)        
        self.TERRAIN = CT.CTerrain(self)   
        self.BOMBES = CBS.CBombes(self)   
        self.OBJETS = COS.CObjets(self)      
        self.JOUEURS = CJS.CJoueurs(self)
        self.CONTROLLEUR = CC.CCControlleur(self)           
        self.MENU = CM.CMenu(self) 
        self.HIGHSCORE = CH.CHighscore(self)
        
    def Initialisation(self): 
        VAR.zoom = 3
        
        self.chargement = CCH.CChargement()
        self.chargement.start()
           
        self.phase_jeu = C_PHASE_DE_JEU.MENU
        
        
        CR.Chargement_Ressources()    
        #CT.CTerrain.Reconfigurer_Terrain()
        
        self.INTERFACE.Initialiser()        
        self.TERRAIN.Initialiser()       
        self.BOMBES.Initialiser()
        self.OBJETS.Initialiser() 
        
        self.JOUEURS.Initialiser()
        self.CONTROLLEUR.Initialiser()
        self.MENU.Initialiser()
       
        self.chargement.Arreter()

    
    
    def Demarrer(self):
        VAR.fenetre = pygame.display.set_mode(VAR.resolution, VAR.mode_ecran, 32)
        pygame.display.set_caption("PyBomber 0.8")        
        self.horloge = pygame.time.Clock()        
        
        self.Initialisation()        
        self.Boucle()

       
    def Relancer_Une_Partie(self):
        VAR.zoom = 4
        CR.Changement_Zoom(VAR.zoom)  
          
        self.phase_jeu = C_PHASE_DE_JEU.JEU
        CT.CTerrain.Reconfigurer_Terrain()        
        
        self.BOMBES.Initialiser()
        self.OBJETS.Initialiser()
        self.TERRAIN.Initialiser()
        self.JOUEURS.Reinitaliser()
        
        FCT.Charge_Musique(random.choice(['78','41','25']) )      
        self.Reprendre_Partie(True)
        #FCT.jouer_sons("intro")

         
    def Boucle(self):
        
        VAR.temps_jeu = time.time()
        
        VAR.boucle_jeu = True
        while VAR.boucle_jeu:
            self.CONTROLLEUR.Gestion_Utilisateurs()
            
            if self.phase_jeu == C_PHASE_DE_JEU.MENU:
                self.MENU.Afficher_Menu() 
                
            elif self.phase_jeu == C_PHASE_DE_JEU.HIGH_SCORE:
                self.HIGHSCORE.Afficher_Highscore()
                
            elif self.phase_jeu == C_PHASE_DE_JEU.JEU:            

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
        
        
    def Arreter_Partie(self):
        self.nbSecondes_Restantes_AvPause = self.tempsRestant() 
        VAR.pause = True

    
    def Reprendre_Partie(self, _nouvelle): 
        VAR.temps_jeu = time.time() 
        if not _nouvelle: VAR.temps_jeu -= self.nbSecondes_Restantes_AvPause
        self.nbSecondes_Restantes_AvPause = -1
        VAR.pause = False
        
        
    def tempsRestant(self):
        if VAR.pause:
            nbSecondes = self.nbSecondes_Restantes_AvPause
        else:
            nbSecondes = int(VAR.duree_partie - (time.time() - VAR.temps_jeu))
        if nbSecondes < 0: nbSecondes = 0            
        return nbSecondes