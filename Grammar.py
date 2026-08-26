from MidiDataExtractor import MidiDataExtractor
from Spaceship import SpaceShip
from pygame import Color
import random
from Palette import Palette

class Grammar():
    def __init__(self, path):
        self.seed = self.generateSeed(path)
        self.SHIPGRAMMAR = None
        self.PALETTEGRAMMAR  = {
            "red": ["dark", "light", "normal"],
            "green": ["dark", "light", "normal"],
            "blue": ["dark", "light", "normal"]
        }

    

    def generateSeed(self, path):
        data = MidiDataExtractor(path)
        seed = round((data.getNotesCount() * data.getMidiDuration() + data.getAvrgVelo() * data.getAvrgPitch()) * 10000)
        print(int(str(seed)[:8]))
        return int(str(seed)[:8])

    def shipGenGrammar(self, spaceship:SpaceShip):
        self.SHIPGRAMMAR  = {
            "head": [spaceship.genHead2, spaceship.genHead1],
            "body": [spaceship.genBody1, spaceship.genBody2],
            "wings": [spaceship.genWings1, spaceship.genWings2],
            "prop": [spaceship.genProp1, spaceship.genProp2, ""],
            "booster": [spaceship.genBoosters, ""]
        }


    def genPart(self, symbol, rng):
        options = self.SHIPGRAMMAR[symbol]
        # Choose ship part decided by the seeded rng
        chosen = rng.choice(options)
        if chosen != "":
            chosen()

    def genShip(self, spaceship:SpaceShip):
        self.shipGenGrammar(spaceship)
        # Seeded rng
        rng = random.Random(self.seed)
        self.genPart("head", rng)
        self.genPart("body", rng)
        self.genPart("wings", rng)
        self.genPart("prop", rng)
        self.genPart("booster", rng)
        

    def genPalette(self, nColor:int) -> Palette:
        # Seeded rng
        rng = random.Random(self.seed)
        # Get values from seed
        colors = {
            "red": int(str(self.seed)[5]), 
            "green": int(str(self.seed)[6]), 
            "blue": int(str(self.seed)[7])
        }

        colorAVRG:float = (colors['red'] + colors['green'] + colors['blue']) / 3
        color = min(colors, key=lambda weight: abs(colors[weight] - colorAVRG))
        return Palette(color, self.genPaletteAccent(color, rng), [rng.randint(0, 100) for _ in range(nColor)])


    def genPaletteAccent(self, symbol, rng):
        options = self.PALETTEGRAMMAR[symbol]
        # Choose palette accent decided by the seeded rng
        return rng.choice(options)
