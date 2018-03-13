import pygame as pg
import numpy as np
import sensor 

class Car(pg.Surface):
    def __init__(self, parent, xpos, ypos, width, height, angle = 1, delta = 18, step = 5):
        '''
            parent = screen
        '''
        
        # Colors
        self.red = (255, 0, 0, 150)
        self.green = (0, 255, 0, 150)

        # Initialize the surface
        super().__init__((width, height), pg.SRCALPHA)
        
        # Store the information
        self.xpos = xpos
        self.ypos = ypos
        
        # Saving original position
        self.xpos0 = xpos
        self.ypos0 = ypos

        self.parent = parent
        
        self.angle = angle

        self.angle0 = angle

        self.delta = delta # angle
        self.step = step # position
        
        self.width = width
        self.height = height

        self.carWidth = 40
        self.carHeight = 18
    

        center_x =  (width - self.carWidth)/2
        center_y =  (height - self.carHeight)/2
        
        # self.fill((255,0,0))

        # draw the rectangle
        pg.draw.rect(self, pg.Color('aquamarine3'), ( center_x, center_y, self.carWidth, self.carHeight))
        # get the position for the rectangle
        self.rect = self.get_rect(center=(xpos, ypos))
        
        # rotate the image to the original position
        self.image = pg.transform.rotozoom(self, 0, 1)
        
        sensor1 = sensor.Sensor(self, (center_x + self.carWidth, height/2), 0, self.green) 
        sensor2 = sensor.Sensor(self, (center_x + self.carWidth, height/2 + 10), -30, self.green) 
        sensor3 = sensor.Sensor(self, (center_x + self.carWidth, height/2 - 10), 30, self.green)
        
        sensor4 = sensor.Sensor(self, (0.51*width, center_y + self.carHeight), -80, self.green) 
        sensor5 = sensor.Sensor(self, (0.51*width, center_y ), 80, self.green) 

        self.sensors = [sensor1, sensor2, sensor3, sensor4, sensor5] 

#        for sen in self.sensors:
#            sen.update()

        # draw guide line
        # pg.draw.line(self, (225, 0, 0, 255), (0, 0), (width,0), 10 )
        # pg.draw.line(self, (0, 255, 0, 255), (0, 0), (0, height), 10 )

    def update(self):
        for sen in self.sensors:
           color = self.red if sen.detect else self.green
           pg.draw.line(self, color, sen.start, sen.end, 2)
        
        # rotate the image
        self.image = pg.transform.rotozoom(self, self.angle, 1)

        # get the new rect after rotate
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.rect.center[0]
        # copy the new rect to the image
        self.parent.blit(self.image, self.rect)


    def rotate(self, direction):
        # rotate the imange
        self.angle += direction*self.delta
        #self.image = pg.transform.rotozoom(self, self.angle, 1)

    
    def move(self, direction):
        # calculate + update position
        self.xpos += direction*self.step*np.cos(np.deg2rad(self.angle))
        self.ypos -= direction*self.step*np.sin(np.deg2rad(self.angle))
        
        # update the center
        self.rect.center = (self.xpos, self.ypos)
    
    def reset(self):
        # update the center
        self.xpos = self.xpos0 
        self.ypos = self.ypos0
        self.angle = self.angle0
        self.rect.center = (self.xpos, self.ypos)

    def get_corners(self):
        delta_x_1 = self.carWidth*np.cos(np.deg2rad(self.angle))/2
        delta_x_2 = self.carHeight*np.sin(np.deg2rad(self.angle))/2

        delta_y_1 = self.carWidth*np.sin(np.deg2rad(self.angle))/2
        delta_y_2 = self.carHeight*np.cos(np.deg2rad(self.angle))/2

        xpos = self.xpos
        ypos = self.ypos

        A_x = xpos + delta_x_1 + delta_x_2
        A_y = ypos - delta_y_1 + delta_y_2

        B_x = xpos - delta_x_1 - delta_x_2
        B_y = ypos + delta_y_1 - delta_y_2

        C_x = xpos + delta_x_1 - delta_x_2
        C_y = ypos - delta_y_1 - delta_y_2

        D_x = xpos - delta_x_1 + delta_x_2
        D_y = ypos + delta_y_1 + delta_y_2

        return([(A_x, A_y), (B_x, B_y), (C_x, C_y), (D_x, D_y)])

    def get_min_max(self, round = False):
        delta_x_1 = self.carWidth*np.cos(np.deg2rad(self.angle))/2
        delta_x_2 = self.carHeight*np.sin(np.deg2rad(self.angle))/2

        delta_y_1 = self.carWidth*np.sin(np.deg2rad(self.angle))/2
        delta_y_2 = self.carHeight*np.cos(np.deg2rad(self.angle))/2

        xpos = self.xpos
        ypos = self.ypos

        A_x = xpos + delta_x_1 + delta_x_2
        A_y = ypos - delta_y_1 + delta_y_2

        B_x = xpos - delta_x_1 - delta_x_2
        B_y = ypos + delta_y_1 - delta_y_2

        C_x = xpos + delta_x_1 - delta_x_2
        C_y = ypos - delta_y_1 - delta_y_2

        D_x = xpos - delta_x_1 + delta_x_2
        D_y = ypos + delta_y_1 + delta_y_2
        

        min_x = min([A_x, B_x, C_x, D_x])
        min_y = min([A_y, B_y, C_y, D_y])

        max_x = max([A_x, B_x, C_x, D_x])
        max_y = max([A_y, B_y, C_y, D_y]) 
        
        res = [(int(min_x), int(min_y)), (int(max_x), int(max_y))] if round else [(min_x, min_y), (max_x, max_y)]

        return(res)

       
    def get_origin(self, round = False):
        delta_x_1 = self.width*np.cos(np.deg2rad(self.angle))/2
        delta_x_2 = self.height*np.sin(np.deg2rad(self.angle))/2

        delta_y_1 = self.width*np.sin(np.deg2rad(self.angle))/2
        delta_y_2 = self.height*np.cos(np.deg2rad(self.angle))/2

        xpos = self.xpos
        ypos = self.ypos

        B_x = xpos - delta_x_1 - delta_x_2
        B_y = ypos + delta_y_1 - delta_y_2
        
        res = (int(B_x), int(B_y)) if round else (B_x, B_y)
        return(res)




