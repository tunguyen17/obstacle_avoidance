import pygame as pg

class Wall():
    def __init__(self, parent, color, pos):
        self.parent = parent
        self.color = color
        self.pos = pos

        pg.draw.rect(parent, color, pos)
    
    def in_wall(self, point):
        x = point[0]
        y = point[1]

        check_x = True if self.pos[0] <= x <= self.pos[2] else False
        check_y = True if self.pos[1] <= y <= self.pos[3] else False
        print(self.pos, "----" ,point)
        return True if (check_x and check_y) else False
        
