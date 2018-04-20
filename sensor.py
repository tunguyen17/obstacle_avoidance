import pygame as pg
import numpy as np
import fun

class Sensor():
    def __init__(self, car, start, angle, color, reach = 60):
        
        self.red = (255, 0, 0, 150)
        self.green = (0, 255, 0, 150)

        self.car = car
        self.reach = reach
        self.start = start
        self.angle = angle
        
        delx = reach*np.cos(np.deg2rad(self.angle))
        dely = reach*np.sin(np.deg2rad(self.angle))

        self.end = (self.start[0] + delx, self.start[1] - dely)
        
#        tempX = car.xpos + (self.start[0] + self.end[0])*np.cos(np.deg2rad(car.angle)) 
#        tempY = car.ypos + (self.start[1] + self.end[1])*np.sin(np.deg2rad(car.angle)) 
#
#        self.endPoint = (int(tempX), int(tempY))
#
        self.color = self.green
        self.dist = fun.inf
        self.detect = False 
        
#        pg.draw.line(self.car, self.color, self.start, self.end, 2) 

    def get_end(self, round = False):
        
        origin = self.car.get_origin()

        tempX = origin[0] + self.end[0]*np.cos(np.deg2rad(self.car.angle)) + self.end[1]*np.sin(np.deg2rad(self.car.angle)) 
        tempY = origin[1] - self.end[0]*np.sin(np.deg2rad(self.car.angle)) + self.end[1]*np.cos(np.deg2rad(self.car.angle)) 

        endPoint = [int(tempX), int(tempY)] if round else [tempX, tempY]

        return endPoint

    def get_start(self, round = False):
        
        origin = self.car.get_origin()

        start_X = origin[0] + self.start[0]*np.cos(np.deg2rad(self.car.angle)) + self.start[1]*np.sin(np.deg2rad(self.car.angle))
        start_Y = origin[1] - self.start[0]*np.sin(np.deg2rad(self.car.angle)) + self.start[1]*np.cos(np.deg2rad(self.car.angle))

        startPoint = [int(start_X), int(start_Y)] if round else [start_X, start_Y]
        
        return startPoint

    def get_min_max(self):
        
        origin = self.car.get_origin()

        start_X = origin[0] + self.start[0]*np.cos(np.deg2rad(self.car.angle)) + self.start[1]*np.sin(np.deg2rad(self.car.angle))
        start_Y = origin[1] - self.start[0]*np.sin(np.deg2rad(self.car.angle)) + self.start[1]*np.cos(np.deg2rad(self.car.angle)) 

 
        end_X = origin[0] + self.end[0]*np.cos(np.deg2rad(self.car.angle)) + self.end[1]*np.sin(np.deg2rad(self.car.angle))
        end_Y = origin[1] - self.end[0]*np.sin(np.deg2rad(self.car.angle)) + self.end[1]*np.cos(np.deg2rad(self.car.angle)) 
        
        
        min_X = min(start_X, end_X)
        min_Y = min(start_Y, end_Y)

        max_X = max(start_X, end_X)
        max_Y = max(start_Y, end_Y)

        return [[min_X, min_Y], [max_X, max_Y]]


    def update(self):
        self.color = self.red if self.detect else self.green
        
        pg.draw.line(self.car, self.color, self.start, self.end, 2) 


    def equation(self):
        
        start = self.get_start()
        end = self.get_end()

        delta = [p1 - p2 for p1, p2 in zip(start, end)]
        
        
       
        #print(delta,"  :   ",delta[1]/delta[0])

        # ax + by = c
        if delta[0] == 0:
            a = 1
            b = 0
            c = p1[0]
        else:   
            m = delta[1] / delta[0]
            a = -m
            b = 1
            c = -m*start[0] + start[1]
       
        #print(a*start[0] + start[1], " = ", c) 

        return [a, b, c]
        
            
    



