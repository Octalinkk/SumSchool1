from abc import ABC, abstractmethod
import pygame
from pygame import Vector2

class Shape(ABC):
    def __init__(self, x: float, y: float, color: tuple):
        self.x = x
        self.y = y
        self.color = color
    
    @abstractmethod
    def draw(self, screen: pygame.Surface, color: tuple, rotation: float) -> None:
        pass
    
    @abstractmethod
    def erase(self, screen: pygame.Surface, rotation: float) -> None:
        pass
    
    @abstractmethod
    def move(self, offset: Vector2) -> None:
        pass