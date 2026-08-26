from pygame import Vector2, draw
from Triangle import Triangle
import math

class EquiTriangle(Triangle):
    def __init__(self, origin: Vector2, side: int = 10, angle: float = 0, color=(0, 200, 50)):
        self.origin:Vector2 = origin
        self.side:int = side  # longueur d'un côté
        self.color = color

        radius = self.side / math.sqrt(3)

        # 3 sommets répartis tous les 120°, en partant du haut (-90°)
        points = []
        for i in range(3):
            theta = math.radians(-90 + i * 120)
            x = self.origin.x + radius * math.cos(theta)
            y = self.origin.y + radius * math.sin(theta)
            points.append(Vector2(x, y))

        super().__init__(points[0], points[1], points[2])

        if angle != 0:
            self.rotate(self.origin, angle)
        self.angle = angle

    def draw(self, screen):
        super().draw(screen, self.color)