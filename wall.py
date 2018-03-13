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
        
        self.min_pt = (pos[0], pos[1])
        self.max_pt = (pos[0] + pos[2], pos[1] + pos[3])
        # pg.draw.rect(parent, color, pos)
    
    def draw(self):
        pg.draw.rect(self.parent, self.color, self.pos)

    def in_wall(self, point):
        x = point[0]
        y = point[1]

        check_x = True if self.pos[0] <= x <= self.pos[0] + self.pos[2] else False
        check_y = True if self.pos[1] <= y <= self.pos[1] + self.pos[3] else False
        #print(self.pos, "----" ,point)
        return True if (check_x and check_y) else False

    
    def in_wall_rectangle(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]

        min_check = self.in_wall(min_pt)
        max_check = self.in_wall(max_pt)

        return (min_check or max_check)


    def in_wall_line(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]
        
        check_X = False if (max_pt[0] < self.min_pt[0]) or (self.max_pt[0] < min_pt[0]) else True
        check_Y = False if (max_pt[1] < self.min_pt[1]) or (self.max_pt[1] < min_pt[1]) else True

        return (check_X and check_Y)
    

    def get_equation(self, points):

        point1, point2 = points

        delta = [p2 - p1 for p1, p2 in zip(point1, point2)]

        
        # ax + by = c
        if  delta[0] == 0:
            a = 1
            b = 0
            c = point1[0]
        else:
            m = delta[1] / delta[0]
            a = -m
            b = 1
            c = -m*point1[0] + point1[1]
        
        return [a, b, c]

    def get_corners(self):
        point1 = self.min_pt
        point2 = (self.max_pt[0], self.min_pt[1])
        point3 = self.max_pt
        point4 = (self.min_pt[0], self.max_pt[1])
        
        return [point1, point2, point3, point4]

    def get_cross(self, l1, l2):
        a = np.array([l1[:2], l2[:2]])
        b = np.array([l1[2], l2[2]])

        return np.linalg.solve(a, b)
    
    def in_wall_sensors(self, sensor_detect, sensor_lst):
        wall_sensor_detect = [False for i in range(len(sensor_lst))]
        check = False

        for i, sensor in enumerate(sensor_lst):
            sensor.equation()
            if not sensor_detect[i]:
                # If sensor has not detect any thing
                min_pt, max_pt = sensor.get_min_max()  
            
                check_X = False if (max_pt[0] < self.min_pt[0]) or (self.max_pt[0] < min_pt[0]) else True
                check_Y = False if (max_pt[1] < self.min_pt[1]) or (self.max_pt[1] < min_pt[1]) else True
                
                check = (check_X and check_Y)

                sensor_detect[i] = check
                wall_sensor_detect[i] = check

            dist_lst = [Fun.inf for s in range(4)]
            
            if check:
                corners = self.get_corners()
                
                sides = [[corners[0], corners[1]],\
                        [corners[1], corners[2]],\
                        [corners[3], corners[2]],\
                        [corners[0], corners[3]]]

                #for p in sides[3]:
                #    pg.draw.circle(self.parent, (244, 255, 21), p, 3)

                sides_lines = [Fun.get_equation(points) for points in sides]
                
                sensor_eq = Fun.get_equation([sensor.get_start(), sensor.get_end()]) 
                
                #print(sensor_eq) 

                for i, l in enumerate(sides_lines):

                    try:
                        intersect = self.get_cross(l, sensor_eq)
                        
                        if Fun.point_between(sides[i][0], intersect, sides[i][1]):
                            dis = Fun.distance([sensor.get_start(), intersect])

                            if dis < 51:
                               # print(dis)
                                pg.draw.circle(self.parent, (255, 0, 0), [int(intersect[0]), int(intersect[1])], 3)
                                dist_lst[i] = dis
                            
                    except Exception as e:
                        print(e)

            if  min(dist_lst) < 51:
                sensor.dist = min(dist_lst)
                sensor.detect = True
            else:
                sensor.dist = Fun.inf
                sensor.detect = False
           
        self.color = self.yellow if True in wall_sensor_detect else self.blue

        return sensor_detect    

