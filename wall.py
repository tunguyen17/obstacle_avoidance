import pygame as pg
import numpy as np
import Fun

class Wall():
    def __init__(self, parent, color, pos):
        
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)

        self.parent = parent
        self.color = color
        self.pos = pos
        
        self.min_pt = (self.pos[0], self.pos[1])
        self.max_pt = (self.pos[0] + self.pos[2], self.pos[1] + self.pos[3])
        
        point1 = self.min_pt
        point2 = (self.max_pt[0], self.min_pt[1])
        point3 = self.max_pt
        point4 = (self.min_pt[0], self.max_pt[1])
        
        self.corners = [point1, point2, point3, point4]
        self.sides = [[self.corners[0], self.corners[1]],\
                    [self.corners[1], self.corners[2]],\
                    [self.corners[3], self.corners[2]],\
                    [self.corners[0], self.corners[3]]]

        self.sides_lines = [Fun.get_equation(points) for points in self.sides]
        
    def draw(self):
        pg.draw.rect(self.parent, self.color, self.pos)

    def in_wall(self, point):
        x = point[0]
        y = point[1]

        check_x = True if self.pos[0] <= x <= self.pos[0] + self.pos[2] else False
        check_y = True if self.pos[1] <= y <= self.pos[1] + self.pos[3] else False
        return True if (check_x and check_y) else False

    
    def in_wall_rectangle(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]

        check_x = max_pt[0] <= self.pos[0] or min_pt[0] >= self.pos[0] + self.pos[2]
        check_y = max_pt[1] <= self.pos[1] or min_pt[1] >= self.pos[1] + self.pos[3]


        return (not check_x and not check_y)


    def in_wall_line(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]
        
        check_X = False if (max_pt[0] < self.min_pt[0]) or (self.max_pt[0] < min_pt[0]) else True
        check_Y = False if (max_pt[1] < self.min_pt[1]) or (self.max_pt[1] < min_pt[1]) else True

        return (check_X and check_Y)


    def get_corners(self):
        point1 = self.min_pt
        point2 = (self.max_pt[0], self.min_pt[1])
        point3 = self.max_pt
        point4 = (self.min_pt[0], self.max_pt[1])
        
        return [point1, point2, point3, point4]
    
    def in_wall_sensors(self, sensor_lst):
        wall_sensor_detect = [False for i in range(len(sensor_lst))]
        check = False

        for i, sensor in enumerate(sensor_lst):
            if not sensor.detect:
                # If sensor has not detect any thing
                min_pt, max_pt = sensor.get_min_max()  
            
                check_X = False if (max_pt[0] < self.min_pt[0]) or (self.max_pt[0] < min_pt[0]) else True
                check_Y = False if (max_pt[1] < self.min_pt[1]) or (self.max_pt[1] < min_pt[1]) else True
                
                check = (check_X and check_Y)
                    
            # If sensor detect a wall. Find the coordinate
            if check:
                sensor_start = sensor.get_start()
                sensor_end = sensor.get_end()

                sensor_eq = Fun.get_equation([sensor_start, sensor_end]) 
                
                intersect_lst = []
                dist_lst = []

                wall_detected = False

                # Find the intersection point
                for i, l in enumerate(self.sides_lines):
                    intersect = Fun.get_cross(l, sensor_eq)
                    
                    if Fun.point_between(self.sides[i][0], intersect, self.sides[i][1]) and Fun.point_between(sensor_start, intersect, sensor_end):
                        dist = Fun.distance([sensor.get_start(), intersect])

                        if dist < sensor.reach + 1:
                            intersect_lst.append(intersect)
                            dist_lst.append(dist)

                            wall_detected = True
                            
                if  wall_detected:
                    
                    sensor.dist = min(dist_lst)
                    
                    intersect_pt = intersect_lst[dist_lst.index(sensor.dist)]

                    pg.draw.circle(self.parent, (255, 0, 0), Fun.round_lst(intersect_pt), 3)
                    
                    sensor.detect = True

                    # Indicate if the wall is detected by any sensor
                    wall_sensor_detect[i] = check

           
        # Change the color when the wall is detected by a sensor
        self.color = self.yellow if True in wall_sensor_detect else self.blue

    def move(self, delta_x = 0, delta_y = 0):
        
        # update position
        self.pos[0] += delta_x
        self.pos[1] += delta_y

        # update position info
        self.min_pt = (self.pos[0], self.pos[1])
        self.max_pt = (self.pos[0] + self.pos[2], self.pos[1] + self.pos[3])
        
        point1 = self.min_pt
        point2 = (self.max_pt[0], self.min_pt[1])
        point3 = self.max_pt
        point4 = (self.min_pt[0], self.max_pt[1])
        
        self.corners = [point1, point2, point3, point4]
        self.sides = [[self.corners[0], self.corners[1]],\
                    [self.corners[1], self.corners[2]],\
                    [self.corners[3], self.corners[2]],\
                    [self.corners[0], self.corners[3]]]

        self.sides_lines = [Fun.get_equation(points) for points in self.sides]


    def set_pos(self, new_x = 0, new_y = 0):
        
        # update position
        self.pos[0] = new_x
        self.pos[1] = new_y

        # update position info
        self.min_pt = (self.pos[0], self.pos[1])
        self.max_pt = (self.pos[0] + self.pos[2], self.pos[1] + self.pos[3])
        
        point1 = self.min_pt
        point2 = (self.max_pt[0], self.min_pt[1])
        point3 = self.max_pt
        point4 = (self.min_pt[0], self.max_pt[1])
        
        self.corners = [point1, point2, point3, point4]
        self.sides = [[self.corners[0], self.corners[1]],\
                    [self.corners[1], self.corners[2]],\
                    [self.corners[3], self.corners[2]],\
                    [self.corners[0], self.corners[3]]]

        self.sides_lines = [Fun.get_equation(points) for points in self.sides]
