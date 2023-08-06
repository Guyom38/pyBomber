
import pygame
from pygame.locals import *

import threading, time

import variables as VAR
import fonctions as FCT

from enums import *

class CChargement(threading.Thread):
    def __init__(self):
        super(CChargement, self).__init__()
        self.arreter = False

    def run(self):
        etat = True
        while not self.arreter:
            VAR.image["chargement"] =  pygame.transform.scale(pygame.image.load("images/chargement.jpg").convert_alpha(), VAR.resolution)
            VAR.fenetre.blit(VAR.image['chargement'], (0, 0))
                
            if etat:
                VAR.image["chargement_titre"] =  pygame.image.load("images/chargement_titre.png").convert_alpha()
                VAR.fenetre.blit(VAR.image["chargement_titre"], (VAR.resolution[0] - VAR.image["chargement_titre"].get_width() - VAR.tailleCellule, VAR.resolution[1] - VAR.image["chargement_titre"].get_height() - VAR.tailleCellule))
            
            pygame.display.update()
            etat = not etat
            time.sleep(0.3) 

    def Arreter(self):
        self.arreter = True