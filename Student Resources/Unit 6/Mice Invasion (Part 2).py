#Import Modules
import os, pygame
from pygame.locals import *
import util
import random
# Some constants defined
SCREENRECT = Rect(0, 0, 405, 405)


difficulty_settings = {
    'easy': {
        'mouse_speed': 3,
        'spawn_rate': 50,
        'score_multiplier': 0.75,
    },
    'medium': {
        'mouse_speed': 5,
        'spawn_rate': 40,
        'score_multiplier': 1.0,
    },
    'hard': {
        'mouse_speed': 7,
        'spawn_rate': 30,
        'score_multiplier': 1.5,
    }
}

# Create classes for game objects
# Create Robot class
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers) # initalization method of Sprite class
        self.images = {
            'up': util.load_image('up.png', -1)[0],
            'down': util.load_image('down.png', -1)[0],
            'left': util.load_image('left.png', -1)[0],
            'right': util.load_image('right.png', -1)[0],
        }
        self.direction = 'up'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.topleft = 13, 367
        
    def update(self):
        pass
    
    def move(self, direction):
        if ((direction == 'right') and (self.rect.right < SCREENRECT.right - 40)): # If direction is right, robot not at right edge
            self.rect.move_ip(40, 0) # Move robot right by 40 pixels
            self.direction = 'right'
        elif (direction == 'left') and (self.rect.left > 40): # If direction is left, robot not at left edge
            self.rect.move_ip(-40, 0) # Move left by 40 pixels
            self.direction = 'left'
        elif ((direction == 'up') and (self.rect.top > 40)):
            self.rect.move_ip(0,-40)
            self.direction = 'up'
        elif ((direction == 'down') and (self.rect.bottom < SCREENRECT.bottom - 40)):
            self.rect.move_ip(0,40)
            self.direction = 'down'
        else:
            return
        
        self.image = self.images[self.direction]
            
    def getShotPosition(self):
        return self.rect.midtop

class SecondRobot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = {
            'up': util.load_image('up.png', -1)[0],
            'down': util.load_image('down.png', -1)[0],
            'left': util.load_image('left.png', -1)[0],
            'right': util.load_image('right.png', -1)[0],
        }
        self.direction = 'up'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.topleft = 13, 367
        
        self.prev_pos = pygame.mouse.get_pos()
        
    def update(self):
        # Move fist based on mouse position
        pos = pygame.mouse.get_pos()
        
        # Determine direction based on mouse movement delta
        dx = pos[0] - self.prev_pos[0]
        dy = pos[1] - self.prev_pos[1]
        
        if abs(dx) > abs(dy):
            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'
        else:
            if dy > 0:
                self.direction = 'down'
            elif dy < 0:
                self.direction = 'up'
                
        self.image = self.images[self.direction]
        self.rect.center = pos
        self.prev_pos = pos
        
    def getShotPosition(self):
        return self.rect.midtop
    
    
