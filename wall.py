import pygame as pg

class Wall():
    def __init__(self, parent, color, pos):
        self.parent = parent
        self.color = color
        self.pos = pos
        
        self.min_pt = (pos[0], pos[1])
        self.max_pt = (pos[0] + pos[2], pos[1] + pos[3])
        pg.draw.rect(parent, color, pos)
    
    def in_wall(self, point):
        x = point[0]
        y = point[1]

        check_x = True if self.pos[0] <= x <= self.pos[0] + self.pos[2] else False
        check_y = True if self.pos[1] <= y <= self.pos[1] + self.pos[3] else False
        #print(self.pos, "----" ,point)
        return True if (check_x and check_y) else False

    
    def in_wall_min_max(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]

        min_check = self.in_wall(min_pt)
        max_check = self.in_wall(max_pt)

        return (min_check or max_check)


    def in_wall_min_max2(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]

        min_check = self.in_wall(min_pt)
        max_check = self.in_wall(max_pt)

        return (min_check or  max_check)
