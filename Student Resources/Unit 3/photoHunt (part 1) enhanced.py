#Import Modules
import pygame
from pygame.locals import *
import util
import math
import random

# A function to create text
def drawText(scr, msg, position, colour, size):
    draw_font = pygame.font.Font(None, size)
    draw_color = Color(colour)
    draw_image = draw_font.render(msg, 0, draw_color)
    scr.blit(draw_image, position)

# Dictonary to define difficulty settings
difficulty_settings = {
    "easy": {
        "time": 600, # 30 sec
        "lives": 7,
        "tolerance": 20,
        "time_bonus": 200, # 10 sec
        "time_penalty": 100, # 5 sec
    },
    "medium": {
        "time": 300, # 15 sec
        "lives": 4,
        "tolerance": 15,
        "time_bonus": 100, # 5 sec
        "time_penalty": 200, # 10 sec
    },
    "hard": {
        "time": 100, # 5 sec 
        "lives": 2,
        "tolerance": 10,
        "time_bonus": 20, # 1 sec
        "time_penalty": 200, # 10 sec 
    },
    "random": {
        "time": random.randint(100, 6000),
        "lives": random.randint(1, 15),
        "tolerance": random.randint(5, 35),
        "time_bonus": random.randint(-400, 400),
        "time_penalty": random.randint(100, 6000),
    },
}    

def difficulty_selection(screen, clock, font):
    buttons = {
        "easy": pygame.Rect(220, 100, 200, 60),
        "medium": pygame.Rect(220, 200, 200, 60),
        "hard": pygame.Rect(220, 300, 200, 60),
        "random": pygame.Rect(220, 400, 200, 60)
    }
    
    selected = None
    running = True
    while running:
        screen.fill((30,30,30))
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                for diff, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        selected = diff
                        running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_1:
                    selected = "easy"
                    running = False
                elif event.key == pygame.K_2:
                    selected = "medium"
                    running = False
                elif event.key == pygame.K_3:
                    selected = "hard"
                    running = False
                elif event.key == pygame.K_4:
                    selected = "random"
                    running = False
        
        for diff, rect in buttons.items():
            color = (0, 200, 0) if rect.collidepoint(mouse_pos) else (0, 150, 0)
            pygame.draw.rect(screen, color, rect)
            label = font.render(diff.capitalize(), True, (255,255,255))
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)
            
        instr = font.render("Click or press 1, 2, 3, 4 to select difficulty", True, (200,200,200))
        screen.blit(instr, (20,20))
        
        pygame.display.flip()
        clock.tick(60)
    
    return selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Photo Hunt')    
    
    # clock to control framerate
    clock = pygame.time.Clock()    
    
    font = pygame.font.Font(None, 36)
    
    #Initialize Difficulty
    difficulty = difficulty_selection(screen, clock, font)
    settings = difficulty_settings[difficulty]


    #Create The Backgound Image
    bgImage = util.load_surface('background.jpg')
    
    currTime = settings["time"]
    TimePenalty = settings["time_penalty"] # For being terrible at the game
    currStage = 1
    gameOver = False
    numberOfStages = 1;
    lives = settings["lives"]
    time_bonus = settings["time_bonus"] # For getting a difference correct
    loaded = False
    tolerance = settings["tolerance"] # Set how far apart the user can click from the center of error 
    errorFound = [False,False,False,False,False]
    redcircle = util.load_image('redCircle.png',-1)



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
                hit = False
                # Checks if user click is within a certain radius of error, deducts 1 life if not
                
                counter = 0
                for currE in errorLocationsLeft:
                    dx = pos[0] - currE[0]
                    dy = pos[1] - currE[1]
                    if dx*dx + dy*dy < tolerance*tolerance:
                        if not errorFound[counter]:
                            errorFound[counter] = True
                            currTime += time_bonus
                        hit = True
                    counter += 1
                        
                counter = 0
                for currE in errorLocationsRight:
                    dx = pos[0] - currE[0]
                    dy = pos[1] - currE[1]                    
                    if dx*dx + dy*dy < tolerance*tolerance:
                        if not errorFound[counter]:
                            errorFound[counter] = True
                            currTime += time_bonus
                        hit = True
                    counter += 1
                
                if not hit:
                    lives -= 1
                    currTime -= TimePenalty
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
            
        # Zero lives
        if lives <= 0:
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
                    
                    
            drawText(screen,"Difficulty selected: ",(220,30),'black',25)
            drawText(screen,str(difficulty).title(),(380,30),'black',25)
            drawText(screen,"Stage",(270,50),'black',50)
            drawText(screen,str(currStage),(370,50),'black',50)
            drawText(screen, "Time: ",(270,100),'black',30)
            displayTime = round(currTime / 20)
            drawText(screen,str(displayTime),(340,100),'red',30)
            drawText(screen,"Lives",(270,150),'black',30)
            drawText(screen,str(lives),(340,150),'red',30)
        elif currStage > numberOfStages:
            drawText(screen, "YOU WIN!!!",(65,300),'red',120)
        else:
            drawText(screen, "GAME OVER",(65,300),'red',120)
        pygame.display.flip()

        #Control the Frame Per Second
        clock.tick(20)

# Execution starts here
main()
print("Thanks for playing the demo! To access over 100 puzzles, please pay for Photo Hunt Premium, which costs $59.99.")