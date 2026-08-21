from MidiDataExtractor import MidiDataExtractor
from Spaceship import SpaceShip
from pygame import Color

class Grammar():
    def __init__(self, path):
        self.seed = self.generateSeed(path)

    

    def generateSeed(self, path):
        data = MidiDataExtractor(path)
        seed = round((data.getNotesCount() * data.getMidiDuration() + data.getAvrgVelo() * data.getAvrgPitch()) * 10000)
        print(int(str(seed)[:8]))
        return int(str(seed)[:8])
        # 1 : Chance for head
        # 2 : Chance for body
        # 3 : Chance for wings
        # 4 : Chance for thruster
        # 5 : Chance for extra boosters
        # 6 : Chance for RED color
        # 7 : Chance for GREEN color
        # 8 : Chance for BLUE color

    def shipGenGrammar(self, spaceship:SpaceShip):
        headSeed = int(str(self.seed)[0])
        bodySeed = int(str(self.seed)[1])
        wingsSeed = int(str(self.seed)[2])
        propSeed = int(str(self.seed)[3])
        boostSeed = int(str(self.seed)[4])

        ###### HEAD RULE #####
        if headSeed in range(0, 4):
            spaceship.genHead1()
        else:
            spaceship.genHead2()

        ###### BODY RULE #####
        if bodySeed in range(0, 5):
            spaceship.genBody1()
        else:
            spaceship.genBody2()
            
        ###### WINGS RULE #####
        if wingsSeed in range(0, 5):
            spaceship.genWings1()
        else:
            spaceship.genWings2()

        ###### THRUST RULE #####
        if propSeed in range(0, 5):
            spaceship.genProp1()
        if propSeed in range(4, 8):
            spaceship.genProp2()        

        ###### EXTRA BOOSTER RULE #####
        if boostSeed in range(0, 3):
            spaceship.genBoosters()
        

    def paletteGrammar(self) -> Color:
        REDSeed = str(self.seed)[5]
        GREENSeed = str(self.seed)[6]
        BLUESeed = str(self.seed)[7]