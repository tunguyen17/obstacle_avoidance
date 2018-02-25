import pygame as pg
import sys
import car

#import someuseful constants
from pygame.locals import *


def main():
    
    clock = pg.time.Clock()

    # Initialise the pygame module
    pg.init()

    # Create a new drawing surface
    screen = pg.display.set_mode((500,  600))
    # display surface caption
    pg.display.set_caption('World')
    BG_COLOR = pg.Color('darkslategray')
    
    rect = car.Car(screen, 300, 300, 300, 200) 
    

    done = False

    angle = 0
    while not done:
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

        
        rect.update()
        
        # screen color
        screen.fill(BG_COLOR)

        # copy/redraw the rectangle
        rect.update()

        # Update display
        pg.display.flip()
        
        clock.tick(30)

if __name__ == "__main__":
    main()
