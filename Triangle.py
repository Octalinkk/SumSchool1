from pygame import Vector2, draw

class Triangle():
    def __init__(self, p1:Vector2, p2:Vector2, p3:Vector2,):
        self.angle = 0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, screen):
        draw.polygon(screen, (255,0,0), [self.p1, self.p2, self.p3])