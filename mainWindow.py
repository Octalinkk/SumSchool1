import pygame
from Spaceship import SpaceShip
from Planet import Planet
from Ring import Ring
from pygame import Vector2
from typing import Optional
from MidiDataExtractor import MidiDataExtractor
from Grammar import Grammar
from AudioConverter import audioToMidi
from StarManager import StarManager


class Game:
    # CLASS CONSTANTS FOR GAME CONFIGURATION
    defPath: str = "./Song/PinkPanther_Both.mp3"

    midi_path: str = defPath.replace(".mp3", ".mid")
    audioToMidi(defPath, midi_path)  # Convert audio to midi
    nStars: int = 500
    screenWidth: int = 1920
    screenHeight: int = 1080
    grammar = Grammar(midi_path)

    def __init__(self):
        self.screen: Optional[pygame.Surface] = None
        self.running: bool = True
        self.extract = MidiDataExtractor(self.midi_path)
        self.Instr1Notes = self.extract.getNotesForIntru(0)
        self.Instr2Notes = self.extract.getNotesForIntru(1)
        self.starManager = StarManager(self.screenWidth, self.screenHeight)

        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("Animation")
        

    def onInit(self) -> None:
        self.starManager.spawnStars(self.nStars, self.screen)
        pygame.mixer.music.load(self.defPath)

        planet = Planet(Vector2(self.screenWidth / 2, self.screenHeight / 2), 100, self.grammar.seed, 2)
        ring = Ring(planet)
        spaceShip = SpaceShip(Vector2(planet.origin.x + planet.radius * 2, planet.origin.y), planet.origin)
        self.grammar.genShip(spaceShip)
        pltShip = self.grammar.genPalette(5)  # Ship has 5 parts
        pltUpperRing = self.grammar.genPalette(360)
        pltLowerRing = self.grammar.genPalette(360)

        pygame.mixer.music.play()


        nextNoteSeq1Idx = 0
        nextNoteSeq2Idx = 0

        while self.running:
            songPos = pygame.mixer.music.get_pos()
            if songPos != -1:
                currentTime = songPos / 1000.0  # Convert to sec

                # Check timing with next note
                if nextNoteSeq2Idx < len(self.Instr2Notes):
                    note2TimestmpStart = self.Instr2Notes[nextNoteSeq2Idx].start - 3

                    if currentTime >= note2TimestmpStart:
                        self.starManager.destroyRandomStar(self.screen)
                        nextNoteSeq2Idx += 1

                # Check timing with next note
                if nextNoteSeq1Idx < len(self.Instr1Notes):
                    note1TimestmpStart = self.Instr1Notes[nextNoteSeq1Idx].start
                    note1TimestmpStop = self.Instr1Notes[nextNoteSeq1Idx].end

                    if currentTime >= note1TimestmpStart:
                        spaceShip.fireBeam()

                    if currentTime >= note1TimestmpStop:
                        spaceShip.stopBeam()
                        nextNoteSeq1Idx += 1

            self.starManager.moveAllStars(self.screen)
            self.starManager.updateAndDrawSupernovas(self.screen)

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

        pygame.quit()


if __name__ == "__main__":
    game: Game = Game()
    game.onInit()