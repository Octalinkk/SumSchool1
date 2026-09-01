import pygame
from pygame import Vector2
import math
from typing import List
from shape import Shape
from supTriangle import supTriangle

class supCircle(Shape):
    
    def __init__(self, x: float, y: float, color: tuple):
        super().__init__(x, y, color)
        self.radius = 5
        self.numSegments = 7  # Nombre de triangles pour former le cercle
        self.triangles: List[supTriangle] = []
    
    def _generateTriangles(self) -> None:
        """Crée des triangles en éventail pour former un cercle"""
        center = Vector2(self.x, self.y)
        
        for i in range(self.numSegments):
            # Calculer les angles pour les 2 points du périmètre
            angle1 = (i / self.numSegments) * 2 * math.pi
            angle2 = ((i + 1) / self.numSegments) * 2 * math.pi
            
            # Calculer les points sur le périmètre
            point1 = Vector2(
                self.x + self.radius * math.cos(angle1),
                self.y + self.radius * math.sin(angle1)
            )
            point2 = Vector2(
                self.x + self.radius * math.cos(angle2),
                self.y + self.radius * math.sin(angle2)
            )
            
            # Créer un triangle : (centre, point1, point2)
            tri = supTriangle(center, point1, point2)
            self.triangles.append(tri)
    
    def draw(self, screen: pygame.Surface, color: tuple, rotation: float) -> None:
        if not self.triangles:
            self._generateTriangles()
        
        for tri in self.triangles:
            tri.draw(screen, color, rotation)
    
    def erase(self, screen: pygame.Surface, rotation: float) -> None:
        self.draw(screen, (0, 0, 0), rotation)
    
    def move(self, offset: Vector2) -> None:
        self.x += offset.x
        self.y += offset.y
        for tri in self.triangles:
            tri.move(offset)