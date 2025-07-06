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

def title_screen(screen, clock):
    title_font = pygame.font.Font(None, 80)
    info_font = pygame.font.Font(None, 36)
    
    screen_width, screen_height = screen.get_size()
    logo = util.load_surface('logo.jpg')
    logo = pygame.transform.smoothscale(logo, (200,200))
    logo_rect = logo.get_rect(center=(screen_width // 2, 100))
    
    # Define buttons
    arcade_button = pygame.Rect(screen_width //2 - 100, 300, 200, 50)
    level_button = pygame.Rect(screen_width //2 - 100, 380, 200, 50)
    
    selected_mode = None
    
    while selected_mode is None:
        screen.fill((243,252,255))
        screen.blit(logo, logo_rect)
        
        title_text = title_font.render("PHOTO HUNT", True, (0,0,0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 200))
        
        mouse_pos = pygame.mouse.get_pos()
        for button, label in [(arcade_button, "Arcade Mode"), (level_button, "Select Level")]:
            color = (100, 200, 100) if button.collidepoint(mouse_pos) else (50, 150, 50)
            pygame.draw.rect(screen, color, button)
            text = info_font.render(label, True, (255,255,255))
            screen.blit(text, text.get_rect(center=button.center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if arcade_button.collidepoint(event.pos):
                    selected_mode = "arcade"
                elif level_button.collidepoint(event.pos):
                    selected_mode = "select_level"
            
        clock.tick(60)
        
    return selected_mode

def level_selection(screen, clock, font):
    screen_width, screen_height = screen.get_size()
    
    level_buttons = {
        "Stage 1": pygame.Rect(220, 200, 200, 50),
        "Stage 2": pygame.Rect(220, 270, 200, 50),
        "Stage 3": pygame.Rect(220, 340, 200, 50)
    }
    
    selected_level = None
    
    while selected_level is None:
        screen.fill((20,20,20))
        title = font.render("Select a Stage", True, (255,255,255))
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))
        
        mouse_pos = pygame.mouse.get_pos()
        for name, rect in level_buttons.items():
            color = (0, 128, 255) if rect.collidepoint(mouse_pos) else (0, 80, 180)
            pygame.draw.rect(screen, color, rect)
            label = font.render(name, True, (255,255,255))
            screen.blit(label, label.get_rect(center=rect.center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, rect in level_buttons.items():
                    if rect.collidepoint(event.pos):
                        return int(name[-1])
                
        clock.tick(60)

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


def load_stage(stage):
    if stage == 1:
        return (
            util.load_surface('Pic1L.jpg'),
            util.load_surface('Pic1R.jpg'),
            [(32,272),(152,224),(27,402),(296,445),(198,261)],
            [(352,272),(472,224),(347,402),(616,445),(518,261)]
        )
    elif stage == 2:
        return (
            util.load_surface('Pic2L.jpg'),
            util.load_surface('Pic2R.jpg'),
            [(265,299),(173,489),(195,349),(139,380),(89,307)],
            [(585,299),(503,489),(515,349),(459,380),(409,307)]
        )
    elif stage == 3:
        return (
            util.load_surface('Pic3L.jpg'),
            util.load_surface('Pic3R.jpg'),
            [(57,269),(215,221),(190,392),(108,452),(13,447)],
            [(377,269),(535,221),(510,392),(428,452),(333,447)]
        )
    else:
        return None, None, [], []
    
# MAIN GAMEPLAY LOOP #

def run_game(screen, clock, font, difficulty, settings, stages):
    while True:
        bgImage = util.load_surface('background.jpg')
        redcircle = util.load_image('redCircle.png',-1)
        tolerance = settings["tolerance"] # Set how far apart the user can click from the center of error 
        currTime = settings["time"]
        TimePenalty = settings["time_penalty"] # For being terrible at the game
        lives = settings["lives"]
        time_bonus = settings["time_bonus"] # For getting a difference correct
        gameOver = False
        
        stage_index = 0
        currStage = stages[stage_index]
        leftPhoto, rightPhoto, errorLocationsLeft, errorLocationsRight = load_stage(currStage)
        loaded = False
        errorFound = [False,False,False,False,False]
        
        while not gameOver:
            #Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == MOUSEBUTTONDOWN and not gameOver:
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
            
            if not loaded:            
                errorFound = [False,False,False,False,False]
                loaded = True 
                   
            #Handle Game Logic Updates
            if errorFound == [True,True,True,True,True]:
                stage_index += 1
                if stage_index >= len(stages):
                    gameOver = True
                else:
                    currStage = stages[stage_index]
                    currTime = settings["time"]
                    loaded = False
                    leftPhoto, rightPhoto, errorLocationsLeft, errorLocationsRight = load_stage(currStage)
                    errorFound = [False, False, False, False, False]                    
                
            # Decrease Time
            currTime = currTime -1
        
            # Time is up/Lives are gone
            if currTime < 0 or lives <= 0:
                gameOver = True
                
        
            # Drawing
            screen.blit(bgImage, (0, 0))
            screen.blit(leftPhoto, (10, 200))
            screen.blit(rightPhoto, (330, 200))
            for i in range(5):
                if errorFound[i]:
                    # Cater for offsect of circle
                    LeftCirclePosition = (errorLocationsLeft[i][0]-30,errorLocationsLeft[i][1]-30)
                    RightCirclePosition = (errorLocationsRight[i][0]-30,errorLocationsRight[i][1]-30)
                    screen.blit(redcircle[0], LeftCirclePosition)
                    screen.blit(redcircle[0], RightCirclePosition)
                        
                        
            drawText(screen,"Difficulty: ",(220,30),'black',25)
            drawText(screen,difficulty.title(),(380,30),'black',25)
            drawText(screen,"Stage",(270,50),'black',50)
            drawText(screen,str(currStage),(370,50),'black',50)
            drawText(screen, "Time: ",(270,100),'black',30)
            drawText(screen,str(round(currTime / 20)),(340,100),'red',30)
            drawText(screen,"Lives",(270,150),'black',30)
            drawText(screen,str(lives),(340,150),'red',30)

            pygame.display.flip()
            #Control the Frame Per Second
            clock.tick(20)    
        
        # Game over / Win screen #
        font_big = pygame.font.Font(None, 40)
        
        
        retry_button = pygame.Rect(170,400,140,50)
        quit_button = pygame.Rect(330,400,140,50)
        menu_button = pygame.Rect(330, 400,140, 50)
        
        if stage_index >= len(stages):
            continue_button = pygame.Rect(420, 420, 120, 50)
        else:
            continue_button = None
        
        while True:
            screen.fill((0,0,0))
            end_msg = "You Win!" if stage_index >= len(stages) else "Game Over!"
            drawText(screen, end_msg, (65,200), 'red', 120)
            
            mouse_pos = pygame.mouse.get_pos()
                
            button_list = [(retry_button, "Retry")]

            if stage_index >= len(stages):
                button_list.append((continue_button, "Continue"))
            else:
                button_list.append((menu_button, "Main Menu"))
            
            for rect, label in button_list:
                color = (0, 180, 0) if rect.collidepoint(mouse_pos) else (0, 120, 0)
                pygame.draw.rect(screen, color, rect)
                text = font_big.render(label, True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=rect.center))

            if continue_button:
                color = (200, 120, 0) if continue_button.collidepoint(mouse_pos) else (180, 100, 0)
                pygame.draw.rect(screen, color, continue_button)
                text = font_big.render("Continue", True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=continue_button.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if retry_button.collidepoint(event.pos):
                        run_game(screen, clock, font, difficulty, settings, stages)
                        return  # outer while -> retry
                    elif menu_button.collidepoint(event.pos):
                        return  # to title
                    elif continue_button and continue_button.collidepoint(event.pos):
                        premium_upsell_screen(screen, clock, font)
                        return  # after upsell, back to title

            clock.tick(30)
                       
                       
def premium_upsell_screen(screen, clock, font):
    message_lines = [
        "Thanks for playing the demo!",
        "To access over 100 puzzles,",
        "please pay for Photo Hunt Premium,",
        "which costs $59.99."
    ]
    
    back_button = pygame.Rect(250, 450, 140, 50)
    
    while True:
        screen.fill((20,20,20))
        
        for i, line in enumerate(message_lines):
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 150 + i * 50))
            
        mouse_pos = pygame.mouse.get_pos()
        color = (100,100,250) if back_button.collidepoint(mouse_pos) else (50,50,200)
        pygame.draw.rect(screen, color, back_button)
        label = font.render("Back", True, (255,255,255))
        screen.blit(label, label.get_rect(center=back_button.center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return
                
        clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption('Photo Hunt')    
    # clock to control framerate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    while True:
    # Show title screen
        game_mode = title_screen(screen, clock)
        
        if game_mode == "arcade":
            difficulty = difficulty_selection(screen,clock,font)
            settings = difficulty_settings[difficulty]
            stages = [1, 2, 3]
        elif game_mode == "select_level":
            stage_selected = level_selection(screen, clock, font)
            difficulty = "easy"
            settings = difficulty_settings[difficulty]
            stages = [stage_selected]
            
        run_game(screen, clock, font, difficulty, settings, stages)

    

# Execution starts here
main()