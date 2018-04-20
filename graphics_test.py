import pygame as pg
import sys
import car
import wall
import fun
import random as rnd

#import someuseful constants
from pygame.locals import *

import numpy as np

# import for learning
import brain as br

def main():
    
    train = False

    # Frame per second
    fps = 60

    # Initialize the learning model
    brain = br.Brain(100, input_shape = 5)
    
    if not train:
        brain.load('good model/saved-model-30-30.h5')

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
        
    obs_5 = wall.Wall(screen,  blue, [330, 140, 200, 60])
    obs_6 = wall.Wall(screen,  blue, [600, 600, 200, 60])

    obs_7 = wall.Wall(screen,  blue, [250, 300, 650, 150])

    obs_lst = [obs_1, obs_2, obs_3, obs_4, obs_5, obs_6, obs_7]
    
    # Initialize learning data
    action_lst = [lambda : rect.rotate(1), lambda : None, lambda : rect.rotate(-1)]
    action_lst_scaled = [0, 0.5, 1]

    # Scalling the input
    sensor_scaled = [fun.scale(fun.inf) for v in rect.sensors]
    
    # state
    s0 = sensor_scaled[:]
    s1 = s0[:]

    # action | 0 - Left | 1 - Straight | 2 - Right 
    a0 = 1
    a1 = 1

    # reward 
    r0 = 0
    r1 = 0

    loop = 0
    # alpha for choosing random action
    p_alpha = 1 if train else 0.001
    
    age = 0
    best_age = 0

    # Simulation loop
    while not done:
        
        if loop % 2 == 0:
            obs_x = int(5*np.cos(loop/200))
            obs_y = int(2*np.sin(loop/50))

            obs_5.move(obs_x, -obs_y)
        
            obs_6.move(-obs_x, obs_y)
            
            obs_7.move(-3*obs_y, 0)

        # Increment iteration
        loop += 1  
        age += 1

        # decrease p_alpha every 100 steps
        if loop % 1000 == 0:
            p_alpha *= 0.9
            print('alpha: ', p_alpha, "\t gamma: ", fun.g(loop))

        # condition to exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                
            
            # Manual action 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                   fps = 30
                   print("fps: ", fps)
                if event.key == pg.K_RIGHT:
                   fps = 60
                   print("fps: ", fps)
                if event.key == pg.K_UP:
                    train = not train
                    print('Trainning ', train)
                if event.key == pg.K_DOWN:
                    brain.save('keysave')

        # repaint background
        screen.fill(BG_COLOR)

        # darw objects
        for obs in obs_lst:
            obs.draw()
        
        # 1. start 
        
        ## get s0
        # s.1 Initialize sensors data
        for sen in rect.sensors:
            sen.dist = fun.inf
            sen.detect = False
        
        # s.2 get sensor reading
        for obs in obs_lst:
            obs.in_wall_sensors(rect.sensors)

        # s.3 save the sensor data
        s0 = [fun.scale(v.dist) for v in rect.sensors]
        

        ## get a0
        if rnd.random() < p_alpha:
            a0 = rnd.randint(0, 2) 
        ## a1 = action choosen by nn
        else:
            a0 = brain.predict_a(s0)
 
        # carry out the action choosen by nn
        action_lst[a0]() 
        rect.move(1)
        
        ## get r
        # Checking for collisions
        for obs in obs_lst:
            # Car collision
            if obs.in_wall_rectangle(rect.get_min_max()):
                rect.reset()
                reward = -500 # car crashed 
                if best_age < age:
                    best_age = age
                    brain.save(age)
                print("\nCRASHED: ", age, "\n")
                age = 0
                break

            # Car not collide
            else: 
                reward = 0  # car still alive
                #if a0 == 1: reward= 20

        ## get s1
        # s.1 Initialize sensors data
        for sen in rect.sensors:
            sen.dist = fun.inf
            sen.detect = False
        
        # s.2 get sensor reading
        for obs in obs_lst:
            obs.in_wall_sensors(rect.sensors)

        # s.3 save the sensor data
        s1 = [fun.scale(v.dist) for v in rect.sensors]

        # reward | r_t
        if reward > -500:
            r = reward + fun.r(min(s1))

        #######################
        memory = [s0, a0, r, s1]

        brain.add_memory(memory)
        
        
        if train:
            brain.train(gamma = fun.g(loop))

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
