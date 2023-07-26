import fonctions as FCT
import pygame
from pygame.locals import *

pygame.init()   

fenetre = pygame.display.set_mode((1024,768), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("PyBomber 0.1")        
horloge = pygame.time.Clock()

x, y = 0,0 
boucle_jeu = True
while boucle_jeu:
    fenetre.fill((16,16,16))
            # --- récupére l'ensemble des évènements
    for event in pygame.event.get():        
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: boucle_jeu = False        
                
        if event.type == KEYDOWN:  
            if event.key == K_UP: y-=1
            if event.key == K_DOWN: y+=1
            if event.key == K_LEFT: x-=1
            if event.key == K_RIGHT: x+=1
                
                           
    objet1 = (x, y, 40, 40)
    objet2 = (50, 40, 40, 40)

    if(FCT.Collision(objet1, objet2)):
        c1 = (255,255,0,0)
    else:
        c1 = (255, 0, 128, 0)

    pygame.draw.rect(fenetre, c1, objet1)
    
    
    pygame.draw.rect(fenetre, (255,0,255,0), objet2)
    
    pygame.display.update()
    horloge.tick(30)           

pygame.quit() 