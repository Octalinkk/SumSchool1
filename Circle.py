from Triangle import Triangle
import math
from pygame import Vector2, draw

class Circle():
    def __init__(self, radius: int, pos: Vector2, details:int=36):
        self.radius = radius
        self.pos = pos
        self.details = details
        self.triangles = self.calcCircleOfTriangles()
        
    def calcCircleOfTriangles(self) -> list[Triangle]:
    
        positionX = self.pos.x
        positionY = self.pos.y
        triangles:list[Triangle] = []
    
        for i in range(self.details):
            angle1 = i * (2 * math.pi / self.details)
            angle2 = (i + 1) * (2 * math.pi / self.details)
            triangles.append(Triangle(Vector2(positionX, positionY),
                                            Vector2((positionX + self.radius * math.cos(angle1), positionY + self.radius * math.sin(angle1))),
            Vector2((positionX + self.radius * math.cos(angle2), positionY + self.radius * math.sin(angle2)))))
        return triangles

    