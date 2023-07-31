from enum import Enum

image = {}
sons = {}

resolution = (1320, 768)
zoom = 4
offSet = (0, 0)

boucle_jeu = True
phase_jeu = ""


nbLignes, nbColonnes = 13, 15 #int((resolution[1] /16)/2), int((resolution[0]/16)/2)-5 
tailleCellule = 16

tauxRemplissage = 70
delaisExplosion = 3    
    
animation_MortFrameMax = 5    


BONNE_DIRECTION = ['GAUCHE', 'DROITE', 'HAUT', 'BAS']

# --- constantes
C_SOL = 0
C_MUR = 1
C_CASSABLE = 2

C_HORS_TERRAIN = (-2, -2)
C_AUCUNE_COLLISION = (-99, -99)

C_OBJ_BOMBE = "BOMB"
C_OBJ_COUP_PIED = "COUP_PIED"
C_OBJ_ROLLER = "ROLLER"
C_OBJ_FLAMME = "FLAMME"
C_OBJ_COUP_POING = "COUP_POING"
C_OBJ_MALADIE = "MALADIE"
C_OBJ_SUPER_FLAMME = "SFLAMME"

class C_MALADIE(Enum):
    TOUCHES_INVERSEES = 1
    CHIASSE = 2
    BOMBES_A_RETARDEMENT = 3
    RALENTISSEMENT = 4
    FIGER = 5
    


# --- code couleur joueurs
C_COLOR_TRANSPARENT = (255, 255, 255, 0)
LISTE_COLOR = {}
#LISTE_COLOR['(0, 0, 1, 255)'] =       (0, 0, 1, 255) # Ombre
#LISTE_COLOR['(184, 0, 136, 255)'] =   (184, 0, 136, 255) # Pied
#LISTE_COLOR['(248, 56, 192, 255)'] =  (248, 56, 192, 255) # Pied
#LISTE_COLOR['(248, 248, 248, 255)'] = (248, 248, 248, 255) # Fond des yeux
#LISTE_COLOR['(160, 136, 80, 255)'] =  (160, 136, 80, 255) # Fond Lunette
#LISTE_COLOR['(248, 184, 144, 255)'] = (248, 184, 144, 255) # Fond Lunette

#LISTE_COLOR['(208, 56, 0, 255)'] =    (208, 56, 0, 255) # Contour Lunette

LISTE_COLOR['(232, 232, 232, 255)'] = [(232, 232, 232, 255), (80, 79, 80, 255),    (164, 0, 0, 255), (0, 0, 244, 255), (0, 244, 0, 255), (255, 216, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Casque1
LISTE_COLOR['(176, 176, 176, 255)'] = [(176, 176, 176, 255), (48, 49, 48, 255),    (141, 0, 0, 255), (0, 0, 227, 255), (0, 227, 0, 255), (160, 138, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Contour Casque2
LISTE_COLOR['(96, 96, 96, 255)'] =    [(96, 96, 96, 255),    (30, 30, 30, 255),    (130, 0, 0, 255), (0, 0, 187, 255), (0, 187, 0, 255), (128, 110, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Casque3 Ombre

#LISTE_COLOR['(160, 152, 160, 255)'] = [(160, 152, 160, 255), (160, 152, 160, 255), (80, 79, 80, 255), (80, 79, 80, 255), (80, 79, 80, 255), (80, 79, 80, 255), (80, 79, 80, 255), (80, 79, 80, 255)] # Bras Jambre

LISTE_COLOR['(88, 160, 248, 255)'] =  [(88, 160, 248, 255),  (33, 33, 33, 255),    (117, 0, 0, 255), (0, 0, 117, 255), (0, 117, 0, 255), (105, 90, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Ventre0
LISTE_COLOR['(0, 0, 248, 255)'] =     [(0, 0, 248, 255),     (25, 25, 24, 255),    (49, 0, 0, 255),  (0, 0, 49, 255), (0, 49, 0, 255), (87, 74, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Ventre1 Slip
LISTE_COLOR['(0, 0, 88, 255)'] =      [(0, 0, 88, 255),      (2, 2, 2, 255),       (36, 0, 0, 255),  (0, 0, 36, 255), (0, 36, 0, 255), (69, 59, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255)] # Ventre2