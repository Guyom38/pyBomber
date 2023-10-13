import pygame
from pygame.locals import *

import joueur as CJ
import variables as VAR
import time

from enums import *

class CCControlleur:
    def __init__(self, _moteur):
        self.MOTEUR = _moteur
        self.JOUEURS = _moteur.JOUEURS
        self.JOUEURS_WEBSOCKET = {}
        
        self.direction = None
        self.pression_temps = time.time()
        self.pression_delais = 1
        self.pression = False
        
        self.action_bouton = None
    
    #
    # --       
    def Initialiser(self):
        self.nbManettes = pygame.joystick.get_count() 
        
        self.MANETTES = []
        for i in range(self.nbManettes):
            self.MANETTES.append(pygame.joystick.Joystick(i))
            pygame.joystick.Joystick(i).init()            
            print("Manette "+str(i)+" :", pygame.joystick.Joystick(i).get_name())
        
        self.Creer_Joueurs_Clavier_Manettes()
    
    #
    # --
    # async def Boucle_Ecoute_WebSocket(self):
    #     self.JOUEURS_WEBSOCKET = {}
    #     print("Initialisation thread websocket")
      
    #     async with websockets.connect("wss://ws.ladnet.net") as websocket: #, extra_headers={'http_proxy_host': "haproxy", 'http_proxy_port': 3128}
    #         print(" + boucle thread websocket")
    #         while True:
    #             try:
                    
    #                 message = await websocket.recv()
    #                 data = json.loads(message)
    #                 print(str(data))
    #                 if 'playerId' in data:
                                            
    #                     idJoueurWS = int(data['playerId'])
    #                     print(str(idJoueurWS) + " => " + str(data))
                        
    #                     if idJoueurWS not in self.JOUEURS_WEBSOCKET:
    #                         self.JOUEURS_WEBSOCKET[idJoueurWS] = len(self.JOUEURS_WEBSOCKET) 
    #                         print("Nouveau Joueur #"+str(idJoueurWS)+" => id:" + str(self.JOUEURS_WEBSOCKET[idJoueurWS]))
                        
    #                     idJoueur = self.JOUEURS_WEBSOCKET[idJoueurWS]
    #                     seuil = 30
                        
                        
    #                     axis_x, axis_y, mouvementJoy = 0.0, 0.0, False                
    #                     if 'joystick' in data['data']:
    #                         axis_x, axis_y, mouvementJoy = float(data['data']['joystick']['x']), float(data['data']['joystick']['y']), True
                        
    #                     if not self.JOUEURS.LISTE[idJoueur].mort:                
    #                         if (mouvementJoy):
    #                             if round(axis_x,0) != 0 or round(axis_y,0) != 0: self.JOUEURS.LISTE[idJoueur].enMouvement = True 
                                
    #                             BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
    #                             if self.JOUEURS.LISTE[idJoueur].maladie == C_MALADIE.TOUCHES_INVERSEES:
    #                                 BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                                
    #                             if axis_x < -seuil: 
    #                                 self.JOUEURS.LISTE[idJoueur].direction = BONNE_DIRECTION[0]
    #                                 self.Menu_Pression_Touche(BONNE_DIRECTION[0])
    #                             if axis_x > seuil: 
    #                                 self.JOUEURS.LISTE[idJoueur].direction =  BONNE_DIRECTION[1]
    #                                 self.Menu_Pression_Touche(BONNE_DIRECTION[1])
    #                             if axis_y > seuil: 
    #                                 self.JOUEURS.LISTE[idJoueur].direction = BONNE_DIRECTION[2]
    #                                 self.Menu_Pression_Touche(BONNE_DIRECTION[2])
    #                             if axis_y < -seuil: 
    #                                 self.JOUEURS.LISTE[idJoueur].direction =  BONNE_DIRECTION[3]     
    #                                 self.Menu_Pression_Touche(BONNE_DIRECTION[3])  
                            
    #                         if 'button' in data['data']: 
    #                             if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.JEU:                         
    #                                 if (data['data']['button'] == 'B'):
    #                                     self.JOUEURS.LISTE[idJoueur].Action_Poser_Une_Bombe()
    #                                 if (data['data']['button'] == 'A'):
    #                                     self.JOUEURS.LISTE[idJoueur].Action_Pousser_La_Bombe()
                                
    #                             elif self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.MENU:
    #                                 if (data['data']['button'] == 'A'):
    #                                     self.action_bouton = True  
                                     
    #             except Exception as e:
    #                 print(f"Erreur: {e}")
                    
    #             await asyncio.sleep(0)
    
    def Traite_Actions_WebSocket(self):
    
            while not self.MOTEUR.actions_websocket.empty():
                try:
                    
                    data = self.MOTEUR.actions_websocket.get_nowait()
                    if 'playerId' in data:
                                            
                        idJoueurWS = int(data['playerId'])
                        print(str(idJoueurWS) + " => " + str(data))
                        
                        if idJoueurWS not in self.JOUEURS_WEBSOCKET:
                            self.JOUEURS_WEBSOCKET[idJoueurWS] = len(self.JOUEURS_WEBSOCKET) 
                            print("Nouveau Joueur #"+str(idJoueurWS)+" => id:" + str(self.JOUEURS_WEBSOCKET[idJoueurWS]))
                        
                        idJoueur = self.JOUEURS_WEBSOCKET[idJoueurWS]
                        seuil = 30
                        
                        
                        axis_x, axis_y, mouvementJoy = 0.0, 0.0, False                
                        if 'joystick' in data['data']:
                            axis_x, axis_y, mouvementJoy = float(data['data']['joystick']['x']), float(data['data']['joystick']['y']), True
                        
                        if not self.JOUEURS.LISTE[idJoueur].mort:                
                            if (mouvementJoy):
                                if round(axis_x,0) != 0 or round(axis_y,0) != 0: self.JOUEURS.LISTE[idJoueur].enMouvement = True 
                                
                                BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
                                if self.JOUEURS.LISTE[idJoueur].maladie == C_MALADIE.TOUCHES_INVERSEES:
                                    BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                                
                                if axis_x < -seuil: 
                                    self.JOUEURS.LISTE[idJoueur].direction = BONNE_DIRECTION[0]
                                    self.Menu_Pression_Touche(BONNE_DIRECTION[0])
                                if axis_x > seuil: 
                                    self.JOUEURS.LISTE[idJoueur].direction =  BONNE_DIRECTION[1]
                                    self.Menu_Pression_Touche(BONNE_DIRECTION[1])
                                if axis_y > seuil: 
                                    self.JOUEURS.LISTE[idJoueur].direction = BONNE_DIRECTION[2]
                                    self.Menu_Pression_Touche(BONNE_DIRECTION[2])
                                if axis_y < -seuil: 
                                    self.JOUEURS.LISTE[idJoueur].direction =  BONNE_DIRECTION[3]     
                                    self.Menu_Pression_Touche(BONNE_DIRECTION[3])  
                            
                            if 'button' in data['data']: 
                                if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.JEU:                         
                                    if (data['data']['button'] == 'B'):
                                        self.JOUEURS.LISTE[idJoueur].Action_Poser_Une_Bombe()
                                    if (data['data']['button'] == 'A'):
                                        self.JOUEURS.LISTE[idJoueur].Action_Pousser_La_Bombe()
                                
                                elif self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.MENU:
                                    if (data['data']['button'] == 'A'):
                                        self.action_bouton = True  
                                     
                except Exception as e:
                    print(f"Erreur: {e}")
                    
                     
    #
    # --           
    def Recherche_Manettes(self):
        if self.nbManettes != pygame.joystick.get_count():
            self.nbManettes = pygame.joystick.get_count() 
            self.Initialiser()
            return True
        return False
        
    def Menu_Pression_Touche(self, _direction):
        if time.time() - self.pression_temps > self.pression_delais:
            self.pression_temps = time.time()
            self.direction = _direction
            self.pression = True
        
        else:
            self.pression = False
              
    def Creer_Joueurs_Clavier_Manettes(self):
        self.JOUEURS.LISTE = []
        for i in range(8):
            self.JOUEURS.LISTE.append(CJ.CJoueur(self.MOTEUR, i, ""))  
        #self.JOUEURS.LISTE.append(CJ.CJoueur(self.MOTEUR, 8, ""))  
        for i in range(2, self.nbManettes):
            self.JOUEURS.LISTE.append(CJ.CJoueur(self.MOTEUR, i, ""))  
    
    def Gestion_Utilisateurs(self):
        # --- récupére l'ensemble des évènements
        for event in pygame.event.get():        
            if event.type == QUIT: VAR.boucle_jeu = False
            if event.type == KEYDOWN and event.key == K_ESCAPE: 
                if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.JEU:
                    self.MOTEUR.phase_jeu = C_PHASE_DE_JEU.MENU
                    self.MOTEUR.MENU.Initialiser()
                elif self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.MENU:
                    VAR.boucle_jeu = False
                
            self.Gestion_Manettes_Boutons(event)
                        
        # --- Gestion Clavier Joueur #1  
        self.Gestion_Clavier()
        self.Traite_Actions_WebSocket()
        
        # --- Gestion Manettes Joueur #1 a #9
        self.Gestion_Manettes_Directions()
    
    
    def Gestion_Clavier(self):
        for key, values in VAR.CLAVIER.items():
            if not self.JOUEURS.LISTE[key].mort:     
                BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
                if self.JOUEURS.LISTE[key].maladie == C_MALADIE.TOUCHES_INVERSEES:
                    BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                            
                keys = pygame.key.get_pressed()                    
                if keys[values["GAUCHE"]] == 1:
                    self.JOUEURS.LISTE[key].direction = BONNE_DIRECTION[0]
                    self.JOUEURS.LISTE[key].enMouvement = True
                    self.Menu_Pression_Touche(BONNE_DIRECTION[0])
                if keys[values["DROITE"]] == 1:
                    self.JOUEURS.LISTE[key].direction = BONNE_DIRECTION[1]
                    self.JOUEURS.LISTE[key].enMouvement = True
                    self.Menu_Pression_Touche(BONNE_DIRECTION[1])
                if keys[values["HAUT"]] == 1:
                    self.JOUEURS.LISTE[key].direction = BONNE_DIRECTION[2]
                    self.JOUEURS.LISTE[key].enMouvement = True
                    self.Menu_Pression_Touche(BONNE_DIRECTION[2])
                    
                if keys[values["BAS"]] == 1:
                    self.JOUEURS.LISTE[key].direction = BONNE_DIRECTION[3]
                    self.JOUEURS.LISTE[key].enMouvement = True
                    self.Menu_Pression_Touche(BONNE_DIRECTION[3])
                
    def Gestion_Manettes_Boutons(self, _event):
        for key, values in VAR.CLAVIER.items():
            if _event.type == KEYDOWN: 
                if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.JEU: 
                    if not self.JOUEURS.LISTE[key].mort:
                        if _event.key == values["ACTION1"]: 
                            self.JOUEURS.LISTE[key].Action_Poser_Une_Bombe()
                        if _event.key == values["ACTION2"]: 
                            self.JOUEURS.LISTE[key].Action_Pousser_La_Bombe()
                        
                elif self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.MENU:
                    if _event.key == values["ACTION1"]: 
                        self.action_bouton = True
                
                    
        if _event.type == pygame.JOYBUTTONDOWN:
            if self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.JEU: 
                if not self.JOUEURS.LISTE[_event.joy].mort:
                    if (_event.button == 2):
                        self.JOUEURS.LISTE[_event.joy].Action_Poser_Une_Bombe()
                    if (_event.button == 1):
                        self.JOUEURS.LISTE[_event.joy].Action_Pousser_La_Bombe()
            
            elif self.MOTEUR.phase_jeu == C_PHASE_DE_JEU.MENU:
                if (_event.button == 1):
                    self.action_bouton = True       
    
    def Gestion_Manettes_Directions(self):      
        
        for manette in self.MANETTES:
            axis_id, axis_x, axis_y = manette.get_id(), manette.get_axis(0), manette.get_axis(1)
            if not self.JOUEURS.LISTE[axis_id].mort:                
                if round(axis_x,0) != 0 or round(axis_y,0) != 0: self.JOUEURS.LISTE[axis_id].enMouvement = True 
                
                BONNE_DIRECTION = [C_DIRECTION.GAUCHE, C_DIRECTION.DROITE, C_DIRECTION.HAUT, C_DIRECTION.BAS]
                if self.JOUEURS.LISTE[axis_id].maladie == C_MALADIE.TOUCHES_INVERSEES:
                    BONNE_DIRECTION = [C_DIRECTION.DROITE, C_DIRECTION.GAUCHE, C_DIRECTION.BAS, C_DIRECTION.HAUT]
                
                if axis_x < -0.5: 
                    self.JOUEURS.LISTE[axis_id].direction = BONNE_DIRECTION[0]
                    self.Menu_Pression_Touche(BONNE_DIRECTION[0])
                if axis_x > 0.5: 
                    self.JOUEURS.LISTE[axis_id].direction =  BONNE_DIRECTION[1]
                    self.Menu_Pression_Touche(BONNE_DIRECTION[1])
                if axis_y < -0.5: 
                    self.JOUEURS.LISTE[axis_id].direction = BONNE_DIRECTION[2]
                    self.Menu_Pression_Touche(BONNE_DIRECTION[2])
                if axis_y > 0.5: 
                    self.JOUEURS.LISTE[axis_id].direction =  BONNE_DIRECTION[3]     
                    self.Menu_Pression_Touche(BONNE_DIRECTION[3])           