import math
import random
from Planet import Planet
from pygame import Vector2
from EquiTriangle import EquiTriangle
from Palette import Palette


class Ring():
    def __init__(self, planet:Planet):
        self.origin:Vector2 = planet.origin
        self.radius:Vector2 = int(planet.radius + planet.radius / 5)
        self.seed = planet.seed
        self.allPoints:list[Vector2] = self.calcRingPoints()
        self.upperPoints:list[Vector2] = [point for point in self.allPoints if point.x > self.origin.x]
        self.lowerPoints:list[Vector2] = [point for point in self.allPoints if point.x <= self.origin.x]
        self.rotate()

    def calcRingPoints(self) -> list[Vector2]:
        rng = random.Random(self.seed)
        rngRadius = rng.randint(10, self.radius)
        points = []
        for angle in range(360):
            x = self.origin.x + rngRadius * math.cos(math.radians(angle))
            y = self.origin.y + self.radius * math.sin(math.radians(angle))
            points.append(Vector2(x, y)) 

        return points

    def rotate(self):        
        rng = random.Random(self.seed)
        rngAngle = rng.randint(-120, 120)
        for index, point in enumerate(self.upperPoints):
            new = Vector2(
                self.origin.x + ((point.x - self.origin.x) * math.cos(rngAngle) - (point.y - self.origin.y) * math.sin(rngAngle)), 
                self.origin.y + ((point.x - self.origin.x) * math.sin(rngAngle) + (point.y - self.origin.y) * math.cos(rngAngle))
            )
            self.upperPoints[index] = new
        for index, point in enumerate(self.lowerPoints):
            new = Vector2(
                self.origin.x + ((point.x - self.origin.x) * math.cos(rngAngle) - (point.y - self.origin.y) * math.sin(rngAngle)), 
                self.origin.y + ((point.x - self.origin.x) * math.sin(rngAngle) + (point.y - self.origin.y) * math.cos(rngAngle))
            )
            self.lowerPoints[index] = new



    def drawUpperRing(self, screen, palette:Palette):
        for point in self.upperPoints:
            EquiTriangle(point, 5, 0, palette.getPalette()[self.upperPoints.index(point)]).draw(screen)

    def drawLowerRing(self, screen, palette:Palette):
            for point in self.lowerPoints:
                EquiTriangle(point, 5, 0, palette.getPalette()[self.lowerPoints.index(point)]).draw(screen)
        