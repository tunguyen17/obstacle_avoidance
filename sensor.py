import pygame as pg
import numpy as np

class Sensor():
    def __init__(self, car, start, angle, reach = 80):
        
        self.car = car
        self.reach = reach
        self.start = start
        self.angle = angle
        
        delx = reach*np.cos(np.deg2rad(self.angle))
        dely = reach*np.sin(np.deg2rad(self.angle))

        self.end = (self.start[0] + delx, self.start[1] - dely)
    
        pg.draw.line(car, (255, 0, 0, 255), self.start, self.end, 3) 
    def update(self):
        self.xpos = self.car.xpos
        self.ypos = self.car.ypos
        
