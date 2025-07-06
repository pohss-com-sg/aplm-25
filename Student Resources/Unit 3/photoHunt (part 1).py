#Import Modules
import pygame
from pygame.locals import *
import util
import math

def main():
    #Initialize Window
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Photo Hunt')

    #Create The Backgound Image
    bgImage = util.load_surface('background.jpg')

    #Initialize Game Variables
    currTime = 1200 # 60 sec * 20 Frame/Sec = 1200 Frames Total
    currStage = 1
    gameOver = False

    #Set how far apart the user can click from the center of error
    tolerance = 15

    # clock to control framerate
    clock = pygame.time.Clock()

    while 1:
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                pass

        #Handle Game Logic Updates
        # Decrease Time
        currTime = currTime -1

        # Time is up
        if currTime < 0:
            gameOver = True

        # Refresh the display
        screen.blit(bgImage, (0, 0))
        pygame.display.flip()

        #Control the Frame Per Second
        clock.tick(20)

# Execution starts here
main()