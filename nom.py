import pygame
import random 
import time
from Spaceship import SpaceShip
from pygame import Vector2
import math

class Game:

    nStars = 1000
    screenWidth = 1280
    screenHeight = 768
    tabStarsWidth = []
    tabStarsHeight = []  # LISTS OF COORDS IN ORDER TO DELETE AND MODIFY EACH STARS
    tabStarsColors = []  # LISTS TO STORE THE COLORS OF THE STARS
    startTime = time.time()
    supnovaActiveList = []
    supnovaDuration = 5
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

    def drawSupnovaAtStage(self, x, y, elapsedTime, randomR, randomG, randomB):

        progress = elapsedTime / self.supnovaDuration
        x_formula = progress * 5
        coef = (-16 * (x_formula ** 2) + 80 * x_formula)*0.1

        if progress < 0.5 :

            spiralX = x + (progress*50)*math.cos(progress*100)*random.uniform(0,1.2)
            spiralY = y + (progress*50)*math.sin(progress*100)*random.uniform(0,1.2)

        else : 

            spiralX = x + (progress*50)*math.cos(progress*100)*random.uniform(0,1.2)
            spiralY = y + (progress*50)*math.sin(progress*100)*random.uniform(0,1.2)

        if progress <= 0.5 :
            
            pygame.draw.polygon(self.screen, (progress*2*randomR*random.uniform(0,0.3), progress*2*randomG*random.uniform(0,0.5), progress*2*randomB), [(spiralX, spiralY), (spiralX+0.5, spiralY+1), (spiralX+1, spiralY)])

        else :

            pygame.draw.polygon(self.screen, (0, 0, 0), [(spiralX, spiralY), (spiralX+0.5, spiralY+1), (spiralX+1, spiralY)])

    def destroyRandomStar(self, nStars):
        if nStars > 0:
            randomStars = int(random.uniform(0, nStars))
            x = self.tabStarsWidth[randomStars]
            y = self.tabStarsHeight[randomStars]
            pygame.draw.polygon(self.screen, (0, 0, 0), [(x+1, y), (x+2, y+2), (x, y+2)])
            del self.tabStarsWidth[randomStars]
            del self.tabStarsHeight[randomStars]
            
            # Crée une supernova active
            self.supnovaActiveList.append({
                'x': x,
                'y': y,
                'startTime': time.time(),
                'randomR': int(random.uniform(0, 255)),
                'randomG': int(random.uniform(0, 255)),
                'randomB': int(random.uniform(0, 255))
            })
            
            nStars -= 1



    def onInit(self):
        self.test_pygame_initialization()
        self.drawStars(self.nStars)
        
        spaceShip = SpaceShip(Vector2(self.screenWidth/2 - 300, self.screenHeight/2), 100, math.pi/2)

        
        while self.running:
            currentTime = time.time()
            if ((int(currentTime - self.startTime)) >= 1):
                self.destroyRandomStar(len(self.tabStarsHeight))
            self.moveAllStars(len(self.tabStarsHeight))

            for supnova in self.supnovaActiveList[:]:  # [:] pour copier la liste
                elapsed = time.time() - supnova['startTime']
                if elapsed < self.supnovaDuration:
                    self.drawSupnovaAtStage(
                        supnova['x'],
                        supnova['y'],
                        elapsed,
                        supnova['randomR'],
                        supnova['randomG'],
                        supnova['randomB']
                    )
                else:
                    self.supnovaActiveList.remove(supnova)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()  
            spaceShip.drawShip(self.screen)
        
            pygame.display.flip()



        pygame.quit()

game = Game()
game.onInit()