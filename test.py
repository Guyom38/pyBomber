import pygame
from pygame.locals import *
import cairosvg


def convert_svg_to_png(svg_path, png_path, scale=1.0):
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)


pygame.init()   
fenetre = pygame.display.set_mode((1024,768), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("test")        
horloge = pygame.time.Clock()


svg_file = "images/701986.svg"
png_file = "images/output.png"
convert_svg_to_png(svg_file, png_file, scale=0.5)  # You can adjust the scale as needed

image = pygame.image.load(png_file)

  


boucle_jeu = True
while boucle_jeu:
            
    for event in pygame.event.get():        
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: boucle_jeu = False        

    fenetre.fill((16,16,16))


    fenetre.blit(image, (100, 100))  # Afficher l'image vectorielle à une position donnée


    pygame.display.update()
    horloge.tick(25)           

pygame.quit() 