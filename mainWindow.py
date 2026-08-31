import pygame
import random
import time
from Spaceship import SpaceShip
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from SoundExtract import SoundExtract
from supTriangle import supTriangle
from supSquare import supSquare
from supCircle import supCircle
from star import Star
from asteroid import Asteroid

class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    nStars: int = 1000
    screenWidth: int = 1920
    screenHeight: int = 1080
    supnovaDuration: float = 0.1
    supnovaActiveTime: float = 1
    supnovaConvergenceDuration: float = 1.9
    supnovaFadeDuration: float = 0.2
    supnovaDestructionTimeDuration: float = 0.1
    
    # CLASS ATTRIBUTES FOR STORING STAR AND SUPERNOVA DATA 
    stars: List[Star] = []
    startTime: float = time.time()
    supnovaActiveList: List[Dict[str, Any]] = []
    asteroids: List[Dict[str, Any]] = []


    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.running: bool = True
        self.extract = SoundExtract("C:/Users/rubat/IdeaProjects/T2D/data/music/midiplayer/brahms_lullaby.mid")
        self.Instr1Notes = self.extract.getNotesForIntru(0)

    def test_pygame_initialization(self) -> None:
        # INITIALIZE PYGAME AND CREATE DISPLAY WINDOW
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Animation")

    def drawStars(self, nStars: int) -> None:
        for i in range(nStars):
            randomWidth: float = random.uniform(0, self.screenWidth)
            randomHeight: float = random.uniform(0, self.screenHeight)
            randomOpacity: int = int(random.uniform(0, 170))
            
            color: int = 255 - randomOpacity
            
            star = Star(randomWidth, randomHeight, color)
            star.drawSmallTriangle(self.screen)
            self.stars.append(star)

    def moveAllStars(self) -> None:
        for star in self.stars:
            star.erase(self.screen)
            star.move(self.screenWidth, self.screenHeight)
            star.drawSmallTriangle(self.screen)

    def generateRandomAsteroid(self) -> None:
        randomX: float = random.uniform(0, self.screenWidth)
        randomY: float = random.uniform(0, self.screenHeight)
        radius: float = random.uniform(10, 30)
        
        # Vitesse aléatoire
        vx: float = random.uniform(-3, 3)
        vy: float = random.uniform(-3, 3)
        
        # Vitesse de rotation
        rotationSpeed: float = random.uniform(-0.05, 0.05)
        
        self.asteroids.append({
            'asteroid': Asteroid(randomX, randomY, radius),
            'x': randomX,
            'y': randomY,
            'radius': radius,
            'vx': vx,
            'vy': vy,
            'rotation': 0,
            'rotationSpeed': rotationSpeed
        })

    def drawSupnovaAtStage(
        self,
        x: float,
        y: float,
        elapsedTime: float,
        supnova_dict: Dict[str, Any]
    ) -> None:
        
        # PHASE 1: EXPANSION
        if elapsedTime < self.supnovaDuration:
            self._drawSupnovaExpansion(x, y, elapsedTime, supnova_dict, self.supnovaDuration)
        
        # PHASE 2: ACTIVE
        elif elapsedTime < self.supnovaDuration + self.supnovaActiveTime:
            self._drawSupnovaActive(supnova_dict)
        
        # PHASE 3: CONVERGENCE
        elif elapsedTime < self.supnovaDuration + self.supnovaActiveTime + self.supnovaConvergenceDuration:
            convergenceElapsed: float = elapsedTime - (self.supnovaDuration + self.supnovaActiveTime)
            self._drawSupnovaConvergence(x, y, convergenceElapsed, supnova_dict, self.supnovaConvergenceDuration)
        
        # PHASE 4: FADE TO BLACK
        elif elapsedTime < self.supnovaDuration + self.supnovaActiveTime + self.supnovaConvergenceDuration + self.supnovaFadeDuration:
            fadeElapsed: float = elapsedTime - (self.supnovaDuration + self.supnovaActiveTime + self.supnovaConvergenceDuration)
            self._drawSupnovaFadeToBlack(x, y, fadeElapsed, supnova_dict, self.supnovaFadeDuration)
        
        # PHASE 5: DESTRUCTION
        else:
            self._drawSupnovaDestruction(supnova_dict)

    def _drawSupnovaExpansion(
        self,
        x: float,
        y: float,
        elapsedTime: float,
        supnova_dict: Dict[str, Any],
        duration: float
    ) -> None:
        progress: float = elapsedTime / duration
        
        if not supnova_dict['shapes']:
            self._generateSupnovaTriangles(x, y, supnova_dict)
        
        for i in range(len(supnova_dict['shapes'])):
            shape = supnova_dict['shapes'][i]
            col = supnova_dict['color'][i]
            
            intensifiedColor = (
                int(col[0] * progress),
                int(col[1] * progress),
                int(col[2] * progress)
            )
            
            shape.draw(self.screen, intensifiedColor, 0)

    def _generateSupnovaTriangles(self,x: float,y: float,supnova_dict: Dict[str, Any]) -> None:
        numTriangles: int = int(random.uniform(30, 60))
        shapeClasses = [supTriangle, supSquare, supCircle]  # Liste des formes disponibles
        
        for _ in range(numTriangles):
            randomR = int(random.uniform(50, 80))
            randomG = int(random.uniform(50, 80))
            randomB = int(random.uniform(150, 255))
            
            angle = random.uniform(0, 6.28)
            
            radius: float = random.uniform(0, 5)
            offsetX: float = radius * math.cos(angle)
            offsetY: float = radius * math.sin(angle)
            
            # Créer une forme aléatoire
            randomShapeClass = random.choice(shapeClasses)
            shape = randomShapeClass(x + offsetX, y + offsetY, (randomR, randomG, randomB))
            
            supnova_dict['shapes'].append(shape)
            supnova_dict['color'].append((randomR, randomG, randomB))
            supnova_dict['spiralX'].append(x + offsetX)
            supnova_dict['spiralY'].append(y + offsetY)

    def _drawSupnovaActive(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['shapes'])):
            shape = supnova_dict['shapes'][i]
            col = supnova_dict['color'][i]
            
            shape.draw(self.screen, col, 0)

    def _drawSupnovaConvergence(
        self,
        x: float,
        y: float,
        convergenceElapsed: float,
        supnova_dict: Dict[str, Any],
        duration: float
    ) -> None:
        progress: float = convergenceElapsed / duration
        speedFactor: float = 0.01
        adjustedProgress: float = progress * speedFactor
        
        for i in range(len(supnova_dict['shapes'])):
            shape = supnova_dict['shapes'][i]
            
            initialX: float = supnova_dict['spiralX'][i]
            initialY: float = supnova_dict['spiralY'][i]
            
            shape.erase(self.screen, 0)
            
            currentX: float = initialX + (x - initialX) * adjustedProgress
            currentY: float = initialY + (y - initialY) * adjustedProgress
            
            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            shape.move(Vector2(offsetX, offsetY))
            
            originalColor = supnova_dict['color'][i]
            convergenceColor = (
                int(originalColor[0] + (255 - originalColor[0]) * progress),
                int(originalColor[1] + (255 - originalColor[1]) * progress),
                int(originalColor[2] + (255 - originalColor[2]) * progress)
            )
            
            shape.draw(self.screen, convergenceColor, 0)

    def _drawSupnovaFadeToBlack(
        self,
        x: float,
        y: float,
        fadeElapsed: float,
        supnova_dict: Dict[str, Any],
        duration: float
    ) -> None:
        progress: float = fadeElapsed / duration
        speedFactor: float = 0.5
        adjustedProgress: float = progress * speedFactor
        
        for i in range(len(supnova_dict['shapes'])):
            shape = supnova_dict['shapes'][i]
            
            initialX: float = supnova_dict['spiralX'][i]
            initialY: float = supnova_dict['spiralY'][i]
            
            shape.erase(self.screen, 0)
            
            currentX: float = initialX + (x - initialX) * (1.0 + adjustedProgress)
            currentY: float = initialY + (y - initialY) * (1.0 + adjustedProgress)
            
            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            shape.move(Vector2(offsetX, offsetY))
            
            fadeColor = (
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
                int(255 * (1 - progress))
            )
            
            shape.draw(self.screen, fadeColor, 0)

    def _drawSupnovaDestruction(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['shapes'])):
            shape = supnova_dict['shapes'][i]
            shape.erase(self.screen, 0)

    def destroyRandomStar(self) -> None:
        if len(self.stars) > 0:
            randomIdx: int = int(random.uniform(0, len(self.stars)))
            star = self.stars[randomIdx]
            
            x: float = star.x
            y: float = star.y
            
            # Vérifier qu'on est assez loin des bords
            margin: float = 20  # Marge de sécurité
            if x < margin or x > self.screenWidth - margin or y < margin or y > self.screenHeight - margin:
                return  # Ne pas créer de supernova si trop près du bord
            
            star.erase(self.screen)
            self.stars.pop(randomIdx)
            
            self.supnovaActiveList.append({
                'x': x,
                'y': y,
                'startTime': time.time(),
                'color': [],
                'shapes': [],
                'spiralX': [],
                'spiralY': []
            })

    def onInit(self) -> None:
        # MAIN GAME LOOP - INITIALIZE AND RUN THE GAME
        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        pygame.mixer.music.load("C:/Users/rubat/IdeaProjects/T2D/data/music/midiplayer/brahms_lullaby.mid")
        
        spaceShip = SpaceShip(Vector2(self.screenWidth/2 + 300, self.screenHeight/2), 0)

        pygame.mixer.music.play()
        
        # Générer 5 astéroïdes au démarrage
        for _ in range(5):
            self.generateRandomAsteroid()
        
        # Index to check next note
        nextNoteIdx = 0
        
        while self.running:
            songPos = pygame.mixer.music.get_pos()            
            # Check if song started
            if songPos != -1:
                currentTime = songPos / 1000.0  # Convert to sec
                
                # Check timing with next note
                if nextNoteIdx < len(self.Instr1Notes):
                    noteTimestmp = self.Instr1Notes[nextNoteIdx].start - 3
                    
                    if currentTime >= noteTimestmp:
                        self.destroyRandomStar()
                        nextNoteIdx += 1 

            self.moveAllStars()
            
            # Dessiner et déplacer les astéroïdes
            for asteroid_dict in self.asteroids[:]:
                ast = asteroid_dict['asteroid']
                
                # Effacer l'ancienne position
                ast.erase(self.screen, asteroid_dict['x'], asteroid_dict['y'], asteroid_dict['radius'], asteroid_dict['rotation'])
                
                # Mettre à jour position
                asteroid_dict['x'] += asteroid_dict['vx']
                asteroid_dict['y'] += asteroid_dict['vy']
                asteroid_dict['rotation'] += asteroid_dict['rotationSpeed']
                
                # Gérer wraparound aux bords de l'écran
                asteroid_dict['x'] = asteroid_dict['x'] % self.screenWidth
                asteroid_dict['y'] = asteroid_dict['y'] % self.screenHeight
                
                # Dessiner à la nouvelle position
                
                ast.draw(self.screen, asteroid_dict['x'], asteroid_dict['y'], asteroid_dict['radius'], (100, 100, 100), asteroid_dict['rotation'])

            for supnova in self.supnovaActiveList[:]:
                elapsed: float = time.time() - supnova['startTime']
                totalDuration: float = (
                    self.supnovaDuration + 
                    self.supnovaActiveTime + 
                    self.supnovaConvergenceDuration + 
                    self.supnovaFadeDuration + 
                    self.supnovaDestructionTimeDuration
                )
                
                # DRAW SUPERNOVA IF STILL ACTIVE
                if elapsed < totalDuration:
                    self.drawSupnovaAtStage(
                        supnova['x'],
                        supnova['y'],
                        elapsed,
                        supnova
                    )
                else:
                    # CLEAN UP MEMORY
                    supnova['shapes'].clear()
                    supnova['spiralX'].clear()
                    supnova['spiralY'].clear()
                    supnova['color'].clear()
    
                    # REMOVE EXPIRED SUPERNOVA FROM ACTIVE LIST
                    self.supnovaActiveList.remove(supnova)

            spaceShip.eraseDrawing(self.screen)
            spaceShip.rotateShip(Vector2(self.screenWidth/2, self.screenHeight/2), 0.001)
            spaceShip.drawShip(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()

        # CLEANUP: CLOSE PYGAME
        pygame.quit()


# ENTRY POINT: CREATE GAME INSTANCE AND START
if __name__ == "__main__":
    game: Game = Game()
    game.onInit() 