#Import Modules
import pygame
from pygame.locals import *
import util
import math

# A function to create text
def drawText(scr, msg, position, colour, size):
    draw_font = pygame.font.Font(None, size)
    draw_color = Color(colour)
    draw_image = draw_font.render(msg, 0, draw_color)
    scr.blit(draw_image, position)

def main():
    #Initialize Window
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Photo Hunt')

    #Create The Backgound Image
    bgImage = util.load_surface('background.jpg')

    #Initialize Game Variables
    currTime = 1200 #60 sec * 20 Frame/Sec = 1200 Frames Total
    currStage = 1
    gameOver = False
    numberOfStages = 1;
    loaded = False
    errorFound = [False,False,False,False,False]
    redcircle = util.load_image('redCircle.png',-1)

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
                pos = pygame.mouse.get_pos()
                # Checks if user click is within a certain radius of error
                counter = 0
                for currE in errorLocationsLeft:
                    if ((math.pow(pos[0] - currE[0],2) +
                         math.pow(pos[1] - currE[1],2)) < tolerance*tolerance):
                        errorFound[counter] = True
                    counter += 1
                counter = 0
                for currE in errorLocationsRight:
                    if ((math.pow(pos[0] - currE[0],2) +
                         math.pow(pos[1] - currE[1],2)) < tolerance*tolerance):
                        errorFound[counter] = True
                    counter += 1                    
                pass

        #Handle Game Logic Updates
        if errorFound == [True,True,True,True,True]:
            currStage += 1
            if currStage > numberOfStages:
                gameOver = True
            currTime = 1200
            loaded = False
            
        if (currStage == 1) and not loaded:
            leftPhoto = util.load_surface('Pic1L.jpg')
            rightPhoto = util.load_surface('Pic1R.jpg')
            errorLocationsLeft = [(32,272),(152,224),(27,402),(296,445),(198,261)]
            errorLocationsRight = [(352,272),(472,224),(347,402),(616,445),(518,261)]
            errorFound = [False,False,False,False,False]
            loaded = True
        
        # Decrease Time
        currTime = currTime -1

        # Time is up
        if currTime < 0:
            gameOver = True

        # Refresh the display
        screen.blit(bgImage, (0, 0))
        if not gameOver:
            screen.blit(leftPhoto, (10, 200))
            screen.blit(rightPhoto, (330, 200))
            
            for i in range(0,5):
                if errorFound[i]:
                    # Cater for offsect of circle
                    LeftCirclePosition = (errorLocationsLeft[i][0]-30,errorLocationsLeft[i][1]-30)
                    RightCirclePosition = (errorLocationsRight[i][0]-30,errorLocationsRight[i][1]-30)
                    screen.blit(redcircle[0], LeftCirclePosition)
                    screen.blit(redcircle[0], RightCirclePosition)
                    
            drawText(screen,"Stage",(270,50),'black',50)
            drawText(screen,str(currStage),(370,50),'black',50)
            drawText(screen, "Time: ",(270,100),'black',30)
            displayTime = round(currTime / 20)
            drawText(screen,str(displayTime),(340,100),'red',30)
        elif currStage > numberOfStages:
            drawText(screen, "YOU WIN!!!",(65,300),'red',120)
        
        else:
            drawText(screen, "GAME OVER",(65,300),'red',120)
        pygame.display.flip()

        #Control the Frame Per Second
        clock.tick(20)

# Execution starts here
main()