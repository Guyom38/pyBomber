
import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

from enums import *


def Charger_Images_FULL(_tag, _fichier):
    tmp = pygame.image.load("images/" + _fichier).convert_alpha() 
    tmp = pygame.transform.scale(tmp, (VAR.resolution[0], VAR.resolution[1]))
    VAR.image[_tag] = tmp
    return tmp
    
def Charger_Images_ZOOM(_tag, _fichier, _zoom):
    tmp = pygame.image.load("images/" + _fichier).convert_alpha() 
    if _zoom > 1: tmp = pygame.transform.scale(tmp, (tmp.get_width() * _zoom, tmp.get_height() *_zoom))  
    VAR.image[_tag] = tmp
    return tmp
    
def Chargement_Ressources():
    
    
    VAR.sons["sloggan"] = pygame.mixer.Sound('audios/sloggan.wav')
    FCT.jouer_sons("sloggan")
    
    Charger_Images_FULL("titre", "titre.jpg")
    Charger_Images_FULL("r", "R.jpg") 
    
    Changement_Zoom(VAR.zoom)
    Chargement_Audios()
   
    VAR.image["start"] = pygame.image.load("images/start.png").convert_alpha() 
    VAR.image["avatar0"] = pygame.image.load("images/avatar_blanc.png").convert_alpha() 
    VAR.image["avatar1"] = pygame.image.load("images/avatar_noir.png").convert_alpha() 
    VAR.image["avatar2"] = pygame.image.load("images/avatar_rouge.png").convert_alpha() 
    VAR.image["avatar3"] = pygame.image.load("images/avatar_jaune.png").convert_alpha() 
    VAR.image["avatar4"] = pygame.image.load("images/avatar_bleu.png").convert_alpha() 
    VAR.image["avatar5"] = pygame.image.load("images/avatar_vert.png").convert_alpha() 
    VAR.image["avatar6"] = pygame.image.load("images/avatar_ciel.png").convert_alpha() 
    VAR.image["avatar7"] = pygame.image.load("images/avatar_rose.png").convert_alpha() 

def Chargement_Audios():   
    VAR.sons["poser_bombe"] = pygame.mixer.Sound('audios/bomb.wav')
    VAR.sons["prendre_objet"] = pygame.mixer.Sound('audios/prendre.wav')
    VAR.sons["explosion"] = pygame.mixer.Sound('audios/boom2.wav')
    
    VAR.sons["menu_clic"] = pygame.mixer.Sound('audios/menu_clic.wav')
    VAR.sons["menu_select"] = pygame.mixer.Sound('audios/menu_select.wav')  
    
    VAR.sons["bloc_timeout"] = pygame.mixer.Sound('audios/bloc_timeout.wav')    
    VAR.sons["intro"] = pygame.mixer.Sound('audios/intro.wav')    
    VAR.sons["tete_mort"] = pygame.mixer.Sound('audios/tete_mort.wav')
    
    VAR.sons["pet"] = pygame.mixer.Sound('audios/pet.wav')
    
    
def Changement_Zoom(_zoom):  
    VAR.tailleCellule = VAR.pixelBloc * _zoom
    
    
    # --- Decors
    Charger_Images_ZOOM("decors", "decors.png", _zoom)
    VAR.image["cassable"] = FCT.image_decoupe(VAR.image["decors"], 0, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["cassable0"] = FCT.image_decoupe(VAR.image["decors"], 1, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["cassable1"] = FCT.image_decoupe(VAR.image["decors"], 2, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["cassable2"] = FCT.image_decoupe(VAR.image["decors"], 2, 1, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["sol0"] = FCT.image_decoupe(VAR.image["decors"], 0, 2, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["sol1"] = FCT.image_decoupe(VAR.image["decors"], 0, 2, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["ombre"] = FCT.image_decoupe(VAR.image["decors"], 1, 2, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image["mur"] = FCT.image_decoupe(VAR.image["decors"], 0, 1, VAR.tailleCellule, VAR.tailleCellule )
    
    Charger_Images_ZOOM("objets", "objets.png", _zoom)
    VAR.image[C_OBJET.BOMBE] =        FCT.image_decoupe(VAR.image["objets"], 0, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.COUP_PIED] =    FCT.image_decoupe(VAR.image["objets"], 1, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.ROLLER] =       FCT.image_decoupe(VAR.image["objets"], 2, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.FLAMME] =       FCT.image_decoupe(VAR.image["objets"], 3, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.COUP_POING] =   FCT.image_decoupe(VAR.image["objets"], 4, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.MALADIE] =      FCT.image_decoupe(VAR.image["objets"], 5, 0, VAR.tailleCellule, VAR.tailleCellule )
    VAR.image[C_OBJET.SUPER_FLAMME] = FCT.image_decoupe(VAR.image["objets"], 6, 0, VAR.tailleCellule, VAR.tailleCellule )
    
    # --- Joueurs
    Charger_Images_ZOOM("joueur0", "sprite1.png", _zoom)
    Charger_Images_ZOOM("explosion", "explosion2.png", _zoom)
    

    
    
        
    
    
    
    
    
    
    
    
   

       
   

    