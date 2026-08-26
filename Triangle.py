from pygame import Vector2, draw
import math

class Triangle():

    pi = math.pi

    def __init__(self, p1:Vector2, p2:Vector2, p3:Vector2,):
        self.angle = 0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def draw(self, screen, color=(255,0,0)):
        draw.polygon(screen, color, [self.p1, self.p2, self.p3])

    def rotate(self, target:Vector2, angleRad:float):        
        self.p1 = Vector2(
            target.x + ((self.p1.x - target.x) * math.cos(angleRad) - (self.p1.y - target.y) * math.sin(angleRad)), 
            target.y + ((self.p1.x - target.x) * math.sin(angleRad) + (self.p1.y - target.y) * math.cos(angleRad))
        )
        self.p2 = Vector2(
            target.x + ((self.p2.x - target.x) * math.cos(angleRad) - (self.p2.y - target.y) * math.sin(angleRad)), 
            target.y + ((self.p2.x - target.x) * math.sin(angleRad) + (self.p2.y - target.y) * math.cos(angleRad))
        )
        self.p3 = Vector2(
            target.x + ((self.p3.x - target.x) * math.cos(angleRad) - (self.p3.y - target.y) * math.sin(angleRad)), 
            target.y + ((self.p3.x - target.x) * math.sin(angleRad) + (self.p3.y - target.y) * math.cos(angleRad))
        )
