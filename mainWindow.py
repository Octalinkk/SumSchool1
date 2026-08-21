import pygame
import random
import time
from Spaceship import SpaceShip
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from SoundExtract import SoundExtract
from Triangle import Triangle


class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    nStars: int = 1000
    screenWidth: int = 1920
    screenHeight: int = 1080
    supnovaDuration: float = 0.5
    
    # CLASS ATTRIBUTES FOR STORING STAR AND SUPERNOVA DATA 
    tabStarsWidth: List[float] = []
    tabStarsHeight: List[float] = []  # LISTS OF COORDINATES TO DELETE AND MODIFY EACH STAR
    tabStarsColors: List[int] = []  # LISTS TO STORE THE COLOR INTENSITY OF EACH STAR
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
        pygame.display.set_caption("APP")

    def drawStars(self, nStars: int) -> None:
        # GENERATE RANDOM STARS AND STORE THEIR PROPERTIES IN CLASS LISTS
        for i in range(nStars):
            # GENERATE RANDOM POSITION AND OPACITY FOR EACH STAR
            randomWidth: int = int(random.uniform(0, self.screenWidth))
            randomHeight: int = int(random.uniform(0, self.screenHeight))
            randomOpacity: int = int(random.uniform(0, 205))
            
            # DRAW STAR AS A SMALL POLYGON (TRIANGLE)
            pygame.draw.polygon(
                self.screen,
                (255 - randomOpacity, 255 - randomOpacity, 255 - randomOpacity),
                [(randomWidth + 1, randomHeight + 0),
                 (randomWidth + 2, randomHeight + 2),
                 (randomWidth + 0, randomHeight + 2)]
            )
            
            # STORE STAR COORDINATES AND COLOR FOR FUTURE UPDATES
            self.tabStarsWidth.append(randomWidth)
            self.tabStarsHeight.append(randomHeight)
            self.tabStarsColors.append(255 - randomOpacity)

    def moveAllStars(self, nStars: int) -> None:
        # UPDATE POSITION OF ALL STARS WITH WRAPPING AT SCREEN EDGES
        for i in range(nStars):
            # ERASE THE STAR AT ITS PREVIOUS POSITION BY DRAWING BLACK POLYGON
            pygame.draw.polygon(
                self.screen,
                (0, 0, 0),
                [(self.tabStarsWidth[i] + 1, self.tabStarsHeight[i] + 0),
                 (self.tabStarsWidth[i] + 2, self.tabStarsHeight[i] + 2),
                 (self.tabStarsWidth[i] + 0, self.tabStarsHeight[i] + 2)]
            )
            
            # UPDATE STAR POSITION WITH WRAPPING USING MODULO OPERATOR
            self.tabStarsHeight[i] = (self.tabStarsHeight[i] + 0.01) % self.screenHeight
            self.tabStarsWidth[i] = (self.tabStarsWidth[i] + 0.1) % self.screenWidth

            # REDRAW STAR AT NEW POSITION WITH ORIGINAL COLOR
            pygame.draw.polygon(
                self.screen,
                (self.tabStarsColors[i], self.tabStarsColors[i], self.tabStarsColors[i]),
                [(self.tabStarsWidth[i] + 1, self.tabStarsHeight[i] + 0),
                 (self.tabStarsWidth[i] + 2, self.tabStarsHeight[i] + 2),
                 (self.tabStarsWidth[i] + 0, self.tabStarsHeight[i] + 2)]
            )

    def drawSupnovaAtStage(
        self,
        x: float,
        y: float,
        elapsedTime: float,
        randomR: int,
        randomG: int,
        randomB: int,
        supnova_dict: Dict[str, Any]
    ) -> None:
        # DRAW SUPERNOVA ANIMATION WITH SPIRAL EFFECT OVER TIME
        # CALCULATE ANIMATION PROGRESS AS FRACTION OF TOTAL DURATION
        progress: float = elapsedTime / self.supnovaDuration

        # CALCULATE SPIRAL POSITION USING TRIGONOMETRIC FUNCTIONS
        spiralX: int = int(x) + int((progress * 100) * math.cos(progress * 100) * random.uniform(0, 1.2))
        spiralY: int = int(y) + int((progress * 100) * math.sin(progress * 100) * random.uniform(0, 1.2))

        if progress < 0.5:
            # FIRST HALF: DRAW EXPANDING BRIGHT SPIRAL WITH INCREASING COLOR INTENSITY

            angle = random.uniform(0, 6.28)

            vec1 = Vector2(spiralX, spiralY)
            vec2 = Vector2(spiralX + random.uniform(2.5, 5), spiralY + random.uniform(5, 10))
            vec3 = Vector2(spiralX + random.uniform(7.5, 15), spiralY)

            tri = Triangle(vec1,vec2,vec3)

            supnova_dict['triangle'].append(tri)
            supnova_dict['spiralX'].append(spiralX)
            supnova_dict['spiralY'].append(spiralY)

            tri.rotate(Vector2(spiralX,spiralY),angle)
            tri.draw(self.screen,(progress * 2 * randomR * random.uniform(0, 1),progress * 2 * randomG * random.uniform(0, 1),progress * 2 * randomB))

        else:
            # SECOND HALF: ERASE THE PREVIOUS POSITION STORED IN THE DICTIONARY
            if supnova_dict['triangle'] is not None:

                for i in range (len(supnova_dict['triangle'])):

                    triErase = supnova_dict['triangle'][i]
                    x = supnova_dict['spiralX'][i]
                    y = supnova_dict['spiralY'][i]

                    
                    triErase.draw(self.screen,(0,0,0))  


    def destroyRandomStar(self, nStars: int) -> None:
        # SELECT AND DESTROY A RANDOM STAR, CREATING A SUPERNOVA ANIMATION
        if nStars > 0:
            # PICK A RANDOM STAR INDEX
            randomStars: int = int(random.uniform(0, nStars))
            x: float = self.tabStarsWidth[randomStars]
            y: float = self.tabStarsHeight[randomStars]
            
            # ERASE THE STAR FROM SCREEN
            pygame.draw.polygon(
                self.screen,
                (0, 0, 0),
                [(x + 1, y), (x + 2, y + 2), (x, y + 2)]
            )
            
            # REMOVE STAR DATA FROM TRACKING LISTS
            del self.tabStarsWidth[randomStars]
            del self.tabStarsHeight[randomStars]

            # CREATE NEW SUPERNOVA ENTRY WITH INITIAL PARAMETERS
            self.supnovaActiveList.append({
                'x': x,
                'y': y,
                'startTime': time.time(),
                'randomR': int(random.uniform(0, 255)),
                'randomG': int(random.uniform(0, 255)),
                'randomB': int(random.uniform(0, 255)),
                'triangle': [],
                'spiralX': [],
                'spiralY': []
            })

    def onInit(self) -> None:
        # MAIN GAME LOOP - INITIALIZE AND RUN THE GAME
        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        pygame.mixer.music.load("C:/Users/rubat/IdeaProjects/T2D/data/music/midiplayer/brahms_lullaby.mid")
        
        spaceShip = SpaceShip(Vector2(self.screenWidth/2 + 300, self.screenHeight/2),0)

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
                        #self.screen.fill((100, 100, 100))
                        self.destroyRandomStar(len(self.tabStarsHeight))
                        nextNoteIdx += 1 

            self.moveAllStars(len(self.tabStarsHeight))

            for supnova in self.supnovaActiveList[:]:  # [:] CREATES A COPY TO SAFELY ITERATE WHILE REMOVING
                elapsed: float = time.time() - supnova['startTime']
                
                # DRAW SUPERNOVA IF STILL ACTIVE
                if elapsed < self.supnovaDuration:
                    self.drawSupnovaAtStage(
                        supnova['x'],
                        supnova['y'],
                        elapsed,
                        supnova['randomR'],
                        supnova['randomG'],
                        supnova['randomB'],
                        supnova
                    )
                else:
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