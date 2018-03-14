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
        #print(self.pos, "----" ,point)
        return True if (check_x and check_y) else False

    
    def in_wall_rectangle(self, min_max):
        min_pt = min_max[0]
        max_pt = min_max[1]

        #min_check = self.in_wall(min_pt)
        #max_check = self.in_wall(max_pt)
        
        check_x = max_pt[0] <= self.pos[0] or min_pt[0] >= self.pos[0] + self.pos[2]
        check_y = max_pt[1] <= self.pos[1] or min_pt[1] >= self.pos[1] + self.pos[3]


        return (not check_x and not check_y)


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
                
                    
            #dist_lst = [Fun.inf for s in range(4)]
            
            # If sensor detect a wall. Find the coordinate
            if check:
               # corners = self.get_corners()
               # 
               # sides = [[corners[0], corners[1]],\
               #         [corners[1], corners[2]],\
               #         [corners[3], corners[2]],\
               #         [corners[0], corners[3]]]

                sensor_start = sensor.get_start()
                sensor_end = sensor.get_end()

                sensor_eq = Fun.get_equation([sensor_start, sensor_end]) 
                
                intersect_lst = []
                dist_lst = []

                wall_detected = False

                # Find the intersection point
                for i, l in enumerate(self.sides_lines):
                    intersect = self.get_cross(l, sensor_eq)
                    
                    if Fun.point_between(self.sides[i][0], intersect, self.sides[i][1]) and Fun.point_between(sensor_start, intersect, sensor_end):
                        dist = Fun.distance([sensor.get_start(), intersect])

                        if dist < 51:
                            intersect_lst.append(intersect)
                            dist_lst.append(dist)

                            wall_detected = True
                            
                            #pg.draw.circle(self.parent, (255, 0, 0), [int(intersect[0]), int(intersect[1])], 3)
                            #dist_lst[i] = dis

                if  wall_detected:
                    
                    sensor.dist = min(dist_lst)
                    
                    intersect_pt = intersect_lst[dist_lst.index(sensor.dist)]

                    pg.draw.circle(self.parent, (255, 0, 0), Fun.round_lst(intersect_pt), 3)
                    
                    sensor.detect = True

                    # Indicate if the wall is detected by any sensor
                    wall_sensor_detect[i] = check

           
        # Change the color when the wall is detected by a sensor
        self.color = self.yellow if True in wall_sensor_detect else self.blue


