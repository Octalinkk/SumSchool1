import pygame
import random 
import time
from SoundExtract import *

class Game:

    nStars = 1000
    screenWidth = 1280
    screenHeight = 768
    tabStarsWidth = []      # LISTS OF COORDS IN ORDER TO DELETE AND MODIFY EACH STARS
    tabStarsHeight = []     # LISTS OF COORDS IN ORDER TO DELETE AND MODIFY EACH STARS
    tabStarsColors = []     # LISTS TO STORE THE COLORS OF THE STARS

    def __init__(self):
        self.screen = None
        self.running = True
        self.extract = SoundExtract("test2.mid")
        self.Instr1Notes = self.extract.getNotesForIntru(0)

    def test_pygame_initialization(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption("APP")

    def drawStars(self, nStars):

        for i in range(nStars): 

            randomWidth = int(random.uniform(0,self.screenWidth))
            randomHeight = int(random.uniform(0,self.screenHeight)) # GENRATE A RANDOM WIDTH AND HEIGHT IN ORDER TO GIVE A RANDOM POSITION FOR EVERY STARS 
            randomOpacity = int(random.uniform(0,255))  # FIND A RANDOM OPACITY FOR THE STARS
            pygame.draw.polygon(self.screen, (255-randomOpacity, 255-randomOpacity, 255-randomOpacity), [(randomWidth+1, randomHeight+0), (randomWidth+2, randomHeight+2), (randomWidth+0, randomHeight+2)])
            self.tabStarsWidth.append(randomWidth)
            self.tabStarsHeight.append(randomHeight) # UPDATE THE TABS OF COORDS TO USE IT, IN ORDER TO DELETE THE STARS
            self.tabStarsColors.append(255-randomOpacity)

    def moveAllStars(self,nStars):
        for i in range(nStars):
            
            pygame.draw.polygon(self.screen, (0, 0, 0), [(self.tabStarsWidth[i]+1, self.tabStarsHeight[i]+0), (self.tabStarsWidth[i]+2, self.tabStarsHeight[i]+2), (self.tabStarsWidth[i]+0, self.tabStarsHeight[i]+2)])  
            self.tabStarsHeight[i] = (self.tabStarsHeight[i] + 0.01)%768
            self.tabStarsWidth[i]= (self.tabStarsWidth[i] + 0.1)%1280

            pygame.draw.polygon(self.screen, (self.tabStarsColors[i], self.tabStarsColors[i], self.tabStarsColors[i]), [(self.tabStarsWidth[i]+1, self.tabStarsHeight[i]+0), (self.tabStarsWidth[i]+2, self.tabStarsHeight[i]+2), (self.tabStarsWidth[i]+0, self.tabStarsHeight[i]+2)])
        

    def deleteARandomStar(self,nStars):
        if (nStars > 0) :
            randomStars = int(random.uniform(0,nStars))
            pygame.draw.polygon(self.screen, (100, 0, 100), [(self.tabStarsWidth[randomStars]+1, self.tabStarsHeight[randomStars]+0), (self.tabStarsWidth[randomStars]+2, self.tabStarsHeight[randomStars]+2), (self.tabStarsWidth[randomStars]+0, self.tabStarsHeight[randomStars]+2)])
            del self.tabStarsWidth[randomStars]
            del self.tabStarsHeight[randomStars]
            # Fonction qui fait explosion
            nStars -= 1

    def supernova(x,y):
        randomSize = int(random.uniform(10,50))
        time = 0
        while (time <= 200):
            pass

    def onInit(self):
        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        pygame.mixer.music.load("test2.mid")
        
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
                        self.screen.fill(color=(100, 100, 100)) # A changer l'animation
                        nextNoteIdx += 1 

            self.moveAllStars(len(self.tabStarsHeight))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip() 
        
        pygame.quit()

game = Game()
game.onInit()