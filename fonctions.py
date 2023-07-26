import pygame
from pygame.locals import *

import variables as VAR


def jouer_sons(_fichier):
    #VAR.sons[_fichier].play()
    pass

def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
    tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
    tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                        
    # --- Colle le decors 
    if dimxZ != -1 and dimyZ != -1:   
        tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
    return tmp




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