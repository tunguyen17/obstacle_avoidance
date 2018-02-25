import pygame as pg
import numpy as np
import sensor 

class Car(pg.Surface):
    def __init__(self, parent, xpos, ypos, width, height, delta = 10, step = 10):
        '''
            parent = screen
        '''

        # Initialize the surface
        super().__init__((width, height), pg.SRCALPHA)
        
        # Store the information
        self.xpos = xpos
        self.ypos = ypos
        self.parent = parent
        self.angle = 0
        self.delta = delta # angle
        self.step = step # position

        self.carWidth = 80
        self.carHeight = 40
    

        center_x =  int((width - self.carWidth)/2)
        center_y =  int((height - self.carHeight)/2)

        # draw the rectangle
        pg.draw.rect(self, pg.Color('aquamarine3'), ( center_x, center_y, self.carWidth, self.carHeight))
        # get the position for the rectangle
        self.rect = self.get_rect(center=(xpos, ypos))
        
        # rotate the image to the original position
        self.image = pg.transform.rotozoom(self, 0, 1)
        
        sensor.Sensor(self, (center_x + self.carWidth, int(height/2)), 0) 
        sensor.Sensor(self, (center_x + self.carWidth, int(height/2) + 10), -30) 
        sensor.Sensor(self, (center_x + self.carWidth, int(height/2) - 10), 30) 
        
        sensor.Sensor(self, (self.carWidth + 70, center_y + self.carHeight), -80) 
        sensor.Sensor(self, (self.carWidth + 70, center_y ), 80) 

        # draw guide line
        # pg.draw.line(self, (225, 0, 0, 255), (0, 0), (width,0), 10 )
        # pg.draw.line(self, (0, 255, 0, 255), (0, 0), (0, height), 10 )

    def update(self):
        # get the new rect after rotate
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.rect.center[0]
        # copy the new rect to the image
        self.parent.blit(self.image, self.rect)


    def rotate(self, direction):
        # rotate the imange
        self.angle += direction*self.delta
        self.image = pg.transform.rotozoom(self, self.angle, 1)

    
    def move(self, direction):

        # calculate + update position
        self.xpos += direction*self.step*np.cos(np.deg2rad(self.angle))
        self.ypos -= direction*self.step*np.sin(np.deg2rad(self.angle))
        
        # update the center
        self.rect.center = (self.xpos, self.ypos)
        
