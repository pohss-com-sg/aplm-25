#Import Modules
import os, pygame
from pygame.locals import *
import util
import random
# Some constants defined
SCREENRECT = Rect(0, 0, 405, 405)


difficulty_settings = {
    'easy': {
        
    },
}

# Create classes for game objects
# Create Robot class
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers) # initalization method of Sprite class
        self.image, self.rect = util.load_image('up.png', -1)
        self.rect.topleft = 13, 367
        
    def update(self):
        pass
    
    def move(self, direction):
        if ((direction == 'right') and (self.rect.right < SCREENRECT.right - 40)): # If direction is right, robot not at right edge
            self.rect.move_ip(40, 0) # Move robot right by 40 pixels
        elif (direction == 'left') and (self.rect.left > 40): # If direction is left, robot not at left edge
            self.rect.move_ip(-40, 0) # Move left by 40 pixels
        elif ((direction == 'up') and (self.rect.top > 40)):
            self.rect.move_ip(0,-40)
        elif ((direction == 'down') and (self.rect.bottom < SCREENRECT.bottom - 40)):
            self.rect.move_ip(0,40)
            
    def getShotPosition(self):
        return self.rect.midtop
        
# Create Mouse object
class Mouse(pygame.sprite.Sprite):
    speed = 5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = util.load_image('mouse.jpg', -1)
        self.facing = -1  # Start moving left
        self.rect.topright = SCREENRECT.right, 27  # Start at right edge

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

class Bullet(pygame.sprite.Sprite):
    speed = 20
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = util.load_image('shot.gif', -1)
        self.rect.center = pos
        
    def update(self):
        self.rect.move_ip(0, -self.speed)
        
        if self.rect.top <= SCREENRECT.top:
            self.kill()

# A function to create text
def drawText(scr, msg, position, colour, size):
    draw_font = pygame.font.Font(None, size)
    draw_color = Color(colour)
    draw_image = draw_font.render(msg, 0, draw_color)
    scr.blit(draw_image, position)

def main():
    #Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((405, 405))

    pygame.display.set_caption('Mice Invasion')
    pygame.mouse.set_visible(0)

    #Create The Backgound Images
    bgImage = util.load_surface('map.png')
    
    # Initialize Game Containers
    allsprites = pygame.sprite.Group()
    mice = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    # Put game objects into containers
    Robot.containers = allsprites
    Mouse.containers = mice
    Bullet.containers = bullets
    
    # Create game objects
    myRobot = Robot()
    Mouse()

    # clock to control framerate
    clock = pygame.time.Clock()
    
    SCORE = 0
    gameOver = False
    
    #Main Loop
    while 1:
                    
    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                myRobot.move('right')
            elif event.type == KEYDOWN and event.key == K_LEFT:
                myRobot.move('left')
            elif event.type == KEYDOWN and event.key == K_UP:
                myRobot.move('up')
            elif event.type == KEYDOWN and event.key == K_DOWN:
                myRobot.move('down')
            elif event.type == KEYDOWN and event.key == K_SPACE:
                Bullet(myRobot.getShotPosition())
        
        # Adds more mouse
        if (random.randint(0, 40) == 0):
            Mouse()        
        
        # Handles game logic for collision
        SCORE += len(pygame.sprite.groupcollide(bullets, mice, True, True))
        
        if (len(pygame.sprite.groupcollide(allsprites, mice, False, True)) > 0):
            gameOver = True
            
        # Updates all game objects
        allsprites.update()
        mice.update()  
        bullets.update()

        #Draw Everything
        screen.blit(bgImage, (0, 0))
        if gameOver:
            drawText(screen, "GAME OVER",(65,140),'red',60)
            drawText(screen, "Player 1: "+str(SCORE), (120, 180), 'black', 40)
        else:
            allsprites.draw(screen)
            mice.draw(screen)
            bullets.draw(screen)
            drawText(screen, "Player 1: "+str(SCORE), (10, 385), 'black', 20)
        pygame.display.flip()
        

        #cap the framerate
        clock.tick(40)

# Execution starts here
main()