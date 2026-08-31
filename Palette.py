from pygame import Color

class Palette():
    def __init__(self, color:str, accent:str, grads:list[int]):
        self.color = color
        self.accent = accent
        self.grads = grads

    def getPalette(self) -> list[Color]:
        colors = []

        for grad in self.grads:
            colors.append(self.getColor(grad))
        return colors


    def getColor(self, grad):
        if (self.color == "red"):
            return self.genRedColor(grad)
        if (self.color == "green"):
            return self.genGreenColor(grad)
        if (self.color == "blue"):
            return self.genBlueColor(grad)

    def genRedColor(self, grad):
        base = Color(255, 0, 0)
        if (self.accent == "light"):
            base.g = grad
            base.b = grad
        if (self.accent == "dark"):
            base.r -= grad
        if (self.accent == "normal"):            
            base.r -= int(grad/2)
            base.g = int(grad/2)
            base.b = int(grad/2)
        return base
    
    def genGreenColor(self, grad):
        base = Color(0, 255, 0)
        if (self.accent == "light"):
            base.r = grad
            base.b = grad
        if (self.accent == "dark"):
            base.g -= grad
        if (self.accent == "normal"):            
            base.r = int(grad/2)
            base.g -= int(grad/2)
            base.b = int(grad/2)
        return base
    
    def genBlueColor(self, grad):
        base = Color(0, 0, 255)
        if (self.accent == "light"):
            base.r = grad
            base.g = grad
        if (self.accent == "dark"):
            base.b -= grad
        if (self.accent == "normal"):            
            base.r = int(grad/2)
            base.g = int(grad/2)
            base.b -= int(grad/2)
        return base
        
        