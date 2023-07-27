import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))


print("Nombre de manettes connectées :", num_joysticks)

MANETTES = []
for i in range(num_joysticks):
    MANETTES.append(pygame.joystick.Joystick(i))
    pygame.joystick.Joystick(i).init()
    
    print("Manette "+str(i)+" :", pygame.joystick.Joystick(i).get_name())
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,255,0))
    for manette in MANETTES:
        axis_x = manette.get_axis(0)
        axis_y = manette.get_axis(1)
        print(manette, axis_x, axis_y)
    pygame.display.flip()


pygame.quit()