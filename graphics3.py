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
    model.add(Dense(10, activation = 'sigmoid', input_shape=(5,), kernel_initializer='random_uniform', bias_initializer = 'Ones')) # Hidden Layer 1
    model.add(Dense(5, activation = 'sigmoid', kernel_initializer='random_uniform', bias_initializer = 'Ones')) # Hidden Layer 2
    model.add(Dense(3, activation = 'tanh', kernel_initializer='random_uniform', bias_initializer = 'Ones')) # Output
    
    model.compile(optimizer = 'rmsprop', loss = 'mse')


    # Initialize graphics stuff
    clock = pg.time.Clock()

    max_x = 1000
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
    rect = car.Car(screen, 200, 500, 300, 200) 
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
        
    obs_5 = wall.Wall(screen,  blue, (100, 100, 150, 250))
    obs_6 = wall.Wall(screen,  blue, (400, 200, 410, 420))

    obs_lst = [obs_1, obs_2, obs_3, obs_4, obs_5, obs_6]
    
    # Initialize learning data
    
    # state
    s0 = np.array([Fun.inf for sen in rect.sensors])[np.newaxis, :]
    s1 = np.array([Fun.inf for sen in rect.sensors])[np.newaxis, :]
    
    # action | 0 - Left | 1 - Straight | 2 - Right 
    a0 = 1
    a1 = 1

    # reward 
    r0 = 1
    r1 = 1

    # prediction
    pred0 = np.zeros(3)[np.newaxis, :]
    pred1 = np.zeros(3)[np.newaxis, :]

    action_lst = [lambda : rect.rotate(1), lambda : None, lambda : rect.rotate(-1)]

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
    
        # 2. Draw rect
        obs_1.draw()
        obs_2.draw()
        obs_3.draw() 
        obs_3.draw()
        obs_4.draw()
        
        obs_5.draw()
        obs_6.draw()

        
        # Initialize sensors data
        for sen in rect.sensors:
            sen.dist = Fun.inf
            sen.detect = False

        # Checking for collisions
        for obs in obs_lst:
            
            # Car collision
            if obs.in_wall_rectangle(rect.get_min_max()):
                rect.reset()
                reward = -1 # car crashed 
                break
            else: 
                reward = 0 # car still alive
                if a0 == 1: reward+=1
            # Sensor detection
            obs.in_wall_sensors(rect.sensors)
        
        # state
        state = np.array([sensor.dist for sensor in rect.sensors])[np.newaxis, :]
        state = Fun.scale(state)
        # ----------------------
        print(state)
        

        # Collect data

        # state | s_t
        s0 = s1[:] # copy old state
        s1 = state # get current state

        # action | a_t
        a0 = a1
        # a1 = action choosen by nn
        
        if rnd.random() < 0.2:
            a1 = rnd.randint(0, 2) 
        else:
            pred0 = pred1[:]
            pred1 = model.predict(s0)
            a1 = pred1[0].argmax()

        #print(a1)

        # reward | r_t
        r0 = reward
    
        # fit the model
        target = pred0[:]
        #print(target)
        target[0][a0] = 0.9*pred0[0][a0]  + 0.1 * (r0 + 0.3 * pred1[0][a1])

        model.fit(s0, target, batch_size = 1)

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        
        clock.tick(60)

if __name__ == "__main__":
    main()
