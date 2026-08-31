import random
import math
import time
from typing import List, Tuple

import pygame
from pygame import Vector2

from Triangle import Triangle


class Supernova:

    EXPANSION_DURATION: float = 0.1
    ACTIVE_DURATION: float = 1
    CONVERGENCE_DURATION: float = 1.9
    FADE_DURATION: float = 1.5
    DESTRUCTION_DURATION: float = 0.1

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.startTime: float = time.time()

        self.triangle: List[Triangle] = []
        self.color: List[Tuple[float, float, float]] = []
        self.spiralX: List[float] = []
        self.spiralY: List[float] = []

    def totalDuration(self) -> float:
        return (
            self.EXPANSION_DURATION
            + self.ACTIVE_DURATION
            + self.CONVERGENCE_DURATION
            + self.FADE_DURATION
            + self.DESTRUCTION_DURATION
        )

    def isExpired(self, elapsedTime: float) -> bool:
        return elapsedTime >= self.totalDuration()

    def drawAtStage(self, screen: pygame.Surface, elapsedTime: float) -> None:
        if elapsedTime < self.EXPANSION_DURATION:
            self._drawExpansion(screen, elapsedTime)

        elif elapsedTime < self.EXPANSION_DURATION + self.ACTIVE_DURATION:
            self._drawActive(screen)

        elif elapsedTime < (
            self.EXPANSION_DURATION + self.ACTIVE_DURATION + self.CONVERGENCE_DURATION
        ):
            convergenceElapsed = elapsedTime - (self.EXPANSION_DURATION + self.ACTIVE_DURATION)
            self._drawConvergence(screen, convergenceElapsed)

        elif elapsedTime < (
            self.EXPANSION_DURATION
            + self.ACTIVE_DURATION
            + self.CONVERGENCE_DURATION
            + self.FADE_DURATION
        ):
            fadeElapsed = elapsedTime - (
                self.EXPANSION_DURATION + self.ACTIVE_DURATION + self.CONVERGENCE_DURATION
            )
            self._drawFadeToBlack(screen, fadeElapsed)

        else:
            self._drawDestruction(screen)

    def _generateTriangles(self) -> None:
        numTriangles: int = 30

        for _ in range(numTriangles):
            randomR = int(random.uniform(50, 80))
            randomG = int(random.uniform(50, 80))
            randomB = int(random.uniform(150, 255))

            angle = random.uniform(0, 6.28)

            # PLACER LES TRIANGLES PLUS LOIN DU CENTRE
            radius: float = random.uniform(0, 5)
            offsetX: float = radius * math.cos(angle)
            offsetY: float = radius * math.sin(angle)

            vec1 = Vector2(self.x + offsetX, self.y + offsetY)
            vec2 = Vector2(
                self.x + offsetX + random.uniform(5, 10),
                self.y + offsetY + random.uniform(5, 10),
            )
            vec3 = Vector2(self.x + offsetX + random.uniform(10, 20), self.y + offsetY)

            tri = Triangle(vec1, vec2, vec3)
            tri.rotate(Vector2(self.x, self.y), angle)

            self.triangle.append(tri)
            self.color.append((randomR, randomG, randomB))
            self.spiralX.append(self.x + offsetX)
            self.spiralY.append(self.y + offsetY)

    def _drawExpansion(self, screen: pygame.Surface, elapsedTime: float) -> None:
        progress: float = elapsedTime / self.EXPANSION_DURATION

        if not self.triangle:
            self._generateTriangles()

        for i in range(len(self.triangle)):
            tri = self.triangle[i]
            col = self.color[i]

            intensifiedColor = (col[0] * progress, col[1] * progress, col[2] * progress)
            tri.draw(screen, intensifiedColor)

    def _drawActive(self, screen: pygame.Surface) -> None:
        for i in range(len(self.triangle)):
            self.triangle[i].draw(screen, self.color[i])

    def _drawConvergence(self, screen: pygame.Surface, convergenceElapsed: float) -> None:
        progress: float = convergenceElapsed / self.CONVERGENCE_DURATION

        speedFactor: float = 0.01
        adjustedProgress: float = progress * speedFactor

        for i in range(len(self.triangle)):
            tri = self.triangle[i]

            initialX: float = self.spiralX[i]
            initialY: float = self.spiralY[i]

            tri.draw(screen, (0, 0, 0))

            currentX: float = initialX + (self.x - initialX) * adjustedProgress
            currentY: float = initialY + (self.y - initialY) * adjustedProgress

            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            tri.move(Vector2(offsetX, offsetY))

            originalColor = self.color[i]
            convergenceColor = (
                originalColor[0] + (255 - originalColor[0]) * progress,
                originalColor[1] + (255 - originalColor[1]) * progress,
                originalColor[2] + (255 - originalColor[2]) * progress,
            )

            tri.draw(screen, convergenceColor)

    def _drawFadeToBlack(self, screen: pygame.Surface, fadeElapsed: float) -> None:
        progress: float = fadeElapsed / self.FADE_DURATION

        speedFactor: float = 0.5
        adjustedProgress: float = progress * speedFactor

        for i in range(len(self.triangle)):
            tri = self.triangle[i]

            initialX: float = self.spiralX[i]
            initialY: float = self.spiralY[i]

            tri.draw(screen, (0, 0, 0))

            currentX: float = initialX + (self.x - initialX) * (1.0 + adjustedProgress)
            currentY: float = initialY + (self.y - initialY) * (1.0 + adjustedProgress)

            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            tri.move(Vector2(offsetX, offsetY))

            fadeColor = (
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
            )

            tri.draw(screen, fadeColor)

    def _drawDestruction(self, screen: pygame.Surface) -> None:
        for tri in self.triangle:
            tri.draw(screen, (0, 0, 0))

    def cleanup(self) -> None:
        
        self.triangle.clear()
        self.spiralX.clear()
        self.spiralY.clear()
        self.color.clear()