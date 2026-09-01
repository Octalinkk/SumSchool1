import pygame
import random
from pygame import Vector2
from typing import List
from supTriangle import supTriangle

class Asteroid:
    
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius
        self.numPoints = random.randint(5, 10)
        self.pointOffsets = self._generatePointOffsets()  # Offsets par rapport au centre
    
    def _generatePointOffsets(self) -> List[Vector2]:
        """Génère des points aléatoires sur le périmètre d'un carré"""
        points = []
        half_radius = self.radius / 2
        
        for _ in range(self.numPoints):
            # Choisir un côté du carré aléatoirement
            side = random.randint(0, 3)
            
            if side == 0:  # Haut
                x = random.uniform(-half_radius, half_radius)
                y = -half_radius
            elif side == 1:  # Droite
                x = half_radius
                y = random.uniform(-half_radius, half_radius)
            elif side == 2:  # Bas
                x = random.uniform(-half_radius, half_radius)
                y = half_radius
            else:  # Gauche
                x = -half_radius
                y = random.uniform(-half_radius, half_radius)
            
            points.append(Vector2(x, y))
        
        return points
    
    def draw(self, screen: pygame.Surface, x: float, y: float, radius: float, color: tuple, rotation: float) -> None:
        center = Vector2(x, y)
        
        # Créer les triangles en éventail
        for i in range(len(self.pointOffsets)):
            point1 = Vector2(x + self.pointOffsets[i].x, y + self.pointOffsets[i].y)
            point2 = Vector2(x + self.pointOffsets[(i + 1) % len(self.pointOffsets)].x, 
                           y + self.pointOffsets[(i + 1) % len(self.pointOffsets)].y)
            
            tri = supTriangle(center, point1, point2, color)
            tri.rotate(center, rotation)
            tri.draw(screen, color, rotation)
    
    def erase(self, screen: pygame.Surface, x: float, y: float, radius: float, rotation: float) -> None:
        self.draw(screen, x, y, radius, (0, 0, 0), rotation)
    
    def move(self, offset: Vector2) -> None:
        self.x += offset.x
        self.y += offset.y