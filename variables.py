from pygame.locals import *

image = {}
sons = {}
temps_jeu = -1
boucle_jeu = True
pause = False
offSet = (0, 0)

animation_MortFrameMax = 5    


fullHd = False
plein_ecran = False

resolution = (1320, 768)
mode_ecran = DOUBLEBUF

if fullHd: resolution = (1920, 1080)
if plein_ecran: mode_ecran = FULLSCREEN

zoom = 3

tailleCellule = 16
nbLignes, nbColonnes = 13, 15
tauxRemplissage = 70
delaisExplosion = 3    

duree_partie = 15
nb_parties = 5
active_maladies = True
active_heritage = True

CLAVIER = {
    0: {"DROITE": K_d, "GAUCHE": K_q, "HAUT" : K_z, "BAS" : K_s, "ACTION1" : K_w, "ACTION2" : K_x},
    1: {"DROITE": K_RIGHT, "GAUCHE": K_LEFT, "HAUT" : K_UP, "BAS" : K_DOWN, "ACTION1" : K_l, "ACTION2" : K_m} }




    



# --- constantes
C_SOL = 0
C_MUR = 1
C_BLOC = 2
C_CASSABLE = 3


C_HORS_TERRAIN = (-2, -2)
C_AUCUNE_COLLISION = (-99, -99)











# --- code couleur joueurs
C_COLOR_TRANSPARENT = (255, 255, 255, 0)

C_COLOR_NOIR = (67, 56, 86)
C_COLOR_ROSE = (246, 143, 186)
C_COLOR_BLEU = (44, 97, 209)
C_COLOR_ROUGE = (231, 38, 41)
C_COLOR_JAUNE = (255, 237, 70)
C_COLOR_CIEL = (113, 185, 255)
C_COLOR_VERT = (140, 217, 101)

LISTE_COLOR_JOUEURS = [C_COLOR_NOIR, C_COLOR_ROUGE, C_COLOR_JAUNE, C_COLOR_BLEU, C_COLOR_VERT, C_COLOR_CIEL, C_COLOR_ROSE]

LISTE_COLOR_COEFF = {}
LISTE_COLOR_COEFF['(232, 232, 232, 255)'] = 1
LISTE_COLOR_COEFF['(176, 176, 176, 255)'] = 0.7
LISTE_COLOR_COEFF['(96, 96, 96, 255)'] = 0.4
LISTE_COLOR_COEFF['(88, 160, 248, 255)'] = 0.6
LISTE_COLOR_COEFF['(0, 0, 248, 255)'] = 0.5
LISTE_COLOR_COEFF['(0, 0, 88, 255)'] = 0.4

LISTE_COLOR = {}

        
