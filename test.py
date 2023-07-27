import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))


img = pygame.image.load("images/sprite1.png").convert_alpha() 
img2 = pygame.image.load("images/sprite1.png").convert_alpha() 


# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
C_COLOR_TRANSPARENT = (255, 255, 255, 0)
# Boucle de jeu

LISTE_COLOR = {}
LISTE_COLOR['(0, 0, 1, 255)'] =       (0, 0, 1, 255) # Ombre
LISTE_COLOR['(184, 0, 136, 255)'] =   (184, 0, 136, 255) # Pied
LISTE_COLOR['(248, 56, 192, 255)'] =  (248, 56, 192, 255) # Pied
LISTE_COLOR['(248, 248, 248, 255)'] = (248, 248, 248, 255) # Fond des yeux
LISTE_COLOR['(160, 136, 80, 255)'] =  (160, 136, 80, 255) # Fond Lunette
LISTE_COLOR['(248, 184, 144, 255)'] = (248, 184, 144, 255) # Fond Lunette

LISTE_COLOR['(208, 56, 0, 255)'] =    (208, 56, 0, 255) # Contour Lunette

LISTE_COLOR['(232, 232, 232, 255)'] = (80, 79, 80, 255) # Casque1
LISTE_COLOR['(176, 176, 176, 255)'] = (48, 49, 48, 255) # Contour Casque2
LISTE_COLOR['(96, 96, 96, 255)'] =    (30, 30, 30, 255) # Casque3 Ombre

LISTE_COLOR['(160, 152, 160, 255)'] = (160, 152, 160, 255) # Bras Jambre

LISTE_COLOR['(88, 160, 248, 255)'] =  (33, 33, 33, 255) # Ventre0
LISTE_COLOR['(0, 0, 248, 255)'] =     (25, 25, 24, 255) # Ventre1 Slip
LISTE_COLOR['(0, 0, 88, 255)'] =      (2, 2, 2, 255) # Ventre2



def Colorisation(img):
    C_COLOR_TRANSPARENT = (255, 255, 255, 0)
    
    for y in range(img.get_height()):
        for x in range(img.get_width()):
            couleur = img.get_at((x, y))
            if not C_COLOR_TRANSPARENT == couleur:
                if str(couleur) in LISTE_COLOR:
                    img.set_at((x,y), LISTE_COLOR[str(couleur)])
       

Colorisation(img)


img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
img2 = pygame.transform.scale(img2, (img2.get_width() * 3, img2.get_height() * 3))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
      
    screen.blit(img, (10,10))        
    screen.blit(img2, (300,10))
    
    pygame.display.flip()


pygame.quit()