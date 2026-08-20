from pygame import Vector2, draw
import math

class SpaceShip():
    def __init__(self, target:Vector2, distance:int, angRad:float):
        self.targetPos = target
        self.dist = distance
        self.angle = angRad
        self.origin = self.calcOrigin()

          
        self.sideLen = 70
        self.angleBody = self.degToRad(15)

    def degToRad(self, angle):
        return angle * math.pi / 180

    def drawCircleOfTriangles(self, screen, radius: int, pos: Vector2, color):

        parts = 360
        positionX = pos.x
        positionY = pos.y

        for i in range(parts):
            angle1 = i * (2 * math.pi / parts)
            angle2 = (i + 1) * (2 * math.pi / parts)
            draw.polygon(screen, color, [(positionX, positionY),
            (positionX + radius * math.cos(angle1), positionY + radius * math.sin(angle1)),
            (positionX + radius * math.cos(angle2), positionY + radius * math.sin(angle2))])


    def drawPlanet(self, parts:int):
        self.drawCircleOfTriangles(100, self.screenWidth // 2, self.screenHeight // 2, (0,204,0))
        for i in range(parts):
            pass

    def drawShip(self, screen):
        self.drawHead1(screen)
        self.drawWings1(screen)
        self.drawBody2(screen)
        self.drawProp2(screen)
        self.drawBoost(screen)

    def drawHead1(self, screen):
        point1 = Vector2(self.origin.x + self.sideLen * math.cos(self.angleBody + self.angle), self.origin.y + self.sideLen * math.sin(self.angleBody + self.angle))
        point2 = Vector2(self.origin.x + self.sideLen * math.cos(-(self.angleBody - self.angle)), self.origin.y + self.sideLen * math.sin(-(self.angleBody - self.angle )))
        draw.polygon(screen, (255, 255, 0), [self.origin, point1, point2])

    def drawBody1(self, screen):      
        point1 = Vector2(self.origin.x + self.sideLen * math.cos(self.angleBody + self.angle), self.origin.y + self.sideLen * math.sin(self.angleBody + self.angle))
        point2 = Vector2(self.origin.x + self.sideLen * math.cos(-(self.angleBody - self.angle)), self.origin.y + self.sideLen * math.sin(-(self.angleBody - self.angle )))
        point3 = Vector2(self.origin.x + (self.sideLen+100) * math.cos(self.angle), self.origin.y + (self.sideLen+100) * math.sin(self.angle))        
        draw.polygon(screen, (255, 0, 0), [point3, point1, point2])

    def drawWings1(self, screen):
        point3Up = Vector2(self.origin.x + (self.sideLen+45) * math.cos(2*self.angle+self.degToRad(5)), self.origin.y + (self.sideLen+45) * math.sin(2*self.angle+self.degToRad(5)))
        point2Up = Vector2(self.origin.x + (self.sideLen+75) * math.cos(2*self.angle+self.degToRad(1)), self.origin.y + (self.sideLen+86) * math.sin(2*self.angle+self.degToRad(1)))
        point1Up = Vector2(self.origin.x + (self.sideLen+150) * math.cos(2*self.angle+self.degToRad(30)), self.origin.y + (self.sideLen+80) * math.sin(self.angle+self.degToRad(30)))
        draw.polygon(screen, (0, 255, 0), [point1Up, point2Up, point3Up])       

        point3Down = Vector2(self.origin.x + (self.sideLen+45) * math.cos(self.angle- (self.angle+self.degToRad(5))), self.origin.y + (self.sideLen+45) * math.sin(self.angle- (self.angle+self.degToRad(5))))
        point2Down = Vector2(self.origin.x + (self.sideLen+75) * math.cos(self.angle- (self.angle+self.degToRad(1))), self.origin.y + (self.sideLen+86) * math.sin(self.angle- (self.angle+self.degToRad(1))))
        point1Down = Vector2(self.origin.x + (self.sideLen+150) * math.cos(self.angle- (self.angle+self.degToRad(30))), self.origin.y + (self.sideLen+80) * math.sin(self.angle- (self.angle+self.degToRad(30))))
        draw.polygon(screen, (0, 255, 0), [point1Down, point2Down, point3Down])    

    def drawProp1(self, screen):
        point1 = Vector2(self.origin.x + (self.sideLen+80) * math.cos(self.angle), self.origin.y + (self.sideLen+80) * math.sin(self.angle)) 
        point2 = Vector2(self.origin.x + (self.sideLen+110) * math.cos(self.angle+self.degToRad(5)), self.origin.y + (self.sideLen+110) * math.sin(self.angle+self.degToRad(5)))
        point3 = Vector2(self.origin.x + (self.sideLen+110) * math.cos(-self.angle-self.degToRad(5)), self.origin.y + (self.sideLen+110) * math.sin(-self.angle-self.degToRad(5)))
        draw.polygon(screen, (0, 0, 255), [point1, point2, point3]) 

    def drawBoost(self, screen):
        point1Up = Vector2(self.origin.x + (self.sideLen+100) * math.cos(2*self.angle+self.degToRad(15)), self.origin.y + (self.sideLen+100) * math.sin(2*self.angle+self.degToRad(15)))
        point2Up = Vector2(point1Up.x + (20) * math.cos(self.angle+self.degToRad(10)), point1Up.y + (20) * math.sin(self.angle+self.degToRad(10)))
        point3Up = Vector2(point1Up.x + (20) * math.cos(self.angle-self.degToRad(10)), point1Up.y + (20) * math.sin(self.angle-self.degToRad(10)))
        draw.polygon(screen, (0, 255, 255), [point1Up, point2Up, point3Up])  

        point1Down = Vector2(self.origin.x + (self.sideLen+100) * math.cos(2*self.angle-self.degToRad(15)), self.origin.y + (self.sideLen+100) * math.sin(2*self.angle-self.degToRad(15)))
        point2Down = Vector2(point1Down.x + (20) * math.cos(self.angle+self.degToRad(10)), point1Down.y + (20) * math.sin(self.angle+self.degToRad(10)))
        point3Down = Vector2(point1Down.x + (20) * math.cos(self.angle-self.degToRad(10)), point1Down.y + (20) * math.sin(self.angle-self.degToRad(10)))        
        draw.polygon(screen, (0, 255, 255), [point1Down, point2Down, point3Down])    

    def drawHead2(self, screen):
        radius = 30
        center = Vector2(self.origin.x + (radius+10) * math.cos(self.angle), self.origin.y + (radius+10) * math.sin(self.angle)) 
        self.drawCircleOfTriangles(screen, radius, center, (255, 255, 0))
        point1 = Vector2(center.x + (radius) * math.cos(self.angle + self.degToRad(90)), center.y + (radius) * math.sin(self.angle + self.degToRad(90))) 
        point2 = Vector2(center.x + (radius) * math.cos(self.angle + self.degToRad(-90)), center.y + (radius) * math.sin(self.angle + self.degToRad(-90))) 
        border = Vector2(center.x + (radius) * math.cos(self.angle), center.y + (radius) * math.sin(self.angle)) 
        point3 = Vector2(border.x + (radius) * math.cos(self.angle + self.degToRad(90)), border.y + (radius) * math.sin(self.angle + self.degToRad(90))) 
        point4 = Vector2(border.x + (radius) * math.cos(self.angle + self.degToRad(-90)), border.y + (radius) * math.sin(self.angle + self.degToRad(-90)))        
        draw.polygon(screen, (255, 255, 0), [point1, point2, point3])         
        draw.polygon(screen, (255, 255, 0), [point3, point2, point4])    

    def drawBody2(self, screen):
        anchor = Vector2(self.origin.x + (65) * math.cos(self.angle), self.origin.y + (65) * math.sin(self.angle)) 
        point1 = Vector2(anchor.x + (35) * math.cos(self.angle + self.degToRad(90)), anchor.y + (35) * math.sin(self.angle + self.degToRad(90))) 
        point2 = Vector2(anchor.x + (35) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (35) * math.sin(self.angle + self.degToRad(-90))) 
        border = Vector2(self.origin.x + (160) * math.cos(self.angle), self.origin.y + (160) * math.sin(self.angle)) 
        point3 = Vector2(border.x + (35) * math.cos(self.angle + self.degToRad(90)), border.y + (35) * math.sin(self.angle + self.degToRad(90))) 
        point4 = Vector2(border.x + (35) * math.cos(self.angle + self.degToRad(-90)), border.y + (35) * math.sin(self.angle + self.degToRad(-90)))          
        draw.polygon(screen, (255, 0, 0), [point1, point2, point3])         
        draw.polygon(screen, (255, 0, 0), [point3, point2, point4])     

    def drawWings2(self, screen):        
        width = 35
        anchor = Vector2(self.origin.x + (120) * math.cos(self.angle), self.origin.y + (120) * math.sin(self.angle)) 
        point1 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(0)), anchor.y + (width) * math.sin(self.angle + self.degToRad(0))) 
        point2 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(180)), anchor.y + (width) * math.sin(self.angle + self.degToRad(180))) 
        point3Up = Vector2(anchor.x + (100) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (100) * math.sin(self.angle + self.degToRad(-90))) 
        point4Up = Vector2(point3Up.x + (2*width) * math.cos(self.angle + self.degToRad(0)), point3Up.y + (2*width) * math.sin(self.angle + self.degToRad(0)))      
        draw.polygon(screen, (0, 255, 0), [point1, point2, point3Up])         
        draw.polygon(screen, (0, 255, 0), [point3Up, point1, point4Up])     
        
        point3Down = Vector2(anchor.x + (100) * math.cos(self.angle + self.degToRad(90)), anchor.y + (100) * math.sin(self.angle + self.degToRad(90))) 
        point4Down = Vector2(point3Down.x + (2*width) * math.cos(self.angle + self.degToRad(0)), point3Down.y + (2*width) * math.sin(self.angle + self.degToRad(0)))      
        draw.polygon(screen, (0, 255, 0), [point1, point2, point3Down])         
        draw.polygon(screen, (0, 255, 0), [point3Down, point1, point4Down])    

    def drawProp2(self, screen):     
        width = 15
        anchor = Vector2(self.origin.x + (self.sideLen+80) * math.cos(self.angle), self.origin.y + (self.sideLen+80) * math.sin(self.angle))  
        point1 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(-90)), anchor.y + (width) * math.sin(self.angle + self.degToRad(-90))) 
        point2 = Vector2(anchor.x + (width) * math.cos(self.angle + self.degToRad(90)), anchor.y + (width) * math.sin(self.angle + self.degToRad(90))) 
        anchor2 = Vector2(anchor.x + (50) * math.cos(self.angle + self.degToRad(0)), anchor.y + (50) * math.sin(self.angle + self.degToRad(0))) 
        point3 = Vector2(anchor2.x + (width/2) * math.cos(self.angle + self.degToRad(-90)), anchor2.y + (width/2) * math.sin(self.angle + self.degToRad(-90))) 
        point4 = Vector2(anchor2.x + (width/2) * math.cos(self.angle + self.degToRad(90)), anchor2.y + (width/2) * math.sin(self.angle + self.degToRad(90))) 
          
        draw.polygon(screen, (0, 0, 255), [anchor, point3, point4])
        draw.polygon(screen, (0, 0, 255), [anchor, point1, point3])         
        draw.polygon(screen, (0, 0, 255), [anchor, point2, point4])







    def calcOrigin(self) -> Vector2:
        x = self.targetPos.x + self.dist * math.cos(self.angle)
        y = self.targetPos.y + self.dist * math.sin(self.angle)
        return Vector2(x, y)