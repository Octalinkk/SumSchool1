import pygame
from pygame import Vector2
from EquiTriangle import EquiTriangle

from perlin_noise import PerlinNoise


class Planet():
    def __init__(self, origin:Vector2, radius:int, seed:int):
        self.origin:Vector2 = origin
        self.radius:Vector2 = radius
        self.seed = seed
        # Gen patern at inst to not lag the heck out of the program
        self.noiseMap = self.genNoiseMap()        
        self.triangles = self.genNoiseTriangles()

    def drawPlanet(self, screen):
        for triangle in self.triangles:
            triangle.draw(screen)

    def genNoiseMap(self):
        noise = PerlinNoise(octaves=2, seed=self.seed)
        # Gen a noise map the size of the planet (Square)
        return [[noise([x / self.radius*2, y / self.radius*2]) for y in range(self.radius*2)] for x in range(self.radius*2)]

    def getNoiseValue(self, x, y):
        return self.noiseMap[y][x]

    def getMaskedColor(self, x, y):
        PALETTE = [            
            (0.3,  (17, 47, 130)),   # deep blue
            (0.6,  (30, 60, 200)),    # blue
            (0.85, (37, 196, 88)),    # green
            (1.01, (17, 130, 53)),    # deep green 
        ]
        v = self.getNoiseValue(x, y) + 0.5 # Bring the fork from +- 0.5 to 0->1
        t = max(0.0, min(1.0, v))

        for seuil, couleur in PALETTE:
            if t < seuil:
                return couleur
        return PALETTE[-1][1]
        

    def genNoiseTriangles(self): 

        tris:list[EquiTriangle] = []
        for y in range(self.radius *2):
            for x in range(self.radius *2):
                dx = x - self.radius
                dy = y - self.radius
                if dx * dx + dy * dy <= self.radius * self.radius: # Only compute patern inside the circle
                    couleur = self.getMaskedColor(x, y)
                    tris.append(EquiTriangle(Vector2((self.origin.x + x)-self.radius, (self.origin.y + y)-self.radius), 1, 0, couleur))
        return tris
                    
