import pygame
import random
import time
from Spaceship import SpaceShip
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from SoundExtract import SoundExtract
from Triangle import Triangle


class Star:

    xMove = 0.1
    yMove = 0.01

    def __init__(self, x: float, y: float, color: int):
        self.x = x
        self.y = y
        self.color = color
    
    def drawSmallTriangle(self, screen: pygame.Surface) -> None:
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
        self.x = (self.x + self.xMove) % screen_width
        self.y = (self.y + self.yMove) % screen_height


class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    nStars: int = 1000
    screenWidth: int = 1920
    screenHeight: int = 1080
    supnovaDuration: float = 0.5
    supnovaActiveTime: float = 10
    supnovaDestructionTimeDuration: float = 0.5
    
    # CLASS ATTRIBUTES FOR STORING STAR AND SUPERNOVA DATA 
    stars: List[Star] = []
    startTime: float = time.time()
    supnovaActiveList: List[Dict[str, Any]] = []


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

    def drawSupnovaAtStage(
        self,
        x: float,
        y: float,
        elapsedTime: float,
        supnova_dict: Dict[str, Any]
    ) -> None:
        """Dispatch vers la bonne phase en fonction du temps écoulé"""
        
        # PHASE 1: EXPANSION (0 à supnovaDuration)
        if elapsedTime < self.supnovaDuration:
            self._drawSupnovaExpansion(x, y, elapsedTime, supnova_dict)
        
        # PHASE 2: ACTIVE (supnovaDuration à supnovaDuration + supnovaActiveTime)
        elif elapsedTime < self.supnovaDuration + self.supnovaActiveTime:
            self._drawSupnovaActive(supnova_dict)
        
        # PHASE 3: DESTRUCTION (après supnovaDuration + supnovaActiveTime)
        else:
            self._drawSupnovaDestruction(supnova_dict)

    def _drawSupnovaExpansion(
        self,
        x: float,
        y: float,
        elapsedTime: float,
        supnova_dict: Dict[str, Any]
    ) -> None:
        """PHASE 1: Expansion - Génère et affiche les triangles en spirale croissante"""
        progress: float = elapsedTime / self.supnovaDuration
        
        # Générer les triangles UNE SEULE FOIS (à la première frame de cette phase)
        if not supnova_dict['triangle']:
            self._generateSupnovaTriangles(x, y, supnova_dict)
        
        # Afficher les triangles avec couleur d'expansion
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            col = supnova_dict['color'][i]
            
            # Augmenter l'intensité pendant l'expansion
            intensifiedColor = (
                col[0] * progress,
                col[1] * progress,
                col[2] * progress
            )
            
            tri.draw(self.screen, intensifiedColor)

    def _generateSupnovaTriangles(
        self,
        x: float,
        y: float,
        supnova_dict: Dict[str, Any]
    ) -> None:
        numTriangles: int = 20  # Nombre de triangles à générer
        
        for _ in range(numTriangles):
            randomR = int(random.uniform(100, 255))
            randomG = int(random.uniform(50, 200))
            randomB = int(random.uniform(150, 255))
            
            angle = random.uniform(0, 6.28)
            
            # Créer un triangle aléatoire
            vec1 = Vector2(x, y)
            vec2 = Vector2(x + random.uniform(2.5, 5), y + random.uniform(5, 10))
            vec3 = Vector2(x + random.uniform(7.5, 15), y)
            
            tri = Triangle(vec1, vec2, vec3)
            tri.rotate(Vector2(x, y), angle)
            
            supnova_dict['triangle'].append(tri)
            supnova_dict['color'].append((randomR, randomG, randomB))
            supnova_dict['spiralX'].append(x)
            supnova_dict['spiralY'].append(y)

    def _drawSupnovaActive(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            col = supnova_dict['color'][i]
            
            # Afficher à couleur pleine (pas de changement d'intensité)
            tri.draw(self.screen, col)

    def _drawSupnovaDestruction(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            
            # Effacer en noir pour la phase 3
            tri.draw(self.screen, (0, 0, 0))

    def destroyRandomStar(self) -> None:
        if len(self.stars) > 0:
            # PICK A RANDOM STAR
            randomIdx: int = int(random.uniform(0, len(self.stars)))
            star = self.stars[randomIdx]
            
            x: float = star.x
            y: float = star.y
            
            # ERASE THE STAR FROM SCREEN
            star.erase(self.screen)
            
            # REMOVE STAR FROM LIST
            self.stars.pop(randomIdx)
            
            # CREATE NEW SUPERNOVA ENTRY
            self.supnovaActiveList.append({
                'x': x,
                'y': y,
                'startTime': time.time(),
                'color': [],
                'triangle': [],
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
        
        # Index to check next note
        nextNoteIdx = 0
        
        while self.running:
            songPos = pygame.mixer.music.get_pos()            
            # Check if song started
            if songPos != -1:
                currentTime = songPos / 1000.0  # Convert to sec
                
                # Check timing with next note
                if nextNoteIdx < len(self.Instr1Notes):
                    noteTimestmp = self.Instr1Notes[nextNoteIdx].start
                    
                    if currentTime >= noteTimestmp:
                        # self.screen.fill((100, 100, 100))
                        self.destroyRandomStar()
                        nextNoteIdx += 1 

            self.moveAllStars()

            for supnova in self.supnovaActiveList[:]:  # [:] CREATES A COPY TO SAFELY ITERATE WHILE REMOVING
                elapsed: float = time.time() - supnova['startTime']
                
                # DRAW SUPERNOVA IF STILL ACTIVE
                if elapsed < self.supnovaDuration + self.supnovaActiveTime + self.supnovaDestructionTimeDuration:
                    self.drawSupnovaAtStage(
                        supnova['x'],
                        supnova['y'],
                        elapsed,
                        supnova
                    )
                else:
                    # CLEAN UP MEMORY: Vider les listes de triangles
                    supnova['triangle'].clear()
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