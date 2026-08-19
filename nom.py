import pygame
import random 
import time
from Spaceship import SpaceShip
from pygame import Vector2

class Game:

    nStars = 1000
    screenWidth = 1280
    screenHeight = 768
    tabStarsWidth = []
    tabStarsHeight = []  # LISTS OF COORDS IN ORDER TO DELETE AND MODIFY EACH STARS
    tabStarsColors = []  # LISTS TO STORE THE COLORS OF THE STARS
    startTime = time.time()

    def __init__(self):
        self.screen = None
        self.running = True

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

    def supernova(self,x,y):
        randomR = int(random.uniform(0,255))
        randomG = int(random.uniform(0,255))
        randomB = int(random.uniform(0,255))
        pygame.draw.polygon(self.screen, (255, 255, 255), [(x, y), (x+0.5, y+1), (x+1, y)])
        r = int(random.uniform(0,100))
        n = 1
        while r > n:
            
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x+r/n, y+r/n), (x+r/n+0.5, y+r/n+1), (x+r/n+1, y+r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x-r/n, y-r/n), (x-r/n+0.5, y-r/n+1), (x-r/n+1, y-r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x+r/n, y-r/n), (x+r/n+0.5, y-r/n+1), (x+r/n+1, y-r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x-r/n, y+r/n), (x-r/n+0.5, y+r/n+1), (x-r/n+1, y+r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x, y+r/n), (x+0.5, y+r/n+1), (x+1, y+r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x, y-r/n), (x+0.5, y-r/n+1), (x+1, y-r/n)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x+r/n, y), (x+r/n+0.5, y+1), (x+r/n+1, y)])
            pygame.draw.polygon(self.screen, (randomR, randomG, randomB), [(x-r/n, y), (x-r/n+0.5, y+1), (x-r/n+1, y)])

            n += 2

    def deleteARandomStar(self,nStars):
        if (nStars > 0) :
            randomStars = int(random.uniform(0,nStars))
            x = self.tabStarsWidth[randomStars]
            y = self.tabStarsHeight[randomStars]
            pygame.draw.polygon(self.screen, (0, 0, 0), [(x+1, y), (x+2, y+2), (x, y+2)])
            del self.tabStarsWidth[randomStars]
            del self.tabStarsHeight[randomStars]
            self.supernova(x,y)
            nStars -= 1




    def onInit(self):
        
        

        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        
        spaceShip = SpaceShip(Vector2(0, 0), Vector2(0, 0), 0)

        
        while self.running:
            currentTime = time.time()
            if ((int(currentTime - self.startTime)) >= 5):
                self.deleteARandomStar(len(self.tabStarsHeight))
            self.moveAllStars(len(self.tabStarsHeight))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()  
        
        pygame.quit()

game = Game()
game.onInit()