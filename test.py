import pygame
import numpy as np

# Charger votre matrice heightmap depuis une source de données, par exemple une image
# Remplacez "heightmap_data" par votre propre matrice ou fichier de données
heightmap_data = np.random.randint(0, 256, size=(100, 100))

# Dimensions de la heightmap
heightmap_width = len(heightmap_data[0])
heightmap_height = len(heightmap_data)

# Dimensions de la fenêtre
window_width = 800
window_height = 600

# Taille d'une cellule dans la heightmap (vous pouvez ajuster cette valeur en fonction de vos besoins)
cell_size = 8

# Initialisation de Pygame
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Fonction pour dessiner la heightmap visible sur la fenêtre
def draw_heightmap():
    for y in range(heightmap_y_offset, heightmap_y_offset + window_height // cell_size + 1):
        for x in range(heightmap_width):
            # Calculer les coordonnées d'affichage de la cellule
            cell_x = x * cell_size
            cell_y = (y - heightmap_y_offset) * cell_size

            # Obtenir la hauteur de la cellule depuis la matrice heightmap_data
            height = heightmap_data[y % heightmap_height][x]

            # Dessiner un rectangle rempli avec une couleur en fonction de la hauteur
            pygame.draw.rect(window, (height, height, height), (cell_x, cell_y, cell_size, cell_size))

# Boucle principale
running = True
heightmap_y_offset = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Effacer l'écran avant de dessiner la nouvelle frame
    window.fill((0, 0, 0))

    # Dessiner la heightmap visible sur la fenêtre
    draw_heightmap()

    # Mettre à jour la position de la heightmap pour le scrolling vertical
    heightmap_y_offset += 1
    if heightmap_y_offset >= heightmap_height:
        heightmap_y_offset = 0

    # Rafraîchir l'affichage
    pygame.display.flip()

    # Réguler la vitesse d'affichage
    clock.tick(10)

pygame.quit()