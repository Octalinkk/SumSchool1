import pygame
import random
import time
from Spaceship import SpaceShip
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from MidiDataExtractor import MidiDataExtractor
from Grammar import Grammar


class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    nStars: int = 1000
    screenWidth: int = 1920
    screenHeight: int = 1080
    supnovaDuration: float = 0.3
    midi_path:str = "test2.mid"
    grammar = Grammar(midi_path)
    
    # CLASS ATTRIBUTES FOR STORING STAR AND SUPERNOVA DATA 
    tabStarsWidth: List[float] = []
    tabStarsHeight: List[float] = []  # LISTS OF COORDINATES TO DELETE AND MODIFY EACH STAR
    tabStarsColors: List[int] = []  # LISTS TO STORE THE COLOR INTENSITY OF EACH STAR
    startTime: float = time.time()
    supnovaActiveList: List[Dict[str, Any]] = []


    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.running: bool = True
        self.extract = MidiDataExtractor(self.midi_path)
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
            randomOpacity: int = int(random.uniform(0, 255))
            
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
        spiralX: int = int(x) + int((progress * 50) * math.cos(progress * 100) * random.uniform(0, 1.2))
        spiralY: int = int(y) + int((progress * 50) * math.sin(progress * 100) * random.uniform(0, 1.2))

        if progress < 0.5:
            # FIRST HALF: DRAW EXPANDING BRIGHT SPIRAL WITH INCREASING COLOR INTENSITY
            pygame.draw.polygon(
                self.screen,
                (progress * 2 * randomR * random.uniform(0, 1),
                 progress * 2 * randomG * random.uniform(0, 1),
                 progress * 2 * randomB),
                [(spiralX, spiralY),
                 (spiralX + 0.5, spiralY + 1),
                 (spiralX + 1, spiralY)]
            )
        else:
            # SECOND HALF: ERASE THE PREVIOUS POSITION STORED IN THE DICTIONARY
            if supnova_dict['spiralX'] is not None:
                pygame.draw.polygon(
                    self.screen,
                    (0, 0, 0),
                    [(supnova_dict['spiralX'], supnova_dict['spiralY']),
                     (supnova_dict['spiralX'] + 0.5, supnova_dict['spiralY'] + 1),
                     (supnova_dict['spiralX'] + 1, supnova_dict['spiralY'])]
                )

        # SAVE CURRENT POSITION FOR NEXT FRAME TO ENABLE ERASING
        supnova_dict['spiralX'] = spiralX
        supnova_dict['spiralY'] = spiralY

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
                'spiralX': None,
                'spiralY': None
            })

    def onInit(self) -> None:
        # MAIN GAME LOOP - INITIALIZE AND RUN THE GAME
        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        pygame.mixer.music.load(self.midi_path)
        
        spaceShip = SpaceShip(Vector2(self.screenWidth/2 + 200, self.screenHeight/2),0)
        self.grammar.genShip(spaceShip)

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