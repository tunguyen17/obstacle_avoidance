import pygame as pg
import sys
import car
import wall

#import someuseful constants
from pygame.locals import *


def main():
    
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

    # Simulation loop
    while not done:
        
        # condition to exit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            
            # Update based on key

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

        
        # 1. screen color
   #     if count < 50:
   #         count += 1
   #     else:
   #         screen.fill(BG_COLOR)
   #         count = 0
        
        # repaint background
        screen.fill(BG_COLOR)

#        rect.move(1)

        # 2. Draw rect
        obs_1 = wall.Wall(screen,  blue, (0,   0, max_x, 10))
        obs_2 = wall.Wall(screen,  blue, (0, 0, 10, max_y))
        obs_3 = wall.Wall(screen,  blue, (max_x-10, 0, max_x, max_y))
        obs_4 = wall.Wall(screen,  blue, (0, max_y-10, max_x, max_y))
        
        obs_5 = wall.Wall(screen,  blue, (100, 100, 150, 250))
        obs_6 = wall.Wall(screen,  blue, (400, 200, 410, 220))
        #obs_7 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))
        #obs_8 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))
        #obs_9 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))

        obs_lst = [obs_1, obs_2, obs_3, obs_4, obs_5, obs_6]


        # Display the min_max corner of the car 
        for corner in rect.get_min_max():
            pg.draw.circle(screen, yellow, corner, 3)
        
        sensor_detect = [False for i in range(num_sensor)]

        # Checking for collisions
        for obs in obs_lst:
            
            # Car collision
            if obs.in_wall_rectangle(rect.get_min_max()):
                rect.reset()
            
            # Sensor detection
            sensor_detect = obs.in_wall_sensors(sensor_detect, rect.sensors)
        
        # update sensors     
        for i, sen in enumerate(rect.sensors):
            sen.detect = sensor_detect[i]
            #color = red if sen.detect else yellow
            #pg.draw.circle(screen, color, sen.get_end(), 3)

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        
        clock.tick(45)

if __name__ == "__main__":
    main()