# Create Mouse object
class Mouse(pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = util.load_image('mouse.jpg', -1)
        self.facing = -1  # Start moving left
        self.rect.topright = SCREENRECT.right, 27  # Start at right edge
        self.speed = speed

    def update(self):
        # Move left or right
        self.rect.move_ip(self.facing * self.speed, 0)
        # Bounce at edges
        if self.rect.left <= 0 or self.rect.right >= SCREENRECT.right:
            self.facing *= -1
            self.rect.move_ip(0, 40)  # Move to next line (down 40 pixels)
        # Kill if off screen bottom
        if self.rect.top >= SCREENRECT.bottom:
            self.kill()


class Bullet(pygame.sprite.Sprite): # Player 1 attack controls
    speed = 20
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = util.load_image('shot.gif', -1)
        self.rect.center = pos
        
    def update(self):
        self.rect.move_ip(0, -self.speed)
        
        if self.rect.top <= SCREENRECT.top:
            self.kill()

class Explosion(pygame.sprite.Sprite): # Player 2 attack controls
    defaultlife = 12 # duration of explosion
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = util.load_image('explosion1.gif')
        self.life = self.defaultlife
        self.rect.center = pos
        
    def update(self):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()

# A function to create text
def drawText(scr, msg, position, colour, size):
    draw_font = pygame.font.Font(None, size)
    draw_color = Color(colour)
    draw_image = draw_font.render(msg, 0, draw_color)
    scr.blit(draw_image, position)

def settings_menu(screen, music_volume, sfx_volume):
    
    pygame.mixer.music.stop()
    play_background_music(bg_options, music_volume)
    
    selected = 0
    options = ['Music Volume', 'SFX Volume', 'Back']
    clock = pygame.time.Clock()
    
    while True:
        screen.fill(('white'))
        screen.blit(logo, logo_rect)
        drawText(screen, "Settings", (150, 120), 'white', 40)
        
        for i, option in enumerate(options):
            color = 'yellow' if i == selected else 'black'
            drawText(screen, option, (100, 180 + i * 40), color, 30)
            
        # Draw volume bars
        pygame.draw.rect(screen, (100, 100, 100), (250, 185, 100, 20))
        pygame.draw.rect(screen, (0, 255, 0), (250, 185, int(music_volume * 100), 20))

        pygame.draw.rect(screen, (100, 100, 100), (250, 225, 100, 20))
        pygame.draw.rect(screen, (0, 255, 0), (250, 225, int(sfx_volume * 100), 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or (selected == 2 and event.key in (K_RETURN, K_SPACE)):
                    pygame.mixer.music.stop()
                    play_background_music(bg_main, music_volume)
                    pygame.event.clear()
                    return music_volume, sfx_volume
                
                elif event.key == K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == K_LEFT:
                    if selected == 0:
                        music_volume = max(0, music_volume - 0.05)
                        pygame.mixer.music.set_volume(music_volume)
                    elif selected == 1:
                        sfx_volume = max(0, sfx_volume - 0.05)
                elif event.key == K_RIGHT:
                    if selected == 0:
                        music_volume = min(1, music_volume + 0.05)
                        pygame.mixer.music.set_volume(music_volume)
                    elif selected == 1:
                        sfx_volume = min(1, sfx_volume + 0.05)
        clock.tick(30)            


def title_screen(screen, music_volume=0.5, sfx_volume=0.5, game_start_sound=None):
    play_background_music(bg_main, music_volume)
    
    menu_fields = ['Mode', 'Difficulty','Settings','Story Mode','Quit']
    mode_options = ["1 Player", "2 Players"]
    difficulty_options = list(difficulty_settings.keys())
    
    selected_field = 0 # 0 = mode, 1 = difficulty
    selected_mode = 0
    selected_difficulty = 1 # defaults to medium
    clock = pygame.time.Clock()
    
    global logo, logo_rect
    logo = util.load_surface('logo.jpg')
    logo_rect = logo.get_rect()
    logo_rect.midtop = (screen.get_width() // 2,10)
    
    game_started = False
    start_pressed = False
    
    while True:
        screen.fill((255,255,255))
        screen.blit(logo, logo_rect)
        
        for i, option in enumerate(menu_fields):
            # Mode field
            pointer = ">" if selected_field == i else " "
            color = 'yellow' if selected_field == i else 'black'
            drawText(screen, f"{pointer} {option}:", (50, 120 + i * 40), color, 30)
            
            if option == 'Mode':
                drawText(screen, f"[{mode_options[selected_mode]}]", (200, 120 + i * 40), 'yellow' if selected_field == i else 'gray', 30)
            elif option == 'Difficulty':
                drawText(screen, f"[{difficulty_options[selected_difficulty]}]", (200, 120 + i * 40), 'yellow' if selected_field == i else 'gray', 30)    
        
        # Instructions
        drawText(screen, "SPACE = Start", (110, 300), 'black', 25)
        drawText(screen, "< > = Change  | Up or down = Navigate", (30, 330), 'gray', 20)
        drawText(screen, "ESC = Quit", (140, 360), 'gray', 20)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == K_UP:
                    selected_field = (selected_field - 1) % len(menu_fields)
                elif event.key == K_DOWN:
                    selected_field = (selected_field + 1) % len(menu_fields)
                elif event.key == K_LEFT:
                    if selected_field == 0: # Mode
                        selected_mode = (selected_mode - 1) % len(mode_options)
                    elif selected_field == 1: # Difficulty
                        selected_difficulty = (selected_difficulty - 1) % len(difficulty_options)
                elif event.key == K_RIGHT:
                    if selected_field == 0: # Mode
                        selected_mode = (selected_mode + 1) % len(mode_options)
                    elif selected_field == 1: # Difficulty
                        selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                elif event.key in (K_SPACE, K_RETURN):
                    if menu_fields[selected_field] == 'Settings':
                        music_volume, sfx_volume = settings_menu(screen, music_volume, sfx_volume)
                    elif menu_fields[selected_field] == 'Story Mode':
                        settings = {
                            'players': 1,
                            'difficulty': difficulty_options[selected_difficulty],
                            'music_volume': music_volume,
                            'sfx_volume': sfx_volume,
                        }
                        story_mode(screen, settings)
                        
                    elif menu_fields[selected_field] == 'Quit':
                        pygame.quit()
                        exit()
                    #else:
                        #if not start_pressed:
                            #if game_start_sound:
                                #game_start_sound.set_volume(sfx_volume)
                                #game_start_sound.play()
                                #pygame.time.wait(int(game_start_sound.get_length() * 1000))
                            #start_pressed = True   
                        #if start_pressed:
                            #pygame.mixer.music.stop()
                        #return {
                            #'players': selected_mode + 1,
                            #'difficulty': difficulty_options[selected_difficulty],
                            #'music_volume': music_volume,
                            #'sfx_volume': sfx_volume,
                        #}
                
        clock.tick(30)

def spawn_mouse_away_from_robot(robot_rect, mouse_speed, min_distance=80):
    attempts = 0
    while attempts < 10:
        x = random.randint(0, SCREENRECT.right - 40)
        y = random.randint(20, 80)
        dist = ((robot_rect.centerx - x)**2 + (robot_rect.centery - y)**2)**0.5
        if dist > min_distance:
            m = Mouse(mouse_speed)
            m.rect.topleft = (x,y)
            return m
        attempts += 1
    m = Mouse(mouse_speed)
    m.rect.topleft = (40, 20)
    return m

def main(screen, game_settings, shoot_sound, explode_sound, game_countdown_sound, bg_gameplay=None):
    music_volume = game_settings.get('music_volume', 0.5)
    sfx_volume = game_settings.get('sfx_volume', 0.5)
    
    pygame.mixer.music.set_volume(music_volume)
    shoot_sound.set_volume(sfx_volume)
    explode_sound.set_volume(sfx_volume)
    if game_countdown_sound:
        game_countdown_sound.set_volume(sfx_volume)
        
    if bg_gameplay is not None:
        pygame.mixer.music.stop()
        play_background_music(bg_gameplay, music_volume)
    
    #Create The Backgound Images
    bgImage = util.load_surface('map.png')
    
    # Gets game settings
    players = game_settings.get('players',1)
    difficulty_key = game_settings.get('difficulty', 'easy')
    difficulty = difficulty_settings[difficulty_key]
    score_multiplier = difficulty['score_multiplier']
    mouse_speed = difficulty['mouse_speed']
    spawn_rate = difficulty['spawn_rate']
    
    # Initialize Game Containers
    allsprites = pygame.sprite.Group()
    mice = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    explosion = pygame.sprite.Group()
    
    # Put game objects into containers
    Robot.containers = allsprites
    if players == 2:
        SecondRobot.containers = allsprites
    Explosion.containers = allsprites, explosion
    Mouse.containers = mice
    Bullet.containers = bullets
    
    
    # Create game objects
    myRobot = Robot()
    if players == 2:
        mySecondRobot = SecondRobot()
    Mouse()

    # clock to control framerate
    clock = pygame.time.Clock()
    
    SCORE = 0.0
    SCORE_player2 = 0.0
    gameOver = False
    death_handled = False
    lose_sound_playing = False
    
    countdown_time = 3 # seconds
    countdown_start_ticks = pygame.time.get_ticks()
    game_started = False
    countdown_playing = False
    
    # Game over menu
    game_over_menu_options = ["Retry", "Go Back"]
    selected_option = 0
    in_game_over_menu = False
    
    #Main Loop
    while True:
        elapsed_seconds =(pygame.time.get_ticks() - countdown_start_ticks) / 1000
        
        if not game_started and not countdown_playing and game_countdown_sound:
            game_countdown_sound.play(-1)
            countdown_playing = True
            
        if elapsed_seconds >= countdown_time and countdown_playing:
            game_countdown_sound.stop()
            countdown_playing = False
            game_started = True
            
    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
            
                if not gameOver:
                    if event.key == K_RIGHT:
                        myRobot.move('right')
                    elif event.key == K_LEFT:
                        myRobot.move('left')
                    elif event.key == K_UP:
                        myRobot.move('up')
                    elif event.key == K_DOWN:
                        myRobot.move('down')
                    elif event.key == K_SPACE:
                        Bullet(myRobot.getShotPosition())
                        shoot_sound.play()
                        
                elif in_game_over_menu:
                    if event.key in (K_UP, K_LEFT):
                        selected_option = (selected_option - 1) % len(game_over_menu_options)
                    elif event.key in (K_DOWN, K_RIGHT):
                        selected_option = (selected_option + 1) % len(game_over_menu_options)
                    elif event.key == K_SPACE or event.key == K_RETURN:
                        if game_over_menu_options[selected_option] == "Retry":
                            return "retry"
                        elif game_over_menu_options[selected_option] == "Go Back":
                            return "menu"
                        
            elif event.type == MOUSEBUTTONDOWN and players == 2:
                Explosion(mySecondRobot.getShotPosition())
        
        if not game_started:
            screen.blit(bgImage, (0,0))
            remaining = int(countdown_time - elapsed_seconds) + 1
            drawText(screen, str(remaining), (120, 180), 'black', 160)
            pygame.display.flip()
            if elapsed_seconds >= countdown_time:
                game_started = True
            clock.tick(40)
            continue
        
        if not gameOver:
            if random.randint(0, spawn_rate) == 0:
                spawn_mouse_away_from_robot(myRobot.rect, mouse_speed)
                
            # Handles game logic for collision
            hits = pygame.sprite.groupcollide(bullets, mice, True, True)
            for bullet, hit_mice in hits.items():
                for mouse in hit_mice:
                    Explosion(mouse.rect.center)
                    explode_sound.play()
            SCORE += len(hits) * score_multiplier
            if players == 2:
                SCORE_player2 += len(pygame.sprite.groupcollide(explosion, mice, False, True)) * score_multiplier
            
            if pygame.sprite.spritecollideany(myRobot, mice) or (players == 2 and pygame.sprite.spritecollideany(mySecondRobot, mice)):
                gameOver = True
                pygame.mixer.music.stop()
                
            if gameOver and not death_handled:
                handle_robot_death(screen, explode_sound, game_over_sound)
                death_handled = True
                in_game_over_menu = True
                
            if gameOver:
                if not lose_sound_playing:
                    if game_over_sound:
                        game_over_sound.play()
                    lose_sound_playing = True
            else:
                if lose_sound_playing:
                    if game_over_sound:
                        game_over_sound.stop()
                    lose_sound_playing = False
            
        # Updates all game objects
        allsprites.update()
        mice.update()  
        bullets.update()
        explosion.update()

        #Draw Everything
        screen.blit(bgImage, (0, 0))
        if gameOver:
            drawText(screen, "GAME OVER",(65,140),'red',60)
            drawText(screen, "Player 1: "+str(int((SCORE))), (120, 180), 'black', 40)
            if players == 2:
                drawText(screen, "Player 2: "+str(int((SCORE_player2))), (120,220), 'black', 40)
                
            for i, option in enumerate(game_over_menu_options):
                color = 'yellow' if i == selected_option else 'black'
                drawText(screen, option, (150, 270 + i*40), color, 35)
                
            pygame.display.flip()
            clock.tick(15)
            continue
        
        else:
            allsprites.draw(screen)
            mice.draw(screen)
            bullets.draw(screen)
            explosion.draw(screen)
            drawText(screen, "Player 1: "+str(int((SCORE))), (10, 385), 'black', 20)
            if players == 2:
                drawText(screen, "Player 2: "+str(int((SCORE_player2))), (310,385), 'black', 20)
        pygame.display.flip()

        #cap the framerate
        clock.tick(40)
    
def handle_robot_death(screen, explode_sound, game_over_sound):
    if explode_sound:
        explode_sound.play()
        
    pygame.display.flip()
    pygame.time.wait(2000)
        
def play_background_music(music_file, volume=0.5):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # loop forever    


def story_mode(screen, settings):
    music_volume = settings.get('music_volume', 0.5)
    sfx_volume = settings.get('sfx_volume', 0.5)
    players = settings.get('players', 1)
    difficulty = settings.get('difficulty', 'easy')    
    pygame.mixer.music.stop()
    play_background_music(bg_house, music_volume)
    
    # Story cutscenes
    screens = [
        "There once was a peaceful place\n called Rur_Ple,\nwhere robots helped\n children learn Python.",
        "Suddenly, \nbug mice invaded,\n threatening to ruin the code!",
        "It is up to you to save Rur_Ple!"
    ]
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    
    for screen_text in screens:
        waiting = True
        while waiting:
            screen.fill((0, 0, 0)) 
            lines = screen_text.split('\n')
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(screen.get_width()//2, 150 + i*40))
                screen.blit(text_surface, text_rect)
            
            drawText(screen, "Press any key to continue...", (80, 350), 'gray', 20)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    pygame.event.clear()
            clock.tick(30)
            
        if game_start_sound:
            game_start_sound.set_volume(sfx_volume)
            game_start_sound.play()
            pygame.time.wait(int(game_start_sound.get_length() * 1000))
                  

    # Now transition directly into gameplay
    pygame.mixer.music.stop()
    play_background_music(bg_gameplay, music_volume)
    
    pygame.event.clear()
    
    # Default game settings for story mode
    story_settings = settings
    while True:
        result = main(screen, settings, shoot_sound, explode_sound, game_countdown_sound, bg_gameplay)
        if result == 'menu':
            break

# Execution starts here
if __name__ == "__main__":
    pygame.init()
    shoot_sound = util.load_sound('shoot.wav')
    explode_sound = util.load_sound('explode.wav')
    game_start_sound = util.load_sound('game_start.wav')
    game_countdown_sound = util.load_sound('game_countdown.wav')
    game_over_sound = util.load_sound('lose.wav')
    bg_main = 'bg_main.mp3'
    bg_options = 'bg_options.mp3'
    bg_house = 'bg_house.mp3'
    bg_gameplay = 'bg_gameplay.mp3'
    screen = pygame.display.set_mode((405,405))
    pygame.display.set_caption('Mice Invasion')
    pygame.mouse.set_visible(0)
    
    settings = title_screen(screen, music_volume=0.5, sfx_volume=0.5, game_start_sound=game_start_sound)
    
    while True:
        start_pressed = False
        settings = title_screen(screen, music_volume=0.5, sfx_volume=0.5, game_start_sound=game_start_sound)
        show_story_screens(screen)
        while True:
            action = main(screen, settings, shoot_sound, explode_sound, game_countdown_sound, bg_gameplay=bg_gameplay)
            if action == 'menu':
                settings = title_screen(screen)
                break
            elif action == 'retry':
                pass