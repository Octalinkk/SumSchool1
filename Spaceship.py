from pygame import Vector2, draw
import math

class SpaceShip():
    def __init__(self, target:Vector2, distance:int, angRad:float):
        self.targetPos = target
        self.dist = distance
        self.angle = angRad
        self.origin = self.calcOrigin()

    def degToRad(self, angle):
        return angle * math.pi / 180

    def drawShip(self, screen):
        sideLen = 70
        angleBody = self.degToRad(15)
        point1 = Vector2(self.origin.x + sideLen * math.cos(angleBody + self.angle), self.origin.y + sideLen * math.sin(angleBody + self.angle))
        point2 = Vector2(self.origin.x + sideLen * math.cos(-(angleBody - self.angle)), self.origin.y + sideLen * math.sin(-(angleBody - self.angle )))
        draw.polygon(screen, (255, 255, 0), [self.origin, point1, point2])

    def calcOrigin(self) -> Vector2:
        x = self.targetPos.x + self.dist * math.cos(self.angle)
        y = self.targetPos.y + self.dist * math.sin(self.angle)
        return Vector2(x, y)