from pygame import Vector2
from Circle import Circle

class Planet():
    def __init__(self, origin:Vector2, radius:int):
        self.origin:Vector2 = origin
        self.radius:Vector2 = radius
        self.triangles = Circle(self.radius, self.origin, 360).calcCircleOfTriangles()

    def drawPlanet(self, screen):
        for triangle in self.triangles:
            triangle.draw(screen)