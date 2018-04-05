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
from keras.models import Sequential
from keras.layers import Dense


def main():
    
    # Initialize the learning model
    model = Sequential()

    # Input layer has shape of 6
    ## 5 from sensors - state
    ## 1 from action - action
    
    # Hidden Layer 1
    model.add(Dense(70, activation = 'sigmoid', input_shape=(6,), kernel_initializer='random_uniform', bias_initializer = 'Zeros'))
    # Hidden Layer 2
    model.add(Dense(50, activation = 'sigmoid', kernel_initializer='random_uniform', bias_initializer = 'Zeros')) 

    model.add(Dense(30, activation = 'sigmoid', kernel_initializer='random_uniform', bias_initializer = 'Zeros')) 

    model.add(Dense(15, activation = 'sigmoid', kernel_initializer='random_uniform', bias_initializer = 'Zeros')) 

    model.add(Dense(10, activation = 'sigmoid', kernel_initializer='random_uniform', bias_initializer = 'Zeros')) 

    # Output    
    model.add(Dense(3, activation = 'linear', kernel_initializer='random_uniform', bias_initializer = 'Zeros'))
    
    model.compile(optimizer = 'rmsprop', loss = 'mse')


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
    state = sensor_scaled
    s0 = np.array(state)
    s1 = s0.copy()

    # action | 0 - Left | 1 - Straight | 2 - Right 
    a0 = 1
    a1 = 1

    # reward 
    r0 = 0
    r1 = 0

    crashed = False

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

        
        # carry out the action choosen by nn
        action_lst[a1]()

        rect.move(1)
    

        for obs in obs_lst:
            obs.draw()
        
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
            else: 
                reward = 50  # car still alive
                #if a0 == 1: reward=500

            # Sensor detection
            obs.in_wall_sensors(rect.sensors)
       
        # Scalling the input
        sensor_scaled = [Fun.scale(v.dist) for v in rect.sensors]

        # action | a_t
        ## save the previous action
        a0 = a1

        ## a1 = action choosen by nn
        if rnd.random() < 0.2:
            a1 = rnd.randint(0, 2) 
            #a1 = 1 
        else:
            # Copy the old prediction
            try:
                pred0 = pred1.copy()
            except:
                pass
            
            s0a0 = np.array(s0 + a0)[np.newaxis, :]
            pred1 = model.predict(s0a0)
            
#            print(pred1)

            a1 = pred1.argmax()
            
        # Collect data

        # state | s_t
        
        state = sensor_scaled

        # copy old state
        s0 = s1.copy()
        ## get current state
        s1 = np.array(state)
    
        
        # reward | r_t
        r0 = reward
            
        #######################
        memory = (s0, a0, r0, s1, a1)
        
        # reset s1 if crashed
        if crashed:
            sensor_scaled = [Fun.scale(Fun.inf) for v in rect.sensors]
            state = sensor_scaled
            s1 = np.array(state)


        print(memory)

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        
        clock.tick(1000)

if __name__ == "__main__":
    main()
