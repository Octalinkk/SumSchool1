import pygame
from pygame import Vector2
from typing import List
from shape import Shape
from supTriangle import supTriangle

class supSquare(Shape):
    
    def __init__(self, x: float, y: float, color: tuple):
        super().__init__(x, y, color)
        self.width = 10
        self.triangles: List[supTriangle] = []
    
    def _generateTriangles(self) -> None:
        """Crée 2 triangles qui forment un carré"""
        half_width = self.width / 2
        
        # Triangle 1 : coin supérieur-droit
        vec1 = Vector2(self.x - half_width, self.y - half_width)
        vec2 = Vector2(self.x + half_width, self.y - half_width)
        vec3 = Vector2(self.x + half_width, self.y + half_width)
        tri1 = supTriangle(vec1, vec2, vec3)
        
        # Triangle 2 : coin inférieur-gauche
        vec1 = Vector2(self.x - half_width, self.y - half_width)
        vec2 = Vector2(self.x + half_width, self.y + half_width)
        vec3 = Vector2(self.x - half_width, self.y + half_width)
        tri2 = supTriangle(vec1, vec2, vec3)
        
        self.triangles = [tri1, tri2]
    
    def draw(self, screen: pygame.Surface, color: tuple, rotation: float) -> None:
        if not self.triangles:
            self._generateTriangles()
        
        for tri in self.triangles:
            tri.rotate(Vector2(self.x, self.y), rotation)
            tri.draw(screen, color, rotation)
    
    def erase(self, screen: pygame.Surface, rotation: float) -> None:
        self.draw(screen, (0, 0, 0), rotation)
    
    def move(self, offset: Vector2) -> None:
        self.x += offset.x
        self.y += offset.y
        for tri in self.triangles:
            tri.move(offset)