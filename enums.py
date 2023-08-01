from enum import Enum

class C_MALADIE(Enum):
    TOUCHES_INVERSEES = 1
    CHIASSE = 2
    BOMBES_A_RETARDEMENT = 3
    RALENTISSEMENT = 4
    FIGER = 5

class C_DIRECTION(Enum):
    BAS = 1
    GAUCHE = 2
    HAUT = 3
    DROITE = 4
    
class C_OBJET(Enum):
    BOMBE = 1
    COUP_PIED = 2
    ROLLER = 3
    FLAMME = 4
    COUP_POING = 5
    MALADIE = 6
    SUPER_FLAMME = 7