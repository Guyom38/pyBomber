
import pygame
from pygame.locals import *

import threading, time

import variables as VAR
import fonctions as FCT

from enums import *


            
            





def Chargement_Ressources():

    

    VAR.tailleCellule = 16 * VAR.zoom
        
    tmp = pygame.image.load("images/titre.jpg").convert_alpha() 
    tmp = pygame.transform.scale(tmp, (VAR.resolution[0], VAR.resolution[1]))
    VAR.image['titre'] = tmp
    
    tmp = pygame.image.load("images/R.jpg").convert_alpha() 
    tmp = pygame.transform.scale(tmp, (VAR.resolution[0], VAR.resolution[1]))
    VAR.image['r'] = tmp
        
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
    VAR.image["start"] = pygame.image.load("images/start.png").convert_alpha() 
    

    
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
    
    VAR.sons["menu_clic"] = pygame.mixer.Sound('audios/menu_clic.wav')
    VAR.sons["menu_select"] = pygame.mixer.Sound('audios/menu_select.wav')  
    
    VAR.sons["bloc_timeout"] = pygame.mixer.Sound('audios/bloc_timeout.wav')    
    VAR.sons["intro"] = pygame.mixer.Sound('audios/intro.wav')    
    VAR.sons["tete_mort"] = pygame.mixer.Sound('audios/tete_mort.wav')
    

    