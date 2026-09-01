import pygame
from pygame import Vector2
import math
from shape import Shape

class supTriangle(Shape):
    
    def __init__(self, vec1, vec2=None, vec3=None, color: tuple = (255, 255, 255)):
        # Cas 1 : 3 Vector2 en paramètres (depuis supSquare/supCircle)
        if isinstance(vec1, Vector2) and isinstance(vec2, Vector2) and isinstance(vec3, Vector2):
            center_x = (vec1.x + vec2.x + vec3.x) / 3
            center_y = (vec1.y + vec2.y + vec3.y) / 3
            super().__init__(center_x, center_y, color)
            
            self.vertices = [
                Vector2(vec1.x - center_x, vec1.y - center_y),
                Vector2(vec2.x - center_x, vec2.y - center_y),
                Vector2(vec3.x - center_x, vec3.y - center_y)
            ]
        # Cas 2 : x, y, color (depuis _generateSupnovaTriangles)
        else:
            x = vec1
            y = vec2
            super().__init__(x, y, color if isinstance(vec3, tuple) else vec3)
            
            self.vertices = [
                Vector2(-5, -5),
                Vector2(5, -5),
                Vector2(0, 5)
            ]
    
    def rotate(self, center: Vector2, angle: float) -> None:
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        
        dx = self.x - center.x
        dy = self.y - center.y
        
        new_x = dx * cos_angle - dy * sin_angle
        new_y = dx * sin_angle + dy * cos_angle
        
        self.x = center.x + new_x
        self.y = center.y + new_y
    
    def draw(self, screen: pygame.Surface, color: tuple, rotation: float) -> None:
        rotated_vertices = []
        cos_angle = math.cos(rotation)
        sin_angle = math.sin(rotation)
        
        for vertex in self.vertices:
            rotated_x = vertex.x * cos_angle - vertex.y * sin_angle
            rotated_y = vertex.x * sin_angle + vertex.y * cos_angle
            rotated_vertices.append((self.x + rotated_x, self.y + rotated_y))
        
        pygame.draw.polygon(screen, color, rotated_vertices)
    
    def erase(self, screen: pygame.Surface, rotation: float) -> None:
        self.draw(screen, (0, 0, 0), rotation)
    
    def move(self, offset: Vector2) -> None:
        self.x += offset.x
        self.y += offset.y