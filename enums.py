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
    
class C_PHASE_DE_JEU(Enum):
    TITRE = 0
    MENU = 1
    JEU = 2
    HIGH_SCORE = 3
    
class C_ETAPE_BOMBE(Enum):
    VA_PETER = 0
    EXPLOSE = 1
    A_EXPLOSE = 2
    
class C_MESSAGE(Enum):
    NON_INITIALISE = 0
    INITIALISE = 1
    SCROLLX = 2
    EN_ATTENTE_START = 3
    COMPTE_A_REBOURS = 4
    TERMINE = 5
    
class C_TERRAIN(Enum):
    SOL = 0
    CASSABLE = 1
    MUR = 2
    BLOC = 3