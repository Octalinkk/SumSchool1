import pygame
import random
import time
from Spaceship import SpaceShip
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from SoundExtract import SoundExtract
from StarManager import StarManager
from asteroid import Asteroid
from supTriangle import supTriangle
from supSquare import supSquare
from supCircle import supCircle


class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    screenWidth: int = 1920
    screenHeight: int = 1080
    nStars: int = 1000

    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.running: bool = True
        self.extract = SoundExtract("C:/Users/rubat/IdeaProjects/T2D/data/music/midiplayer/brahms_lullaby.mid")
        self.Instr1Notes = self.extract.getNotesForIntru(0)
        
        # Initialize StarManager
        self.starManager: StarManager = StarManager(self.screenWidth, self.screenHeight)
        
        # Asteroids management
        self.asteroids: List[Dict[str, Any]] = []

    def test_pygame_initialization(self) -> None:
        # INITIALIZE PYGAME AND CREATE DISPLAY WINDOW
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Animation")

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

    def onInit(self) -> None:
        # MAIN GAME LOOP - INITIALIZE AND RUN THE GAME
        self.test_pygame_initialization()
        
        # Spawn stars using StarManager
        self.starManager.spawnStars(self.nStars, self.screen)
        
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
                        self.starManager.destroyRandomStar(self.screen)
                        nextNoteIdx += 1 

            # Move and draw stars using StarManager
            self.starManager.moveAllStars(self.screen)
            
            # Draw and move asteroids
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

            # Update and draw supernovas using StarManager
            self.starManager.updateAndDrawSupernovas(self.screen)

            # Draw spaceship
            spaceShip.eraseDrawing(self.screen)
            spaceShip.rotateShip(Vector2(self.screenWidth/2, self.screenHeight/2), 0.001)
            spaceShip.drawShip(self.screen)
            
            # Handle events
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