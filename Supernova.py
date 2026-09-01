import random
import math
import time
from typing import List, Tuple, Any

import pygame
from pygame import Vector2

from supTriangle import supTriangle
from supSquare import supSquare
from supCircle import supCircle


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

        self.shapes: List[Any] = []
        self.color: List[Tuple[int, int, int]] = []
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

    def _generateShapes(self) -> None:
        numShapes: int = int(random.uniform(30, 60))
        shapeClasses = [supTriangle, supSquare, supCircle]

        for _ in range(numShapes):
            randomR = int(random.uniform(50, 80))
            randomG = int(random.uniform(50, 80))
            randomB = int(random.uniform(150, 255))

            angle = random.uniform(0, 6.28)

            # PLACER LES FORMES PLUS LOIN DU CENTRE
            radius: float = random.uniform(0, 5)
            offsetX: float = radius * math.cos(angle)
            offsetY: float = radius * math.sin(angle)

            # Créer une forme aléatoire
            randomShapeClass = random.choice(shapeClasses)
            shape = randomShapeClass(self.x + offsetX, self.y + offsetY, (randomR, randomG, randomB))

            self.shapes.append(shape)
            self.color.append((randomR, randomG, randomB))
            self.spiralX.append(self.x + offsetX)
            self.spiralY.append(self.y + offsetY)

    def _drawExpansion(self, screen: pygame.Surface, elapsedTime: float) -> None:
        progress: float = elapsedTime / self.EXPANSION_DURATION

        if not self.shapes:
            self._generateShapes()

        for i in range(len(self.shapes)):
            shape = self.shapes[i]
            col = self.color[i]

            intensifiedColor = (
                int(col[0] * progress),
                int(col[1] * progress),
                int(col[2] * progress)
            )
            shape.draw(screen, intensifiedColor, 0)

    def _drawActive(self, screen: pygame.Surface) -> None:
        for i in range(len(self.shapes)):
            self.shapes[i].draw(screen, self.color[i], 0)

    def _drawConvergence(self, screen: pygame.Surface, convergenceElapsed: float) -> None:
        progress: float = convergenceElapsed / self.CONVERGENCE_DURATION

        speedFactor: float = 0.01
        adjustedProgress: float = progress * speedFactor

        for i in range(len(self.shapes)):
            shape = self.shapes[i]

            initialX: float = self.spiralX[i]
            initialY: float = self.spiralY[i]

            shape.erase(screen, 0)

            currentX: float = initialX + (self.x - initialX) * adjustedProgress
            currentY: float = initialY + (self.y - initialY) * adjustedProgress

            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            shape.move(Vector2(offsetX, offsetY))

            originalColor = self.color[i]
            convergenceColor = (
                int(originalColor[0] + (255 - originalColor[0]) * progress),
                int(originalColor[1] + (255 - originalColor[1]) * progress),
                int(originalColor[2] + (255 - originalColor[2]) * progress),
            )

            shape.draw(screen, convergenceColor, 0)

    def _drawFadeToBlack(self, screen: pygame.Surface, fadeElapsed: float) -> None:
        progress: float = fadeElapsed / self.FADE_DURATION

        speedFactor: float = 0.5
        adjustedProgress: float = progress * speedFactor

        for i in range(len(self.shapes)):
            shape = self.shapes[i]

            initialX: float = self.spiralX[i]
            initialY: float = self.spiralY[i]

            shape.erase(screen, 0)

            currentX: float = initialX + (self.x - initialX) * (1.0 + adjustedProgress)
            currentY: float = initialY + (self.y - initialY) * (1.0 + adjustedProgress)

            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            shape.move(Vector2(offsetX, offsetY))

            fadeColor = (
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
            )

            shape.draw(screen, fadeColor, 0)

    def _drawDestruction(self, screen: pygame.Surface) -> None:
        for shape in self.shapes:
            shape.erase(screen, 0)

    def cleanup(self) -> None:
        self.shapes.clear()
        self.spiralX.clear()
        self.spiralY.clear()
        self.color.clear()