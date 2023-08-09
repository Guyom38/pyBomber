import variables as VAR

class CFoyer:
    def __init__(self, _x, _y, _imageY = 6):
        self.x = _x
        self.y = _y  
        self.imageY = _imageY   
        
    def ecranX(self): return VAR.offSet[0] + (self.x * VAR.tailleCellule) 
    def ecranY(self): return VAR.offSet[1] + (self.y * VAR.tailleCellule) 