import pygame
from pygame.locals import *

import variables as VAR
import time

def Animation(_frequence, _nbImages):
    return int((time.time()*_frequence) % _nbImages)
    
def jouer_sons(_fichier):
    VAR.sons[_fichier].play()


def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
    tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
    tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                        
    # --- Colle le decors 
    if dimxZ != -1 and dimyZ != -1:   
        tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
    return tmp

# -- image rempli de blanc, lorsque le joueur clignotte !    
def Colorisation_Masque(_image_masque, _couleurRemplacement = (255,255,255,255)):
    image = _image_masque.copy()
    
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            couleur = image.get_at((x, y))
            if not VAR.C_COLOR_TRANSPARENT == couleur:
                image.set_at((x,y), _couleurRemplacement)   
    return image

def image_vide(dimx, dimy):
    return pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)




def GenereMat2D(xDim, yDim, valeurDefaut):
    return [[valeurDefaut for x in range(xDim)] for i in range(yDim)]




def Collision(objet1, objet2):
    x1, y1, dx1, dy1 = objet1
    x2, y2, dx2, dy2 = objet2
    
    if ((x2 >= x1 + dx1) 
            or (x2 + dx2 <= x1) 
            or (y2 >= y1 + dy1)
            or (y2 + dy2 <= y1)):

        return False
    else:
        return True
  
  
LISTE_FONTS = {}
def Init_Texte(_taille):
    if not _taille in LISTE_FONTS:        
        LISTE_FONTS[_taille] = pygame.font.SysFont('PressStart2P', _taille) 
    
def Image_Texte(_texte, _couleur, _taille):
    Init_Texte(_taille) 
       
    image_texte = LISTE_FONTS[_taille].render(_texte, True, _couleur).convert_alpha()  
    return image_texte


def Position_Sur_Terrain(_x, _y):
    return (_x >=0 and _x < VAR.nbColonnes and _y >=0 and _y < VAR.nbLignes)