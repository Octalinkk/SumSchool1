import random
import time
from typing import List

import pygame

from Star import Star
from Supernova import Supernova


class StarManager:

    def __init__(self, screenWidth: int, screenHeight: int):
        self.screenWidth: int = screenWidth
        self.screenHeight: int = screenHeight

        self.stars: List[Star] = []
        self.supernovaActiveList: List[Supernova] = []

    def spawnStars(self, nStars: int, screen: pygame.Surface) -> None:
        for _ in range(nStars):
            randomWidth: float = random.uniform(0, self.screenWidth)
            randomHeight: float = random.uniform(0, self.screenHeight)
            randomOpacity: int = int(random.uniform(0, 170))

            color: int = 255 - randomOpacity

            star = Star(randomWidth, randomHeight, color)
            star.drawSmallTriangle(screen)
            self.stars.append(star)

    def moveAllStars(self, screen: pygame.Surface) -> None:
        for star in self.stars:
            star.erase(screen)
            star.move(self.screenWidth, self.screenHeight)
            star.drawSmallTriangle(screen)

    def destroyRandomStar(self, screen: pygame.Surface) -> None:
        if len(self.stars) == 0:
            return

        randomIdx: int = int(random.uniform(0, len(self.stars)))
        star = self.stars[randomIdx]

        star.erase(screen)
        self.stars.pop(randomIdx)

        self.supernovaActiveList.append(Supernova(star.x, star.y))

    def updateAndDrawSupernovas(self, screen: pygame.Surface) -> None:
        for supernova in self.supernovaActiveList[:]:
            elapsed: float = time.time() - supernova.startTime

            if not supernova.isExpired(elapsed):
                supernova.drawAtStage(screen, elapsed)
            else:
                supernova.cleanup()
                self.supernovaActiveList.remove(supernova)