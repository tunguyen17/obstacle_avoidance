import pygame as pg
import sys
import car
import wall
import Fun
import random as rnd

#import someuseful constants
from pygame.locals import *

import numpy as np

# import for learning
import Brain as br

def main():
    
    # Initialize the learning model
    brain = br.Brain(500)

    # Initialize graphics stuff
    clock = pg.time.Clock()

    max_x = 1100
    max_y = 800

    # Initialise the pygame module
    pg.init()

    # Create a new drawing surface
    screen = pg.display.set_mode((max_x,  max_y))

    # display surface caption
    pg.display.set_caption('World')
    BG_COLOR = pg.Color('darkslategray')
    
    blue = (0,0,255)
    green = (0, 255,0)
    red = (255, 0, 0)
    yellow = (255, 255, 0)

    # draw rect
    rect = car.Car(screen, 230, 75, 300, 200) 
    rect.rotate(0)
    
    # num sensor
    num_sensor = len(rect.sensors)

    done = False
    count = 0
    screen.fill(BG_COLOR)

    # Draw Walls
    obs_1 = wall.Wall(screen,  blue, (0,   0, max_x, 10))
    obs_2 = wall.Wall(screen,  blue, (0, 0, 10, max_y))
    obs_3 = wall.Wall(screen,  blue, (max_x-10, 0, max_x, max_y))
    obs_4 = wall.Wall(screen,  blue, (0, max_y-10, max_x, max_y))
        
    obs_5 = wall.Wall(screen,  blue, (140, 140, 850, 520))

    obs_lst = [obs_1, obs_2, obs_3, obs_4, obs_5]
    
    # Initialize learning data
    action_lst = [lambda : rect.rotate(1), lambda : None, lambda : rect.rotate(-1)]
    action_lst_scaled = [0, 0.5, 1]
 

    # Scalling the input
    sensor_scaled = [Fun.scale(Fun.inf) for v in rect.sensors]
    
    # state
    s0 = sensor_scaled[:]
    s1 = s0[:]

    # action | 0 - Left | 1 - Straight | 2 - Right 
    a0 = 1
    a1 = 1

    # reward 
    r0 = 0
    r1 = 0

    crashed = False
    
    # initialize buffer 
    buffer = []
    buffer_size = 3

    # Simulation loop
    while not done:
        
        # condition to exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            
            # Manual action 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                   rect.rotate(1)
                if event.key == pg.K_RIGHT:
                    rect.rotate(-1)
                if event.key == pg.K_UP:
                    rect.move(1)
                    pass
                if event.key == pg.K_DOWN:
                    rect.move(-1)
        
        # repaint background
        screen.fill(BG_COLOR)

        # darw objects
        for obs in obs_lst:
            obs.draw()
        
        # 1. start 

        # carry out the action choosen by nn
        action_lst[a1]() 
        rect.move(1)
        
        # Initialize sensors data
        for sen in rect.sensors:
            sen.dist = Fun.inf
            sen.detect = False

        # Checking for collisions
        for obs in obs_lst:
            # Car collision
            if obs.in_wall_rectangle(rect.get_min_max()):
                rect.reset()
                reward = -500 # car crashed 
                crashed = True
                print("\n-----------------CRASHED------------------\n")
                break

            # Car not collide
            else: 
                reward = 0  # car still alive
                if a0 == 1: reward= 20

            # Sensor detection
            obs.in_wall_sensors(rect.sensors)


        # reward | r_t
        r0 = reward
       
        # Scalling the sensor data
        sensor_scaled = [Fun.scale(v.dist) for v in rect.sensors]

        # action | a_t
        ## save the previous action
        a0 = a1
            
        # copy old state
        s0 = s1[:]
        ## get current state
        s1 = sensor_scaled 
    

        ## random action
        if rnd.random() < 0.1:
            a1 = rnd.randint(0, 2) 
        ## a1 = action choosen by nn
        else:
            s0a0 = np.array(s0 + [a0])
            a1 = brain.predict_a(s0a0)
           
        #######################
        memory = [s0, a0, r0, s1, a1]
    
        brain.add_memory(memory)
        
        brain.train()


#            for row in data:
#                print(row)
#            print("\n ----------------  \n")

        # reset s1 if crashed
        if crashed:
            # reset sensor data
            sensor_scaled = [Fun.scale(Fun.inf) for v in rect.sensors]
            s1 = sensor_scaled

            crashed = False

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        
        clock.tick(1000)

if __name__ == "__main__":
    main()
