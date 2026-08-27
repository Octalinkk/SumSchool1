import pygame

class Star:
    def __init__(self, x: float, y: float, color: int):
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(
            screen,
            (self.color, self.color, self.color),
            [(self.x + 1, self.y + 0),
             (self.x + 2, self.y + 2),
             (self.x + 0, self.y + 2)]
        )
    
    def erase(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            [(self.x + 1, self.y + 0),
             (self.x + 2, self.y + 2),
             (self.x + 0, self.y + 2)]
        )
    
    def move(self, screen_width: float, screen_height: float) -> None:
        self.x = (self.x + 1.1) % screen_width
        self.y = (self.y + 1.01) % screen_height