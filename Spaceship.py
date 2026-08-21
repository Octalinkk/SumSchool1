from pygame import Vector2, draw
import math
from Triangle import Triangle

class SpaceShip():
    def __init__(self, origin:Vector2, seed):
        self.angle = 0
        self.origin = origin
        self.headPoints:list[Triangle] = []
        self.bodyPoints:list[Triangle] = []
        self.wingsPoints:list[Triangle] = []
        self.propPoints:list[Triangle] = []
        self.boostPoints:list[Triangle] = []

          
        self.sideLen:int = 70
        self.angleBody:float = self.degToRad(15)

        self.genShip()

    def degToRad(self, angle):
        return angle * math.pi / 180

    def calcCircleOfTriangles(self, radius: int, pos: Vector2, details:int=36):

        positionX = pos.x
        positionY = pos.y
        triangles:list[Triangle] = []

        for i in range(details):
            angle1 = i * (2 * math.pi / details)
            angle2 = (i + 1) * (2 * math.pi / details)
            triangles.append(Triangle(Vector2(positionX, positionY),
                                            Vector2((positionX + radius * math.cos(angle1), positionY + radius * math.sin(angle1))),
            Vector2((positionX + radius * math.cos(angle2), positionY + radius * math.sin(angle2)))))

    def rotateShip(self, target:Vector2, angleRad:float):
        for triangle in self.headPoints:
            triangle.rotate(target, angleRad)
        for triangle in self.bodyPoints:
                    triangle.rotate(target, angleRad)
        for triangle in self.wingsPoints:
                    triangle.rotate(target, angleRad)
        for triangle in self.propPoints:
                    triangle.rotate(target, angleRad)


    def genShip(self):
        self.genHead1()
        self.genBody1()
        self.genWings1()
        self.genProp1()

    def eraseDrawing(self, screen):
        self.drawPart(screen, self.headPoints, (0, 0, 0))
        self.drawPart(screen, self.bodyPoints, (0, 0, 0))
        self.drawPart(screen, self.wingsPoints, (0, 0, 0))
        self.drawPart(screen, self.propPoints, (0, 0, 0))

    def drawShip(self, screen):
            self.eraseDrawing(screen)
            self.drawPart(screen, self.headPoints)
            self.drawPart(screen, self.bodyPoints)
            self.drawPart(screen, self.wingsPoints)
            self.drawPart(screen, self.propPoints)

    def drawPart(self, screen, datas:list[Triangle], color=(255, 255, 0)):
        for triangle in datas:
            triangle.draw(screen, color)

    def genHead1(self):
        point1 = Vector2(self.origin.x + self.sideLen * math.cos(self.angleBody + self.angle), self.origin.y + self.sideLen * math.sin(self.angleBody + self.angle))
        point2 = Vector2(self.origin.x + self.sideLen * math.cos(-(self.angleBody - self.angle)), self.origin.y + self.sideLen * math.sin(-(self.angleBody - self.angle )))
        #draw.polygon(screen, (255, 255, 0), [self.origin, point1, point2])
        self.headPoints = [Triangle(self.origin, point1, point2)]

    def genBody1(self):      
        point1 = Vector2(self.origin.x + self.sideLen * math.cos(self.angleBody + self.angle), self.origin.y + self.sideLen * math.sin(self.angleBody + self.angle))
        point2 = Vector2(self.origin.x + self.sideLen * math.cos(-(self.angleBody - self.angle)), self.origin.y + self.sideLen * math.sin(-(self.angleBody - self.angle )))
        point3 = Vector2(self.origin.x + (self.sideLen+100) * math.cos(self.angle), self.origin.y + (self.sideLen+100) * math.sin(self.angle))        
        #draw.polygon(screen, (255, 0, 0), [point3, point1, point2])
        self.bodyPoints = [Triangle(point3, point1, point2)]

    def genWings1(self):
        point3Up = Vector2(self.origin.x + (self.sideLen+45) * math.cos(2*self.angle+self.degToRad(5)), self.origin.y + (self.sideLen+45) * math.sin(2*self.angle+self.degToRad(5)))
        point2Up = Vector2(self.origin.x + (self.sideLen+75) * math.cos(2*self.angle+self.degToRad(1)), self.origin.y + (self.sideLen+86) * math.sin(2*self.angle+self.degToRad(1)))
        point1Up = Vector2(self.origin.x + (self.sideLen+150) * math.cos(2*self.angle+self.degToRad(30)), self.origin.y + (self.sideLen+80) * math.sin(self.angle+self.degToRad(30)))
        #draw.polygon(screen, (0, 255, 0), [point1Up, point2Up, point3Up])       

        point3Down = Vector2(self.origin.x + (self.sideLen+45) * math.cos(self.angle- (self.angle+self.degToRad(5))), self.origin.y + (self.sideLen+45) * math.sin(self.angle- (self.angle+self.degToRad(5))))
        point2Down = Vector2(self.origin.x + (self.sideLen+75) * math.cos(self.angle- (self.angle+self.degToRad(1))), self.origin.y + (self.sideLen+86) * math.sin(self.angle- (self.angle+self.degToRad(1))))
        point1Down = Vector2(self.origin.x + (self.sideLen+150) * math.cos(self.angle- (self.angle+self.degToRad(30))), self.origin.y + (self.sideLen+80) * math.sin(self.angle- (self.angle+self.degToRad(30))))
        #draw.polygon(screen, (0, 255, 0), [point1Down, point2Down, point3Down])
        self.wingsPoints = [Triangle(point1Up, point2Up, point3Up), Triangle(point1Down, point2Down, point3Down)]    

    def genProp1(self):
        point1 = Vector2(self.origin.x + (self.sideLen+80) * math.cos(self.angle), self.origin.y + (self.sideLen+80) * math.sin(self.angle)) 
        point2 = Vector2(self.origin.x + (self.sideLen+110) * math.cos(self.angle+self.degToRad(5)), self.origin.y + (self.sideLen+110) * math.sin(self.angle+self.degToRad(5)))
        point3 = Vector2(self.origin.x + (self.sideLen+110) * math.cos(-self.angle-self.degToRad(5)), self.origin.y + (self.sideLen+110) * math.sin(-self.angle-self.degToRad(5)))
        #draw.polygon(screen, (0, 0, 255), [point1, point2, point3]) 
        self.propPoints = [Triangle(point1, point2, point3)]

    def genBoosters(self):
        point1Up = Vector2(self.origin.x + (self.sideLen+100) * math.cos(2*self.angle+self.degToRad(15)), self.origin.y + (self.sideLen+100) * math.sin(2*self.angle+self.degToRad(15)))
        point2Up = Vector2(point1Up.x + (20) * math.cos(self.angle+self.degToRad(10)), point1Up.y + (20) * math.sin(self.angle+self.degToRad(10)))
        point3Up = Vector2(point1Up.x + (20) * math.cos(self.angle-self.degToRad(10)), point1Up.y + (20) * math.sin(self.angle-self.degToRad(10)))
        #draw.polygon(screen, (0, 255, 255), [point1Up, point2Up, point3Up])  

        point1Down = Vector2(self.origin.x + (self.sideLen+100) * math.cos(2*self.angle-self.degToRad(15)), self.origin.y + (self.sideLen+100) * math.sin(2*self.angle-self.degToRad(15)))
        point2Down = Vector2(point1Down.x + (20) * math.cos(self.angle+self.degToRad(10)), point1Down.y + (20) * math.sin(self.angle+self.degToRad(10)))
        point3Down = Vector2(point1Down.x + (20) * math.cos(self.angle-self.degToRad(10)), point1Down.y + (20) * math.sin(self.angle-self.degToRad(10)))        
        #draw.polygon(screen, (0, 255, 255), [point1Down, point2Down, point3Down])  
        self.boostPoints = [Triangle(point1Up, point2Up, point3Up), Triangle(point1Down, point2Down, point3Down)]  

    def genHead2(self):
        radius = 30
        center = Vector2(self.origin.x + (radius+10) * math.cos(self.angle), self.origin.y + (radius+10) * math.sin(self.angle)) 
        circle = self.calcCircleOfTriangles(radius, center, 10)
        point1 = Vector2(center.x + (radius) * math.cos(self.angle + self.degToRad(90)), center.y + (radius) * math.sin(self.angle + self.degToRad(90))) 
        point2 = Vector2(center.x + (radius) * math.cos(self.angle + self.degToRad(-90)), center.y + (radius) * math.sin(self.angle + self.degToRad(-90))) 
        border = Vector2(center.x + (radius) * math.cos(self.angle), center.y + (radius) * math.sin(self.angle)) 
        point3 = Vector2(border.x + (radius) * math.cos(self.angle + self.degToRad(90)), border.y + (radius) * math.sin(self.angle + self.degToRad(90))) 
        point4 = Vector2(border.x + (radius) * math.cos(self.angle + self.degToRad(-90)), border.y + (radius) * math.sin(self.angle + self.degToRad(-90)))    

        #draw.polygon(screen, (255, 255, 0), [point1, point2, point3])         
        #draw.polygon(screen, (255, 255, 0), [point3, point2, point4]) 
        self.headPoints = [circle, Triangle(point1, point2, point3), Triangle(point3, point2, point4)]


    def genBody2(self):
        anchor = Vector2(self.origin.x + (65) * math.cos(self.angle), self.origin.y + (65) * math.sin(self.angle)) 
        point1 = Vector2(anchor.x + (35) * math.cos(self.angle + self.degToRad(90)), anchor.y + (35) * math.sin(self.angle + self.degToRad(90))) 
        point2 = Vector2(anchor.x + (35) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (35) * math.sin(self.angle + self.degToRad(-90))) 
        border = Vector2(self.origin.x + (160) * math.cos(self.angle), self.origin.y + (160) * math.sin(self.angle)) 
        point3 = Vector2(border.x + (35) * math.cos(self.angle + self.degToRad(90)), border.y + (35) * math.sin(self.angle + self.degToRad(90))) 
        point4 = Vector2(border.x + (35) * math.cos(self.angle + self.degToRad(-90)), border.y + (35) * math.sin(self.angle + self.degToRad(-90)))          
        #draw.polygon(screen, (255, 0, 0), [point1, point2, point3])         
        #draw.polygon(screen, (255, 0, 0), [point3, point2, point4]) 
        self.bodyPoints = [Triangle(point1, point2, point3), Triangle(point3, point2, point4)]    

    def genWings2(self):        
        width = 35
        anchor = Vector2(self.origin.x + (120) * math.cos(self.angle), self.origin.y + (120) * math.sin(self.angle)) 
        point1 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(0)), anchor.y + (width) * math.sin(self.angle + self.degToRad(0))) 
        point2 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(180)), anchor.y + (width) * math.sin(self.angle + self.degToRad(180))) 
        point3Up = Vector2(anchor.x + (100) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (100) * math.sin(self.angle + self.degToRad(-90))) 
        point4Up = Vector2(point3Up.x + (2*width) * math.cos(self.angle + self.degToRad(0)), point3Up.y + (2*width) * math.sin(self.angle + self.degToRad(0)))      
        #draw.polygon(screen, (0, 255, 0), [point1, point2, point3Up])         
        #draw.polygon(screen, (0, 255, 0), [point3Up, point1, point4Up])     
        
        point3Down = Vector2(anchor.x + (100) * math.cos(self.angle + self.degToRad(90)), anchor.y + (100) * math.sin(self.angle + self.degToRad(90))) 
        point4Down = Vector2(point3Down.x + (2*width) * math.cos(self.angle + self.degToRad(0)), point3Down.y + (2*width) * math.sin(self.angle + self.degToRad(0)))      
        #draw.polygon(screen, (0, 255, 0), [point1, point2, point3Down])         
        #draw.polygon(screen, (0, 255, 0), [point3Down, point1, point4Down]) 
        self.wingsPoints = [Triangle(point1, point2, point3Up), Triangle(point3Up, point1, point4Up), Triangle(point1, point2, point3Down), Triangle(point3Down, point1, point4Down)]   

    def genProp2(self):     
        width = 15
        anchor = Vector2(self.origin.x + (self.sideLen+80) * math.cos(self.angle), self.origin.y + (self.sideLen+80) * math.sin(self.angle))  
        point1 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (width) * math.sin(self.angle + self.degToRad(-90))) 
        point2 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(90)), anchor.y + (width) * math.sin(self.angle + self.degToRad(90))) 
        anchor2 = Vector2(anchor.x + (50) * math.cos(self.angle + self.degToRad(0)), anchor.y + (50) * math.sin(self.angle + self.degToRad(0))) 
        point3 = Vector2(anchor2.x + (width/2) * math.cos(self.angle + self.degToRad(-90)), anchor2.y + (width/2) * math.sin(self.angle + self.degToRad(-90))) 
        point4 = Vector2(anchor2.x + (width/2) * math.cos(self.angle + self.degToRad(90)), anchor2.y + (width/2) * math.sin(self.angle + self.degToRad(90))) 
          
        #draw.polygon(screen, (0, 0, 255), [anchor, point3, point4])
        #draw.polygon(screen, (0, 0, 255), [anchor, point1, point3])         
        #draw.polygon(screen, (0, 0, 255), [anchor, point2, point4])
        self.propPoints = [Triangle(anchor, point3, point4), Triangle(anchor, point1, point3), Triangle(anchor, point2, point4)]
