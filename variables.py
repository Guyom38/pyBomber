image = {}
sons = {}

resolution = (640, 480)
zoom = 2
offSet = (0, 0)

boucle_jeu = True

nbLignes, nbColonnes = 15, 21 #13, 15
tailleCellule = 16

tauxRemplissage = 70
    
    
    
    
# --- constantes
C_SOL = 0
C_MUR = 1
C_CASSABLE = 2

C_HORS_TERRAIN = (-2, -2)
C_AUCUNE_COLLISION = (-99, -99)

C_OBJ_BOMBE = "BOMB"
C_OBJ_COUP = "COUP"
C_OBJ_ROLLER = "ROLLER"
C_OBJ_FLAMME = "FLAMME"