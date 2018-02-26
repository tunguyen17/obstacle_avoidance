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
    
    # draw rect
    rect = car.Car(screen, 300, 300, 300, 200) 
    rect.rotate(0)
    
        
    done = False
    count = 0
    screen.fill(BG_COLOR)

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
        
        screen.fill(BG_COLOR)

        # 2. Draw rect
        obs_1 = wall.Wall(screen,  blue, (0, 0, max_x, 50))
        obs_2 = wall.Wall(screen,  blue, (0, 0, 50, max_y))
        obs_3 = wall.Wall(screen,  blue, (max_x-50, 0, max_x, max_y))
        obs_4 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))
        
        obs_5 = wall.Wall(screen,  blue, (50, 50, 150, 250))
        obs_6 = wall.Wall(screen,  blue, (400, 200, 410, 220))
        #obs_7 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))
        #obs_8 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))
        #obs_9 = wall.Wall(screen,  blue, (0, max_y-50, max_x, max_y))

        obs_lst = [obs_1, obs_2, obs_3, obs_4, obs_5, obs_6]

#        print(rect.xpos, ",  ", rect.ypos)

       
        # Checking for collisions
        for corner in rect.get_corners():
            pg.draw.circle(screen, blue, corner , 5)

            for obs in obs_lst:
                if obs.in_wall(corner):
                    rect.reset() 

        # pg.draw.circle(screen, (255, 0, 0), rect.get_origin(), 5)

        for sen in rect.sensors:
            point = sen.get_end()

#            for obs in obs_lst: 
#                color = (255, 0, 0) if obs.in_wall(point) else (255, 255, 0)
#                pg.draw.circle(screen,  color, point, 5)

            for obs in obs_lst:
                if obs.in_wall(point): 
                    pg.draw.circle(screen, (255, 0, 0), point, 5)

        # 3. copy/redraw the rectangle
        rect.update()


        # Update display
        pg.display.flip()
        
        clock.tick(30)

if __name__ == "__main__":
    main()
