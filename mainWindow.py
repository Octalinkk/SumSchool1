import pygame
import random
import time
from Spaceship import SpaceShip
from Planet import Planet
from Ring import Ring
from Star import Star
from pygame import Vector2
from typing import List, Dict, Any, Optional
import math
from MidiDataExtractor import MidiDataExtractor
from Grammar import Grammar
from Triangle import Triangle


class Star:

    xMove = 0.5
    yMove = 0.15

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
    midi_path:str = "test3.mid"
    grammar = Grammar(midi_path)
    supnovaDuration: float = 0.1
    supnovaActiveTime: float = 1
    supnovaConvergenceDuration: float = 1.9
    supnovaFadeDuration: float = 0.2
    supnovaDestructionTimeDuration: float = 0.1
    
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
        
        # Générer les triangles UNE SEULE FOIS
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
        numTriangles: int = int(random.uniform(30, 60))  # Nombre de triangles à générer
        
        for _ in range(numTriangles):
            randomR = int(random.uniform(50, 80))
            randomG = int(random.uniform(50,80))
            randomB = int(random.uniform(150, 255))
            
            angle = random.uniform(0, 6.28)
            
            # PLACER LES TRIANGLES PLUS LOIN DU CENTRE
            radius: float = random.uniform(0, 5)
            offsetX: float = radius * math.cos(angle)
            offsetY: float = radius * math.sin(angle)
            
            # Créer un triangle aléatoire à distance du centre
            vec1 = Vector2(x + offsetX, y + offsetY)
            vec2 = Vector2(x + offsetX + random.uniform(5, 10), y + offsetY + random.uniform(5, 10))
            vec3 = Vector2(x + offsetX + random.uniform(10, 20), y + offsetY)
            
            tri = Triangle(vec1, vec2, vec3)
            tri.rotate(Vector2(x, y), angle)
            
            supnova_dict['triangle'].append(tri)
            supnova_dict['color'].append((randomR, randomG, randomB))
            supnova_dict['spiralX'].append(x + offsetX)
            supnova_dict['spiralY'].append(y + offsetY)

    def _drawSupnovaActive(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            col = supnova_dict['color'][i]
            
            tri.draw(self.screen, col)

    def _drawSupnovaConvergence(
        self,
        x: float,
        y: float,
        convergenceElapsed: float,
        supnova_dict: Dict[str, Any],
        duration: float
    ) -> None:
        progress: float = convergenceElapsed / duration
        
        # VITESSE DE DÉPLACEMENT: Réduis ce facteur pour ralentir (0.5 = 50% plus lent, 0.25 = 75% plus lent)
        speedFactor: float = 0.01
        adjustedProgress: float = progress * speedFactor
        
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            
            # Récupérer la position initiale
            initialX: float = supnova_dict['spiralX'][i]
            initialY: float = supnova_dict['spiralY'][i]
            
            # EFFACER: Dessiner en noir à la position courante
            tri.draw(self.screen, (0, 0, 0))
            
            # Calculer la position interpolée vers le centre avec vitesse réduite
            currentX: float = initialX + (x - initialX) * adjustedProgress
            currentY: float = initialY + (y - initialY) * adjustedProgress
            
            # Déplacer le triangle
            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            tri.move(Vector2(offsetX, offsetY))
            
            # Interpoler la couleur vers le blanc
            originalColor = supnova_dict['color'][i]
            convergenceColor = (
                originalColor[0] + (255 - originalColor[0]) * progress,
                originalColor[1] + (255 - originalColor[1]) * progress,
                originalColor[2] + (255 - originalColor[2]) * progress
            )
            
            # REDESSINER: Afficher le triangle à la nouvelle position
            tri.draw(self.screen, convergenceColor)

    def _drawSupnovaFadeToBlack(
        self,
        x: float,
        y: float,
        fadeElapsed: float,
        supnova_dict: Dict[str, Any],
        duration: float
    ) -> None:
        progress: float = fadeElapsed / duration
        
        # VITESSE DE DÉPLACEMENT: Même facteur que la convergence pour la cohérence
        speedFactor: float = 0.5
        adjustedProgress: float = progress * speedFactor
        
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
            
            # Récupérer la position initiale
            initialX: float = supnova_dict['spiralX'][i]
            initialY: float = supnova_dict['spiralY'][i]
            
            # EFFACER: Dessiner en noir à la position courante
            tri.draw(self.screen, (0, 0, 0))
            
            # CONTINUE IN DIRECTION OF THE CENTER WITH THE FADE
            currentX: float = initialX + (x - initialX) * (1.0 + adjustedProgress)
            currentY: float = initialY + (y - initialY) * (1.0 + adjustedProgress)
            
            # MOVE TRIANGLE
            offsetX: float = currentX - initialX
            offsetY: float = currentY - initialY
            tri.move(Vector2(offsetX, offsetY))
            
            # MAKE COLOR FOR THE FADE
            fadeColor = (
                int(255 * (1 - progress)),
                int(255 * (1 - progress)),
                int(255 * (1 - progress))
            )
            
            # REDRAW AND MAKE THE FADE
            tri.draw(self.screen, fadeColor)

    def _drawSupnovaDestruction(
        self,
        supnova_dict: Dict[str, Any]
    ) -> None:
        for i in range(len(supnova_dict['triangle'])):
            tri = supnova_dict['triangle'][i]
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
        self.windownInit()
        self.drawStars(self.nStars)
        pygame.mixer.music.load(self.midi_path)

        
        planet = Planet(Vector2(self.screenWidth/2, self.screenHeight/2), 100, self.grammar.seed)
        ring = Ring(planet)
        spaceShip = SpaceShip(Vector2(planet.origin.x + planet.radius * 2, planet.origin.y), planet.origin)
        self.grammar.genShip(spaceShip)
        pltShip = self.grammar.genPalette(5) # Ship has 5 parts
        pltUpperRing = self.grammar.genPalette(360) # Ship has 5 parts
        pltLowerRing = self.grammar.genPalette(360) # Ship has 5 parts

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
                    note2TimestmpStart = self.Instr2Notes[nextNoteSeq2Idx].start -3
                    
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
                    supnova['triangle'].clear()
                    supnova['spiralX'].clear()
                    supnova['spiralY'].clear()
                    supnova['color'].clear()
    
                    # REMOVE EXPIRED SUPERNOVA FROM ACTIVE LIST
                    self.supnovaActiveList.remove(supnova)

            spaceShip.eraseDrawing(self.screen)
            ring.drawLowerRing(self.screen, pltLowerRing)
            spaceShip.rotateShip(0.001)
            spaceShip.drawShip(self.screen, pltShip)
            spaceShip.drawBeam(self.screen)
            planet.drawPlanet(self.screen)
            ring.drawUpperRing(self.screen, pltUpperRing)
            
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