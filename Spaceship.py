from pygame import Vector2

class SpaceShip():
    def __init__(self, origin:Vector2, target:Vector2, distance:int):
        self.originPos = origin
        self.targetPos = target
        self.dist = distance