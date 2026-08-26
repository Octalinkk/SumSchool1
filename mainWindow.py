import pygame
import random
import time
from Spaceship import SpaceShip
from Planet import Planet
from Star import Star
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from MidiDataExtractor import MidiDataExtractor
from Grammar import Grammar
from Triangle import Triangle





class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    nStars: int = 1000
    screenWidth: int = 1920
    screenHeight: int = 1080
    supnovaDuration: float = 0.3
    midi_path:str = "test2.mid"
    grammar = Grammar(midi_path)
    
    # CLASS ATTRIBUTES FOR STORING STAR AND SUPERNOVA DATA 
    stars: List[Star] = []
    startTime: float = time.time()
    supnovaActiveList: List[Dict[str, Any]] = []


    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.running: bool = True
        self.extract = MidiDataExtractor(self.midi_path)
        self.Instr1Notes = self.extract.getNotesForIntru(0)  
        self.Instr2Notes = self.extract.getNotesForIntru(1)  

    def windownInit(self) -> None:
        # INITIALIZE PYGAME AND CREATE DISPLAY WINDOW
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("APP")

    def drawStars(self, nStars: int) -> None:
        for i in range(nStars):
            randomWidth: float = random.uniform(0, self.screenWidth)
            randomHeight: float = random.uniform(0, self.screenHeight)
            randomOpacity: int = int(random.uniform(0, 205))
            
            color: int = 255 - randomOpacity
            
            star = Star(randomWidth, randomHeight, color)
            star.draw(self.screen)
            self.stars.append(star)

    def moveAllStars(self) -> None:
        for star in self.stars:
            star.erase(self.screen)
            star.move(self.screenWidth, self.screenHeight)
            star.draw(self.screen)

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
                'randomR': int(random.uniform(0, 255)),
                'randomG': int(random.uniform(0, 255)),
                'randomB': int(random.uniform(0, 255)),
                'triangle': [],
                'spiralX': [],
                'spiralY': []
            })

    def onInit(self) -> None:
        # MAIN GAME LOOP - INITIALIZE AND RUN THE GAME
        self.windownInit()
        self.drawStars(self.nStars)
        pygame.mixer.music.load(self.midi_path)

        
        planet = Planet(Vector2(self.screenWidth/2, self.screenHeight/2), 100, self.grammar.seed)
        spaceShip = SpaceShip(Vector2(planet.origin.x + planet.radius * 2, planet.origin.y), planet.origin)
        self.grammar.genShip(spaceShip)
        palette = self.grammar.genPalette(5) # Ship has 5 parts

        pygame.mixer.music.play()
        
        # Index to check next note
        nextNoteSeq1Idx = 0
        nextNoteSeq2Idx = 0
        
        while self.running:
            songPos = pygame.mixer.music.get_pos()            
            # Check if song started
            if songPos != -1:
                currentTime = songPos / 1000.0  # Convert to sec
                
                # Check timing with next note
                if nextNoteSeq2Idx < len(self.Instr2Notes):
                    note2TimestmpStart = self.Instr2Notes[nextNoteSeq2Idx].start
                    
                    if currentTime >= note2TimestmpStart:
                        self.destroyRandomStar()
                        nextNoteSeq2Idx += 1 

                # Check timing with next note
                if nextNoteSeq1Idx < len(self.Instr1Notes):
                    note1TimestmpStart = self.Instr1Notes[nextNoteSeq1Idx].start                    
                    note1TimestmpStop = self.Instr1Notes[nextNoteSeq1Idx].end
                    
                    if currentTime >= note1TimestmpStart:
                        #self.screen.fill((100, 100, 100))
                        spaceShip.fireBeam()

                    if currentTime >= note1TimestmpStop:
                        #self.screen.fill((100, 100, 100))
                        spaceShip.stopBeam()
                        
                        nextNoteSeq1Idx += 1 

            self.moveAllStars()

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
                    # CLEAN UP MEMORY: Vider les listes de triangles
                    supnova['triangle'].clear()
                    supnova['spiralX'].clear()
                    supnova['spiralY'].clear()
    
                    # REMOVE EXPIRED SUPERNOVA FROM ACTIVE LIST
                    self.supnovaActiveList.remove(supnova)

            spaceShip.eraseDrawing(self.screen)
            spaceShip.rotateShip(0.001)
            spaceShip.drawShip(self.screen, palette)
            spaceShip.drawBeam(self.screen)
            planet.drawPlanet(self.screen)
            
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