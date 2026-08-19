from pygame import Vector2, draw
import math

class Triangle():
    def __init__(self, co1, co2, co3, color):
        self.coord = [co1, co2, co3]
        self.color = color
    def draw(self, screen):
        draw.polygon(screen, self.color, self.coord)


class SpaceShip():
    def __init__(self, target:Vector2, distance:int, angRad:float):
        self.targetPos = target
        self.dist = distance
        self.angle = angRad
        self.origin = self.calcOrigin()

          
        self.sideLen = 70
        self.angleBody = self.degToRad(15)

    def degToRad(self, angle):
        return angle * math.pi / 180

    def drawShip(self, screen):
        self.drawHead1(screen)
        self.drawWings1(screen)
        self.drawBody1(screen)

          


    def calcOrigin(self) -> Vector2:
        x = self.targetPos.x + self.dist * math.cos(self.angle)
        y = self.targetPos.y + self.dist * math.sin(self.angle)
        return Vector2(x, y)