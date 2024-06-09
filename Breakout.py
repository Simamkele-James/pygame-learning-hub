#By Simamkele James
# March 2024 

import pygame
from sys import exit
from pygame.locals import *
from random import randint
from random import uniform

#Settings
WIDTH = 800
HEIGHT = 500

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 1

BRICK_WIDTH = 45
BRICK_HEIGHT = 20
TOTAL_BRICKS_NUMBER = 12
BRICKS_SPACE = 5 # space between bricks
BOARDER_X = 100 #how far away from the width board are the bricks

NUMBER_OF_BRICKS = 33
NUMBER_OF_LAYERS = 1

# ball size
BALL_SIZE = 10 #
BALL_SPEED =  0.4


#defin directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
x_tuple = (RIGHT,LEFT)
y_tuple = (UP,DOWN)

directionx = x_tuple[randint(0,1)]
directiony = y_tuple[randint(0,1)]

#   Define Colors
LIGHT_BLUE = (173 , 216 , 230)
DARK_GRAY  = (40  , 40  ,  40)

def main():
    global DISPLAYSURF, FPSCLOCK, FONT

    pygame.init()
    FONT = pygame.font.SysFont("arialblack",30)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("BREAKOUT")

    startGameScreen()
    while True:
        runGame()
        #showGameOverScreen()


# game functions

def runGame():
    """draws the paddle and runs the entire game"""
    global paddle_rect,bricks, brick_surface

    paddle_surf = pygame.Surface ((PADDLE_WIDTH,PADDLE_HEIGHT))
    paddle_surf.fill('red')
    paddle_rect = paddle_surf.get_rect( center = (int(WIDTH/2),HEIGHT) )

    brick_surface = pygame.Surface((BRICK_WIDTH,BRICK_HEIGHT))
    

    bricks = []
    layer_bricks = 12 #total number of brick in a specific layer
    offset = 0
    for i in range(NUMBER_OF_LAYERS):
        layer = []
        for j in range(layer_bricks):
            brick_surface.fill((randint(0,255),randint(0,255),randint(0,255)))
            layer.append(brick_surface.get_rect( topleft = (BOARDER_X+ 2*offset + j *(BRICK_WIDTH+BRICKS_SPACE),int(BRICK_HEIGHT*3)+ i*(BRICK_HEIGHT+10)-45) ))
            

        offset += 11.5
        
        bricks.append(layer)
        layer_bricks -= 1
    
    #BALL coordinates
    global x_pos, y_pos
    x_pos, y_pos = int(WIDTH/2),HEIGHT
    while True:
        DISPLAYSURF.fill("black")
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver()

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            paddle_rect.centerx -= PADDLE_SPEED
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            paddle_rect.centerx += PADDLE_SPEED

        if paddle_rect.right >= WIDTH:
            paddle_rect.right = WIDTH
        if paddle_rect.left <= 0:
            paddle_rect.left = 0

        DISPLAYSURF.blit(paddle_surf,paddle_rect)
        display_bricks()
        
        if run_ball(): # checks if game is done
            return
        pygame.display.update()


def display_bricks():
    """draws the bricks to the display surface"""
    global bricks

    layer_index = 1
    for layer in bricks:
        for rect in layer:
            DISPLAYSURF.blit(brick_surface,rect)



def run_ball():
    """UPDATES the position of the ball and its direction"""
    global x_pos, y_pos, directiony, directionx, ball_rect
    ball_rect = pygame.draw.circle(DISPLAYSURF,"pink",(x_pos,y_pos),BALL_SIZE)

    if brick_ball_collision():    #also checks if all bricks have been hit by the ball
        return True
            
    if directionx == LEFT:
        x_pos -= BALL_SPEED
        if x_pos <= 0:
            directionx = RIGHT
    
    elif directionx == RIGHT:
        x_pos += BALL_SPEED
        if x_pos >= WIDTH:
            directionx = LEFT
    
    if directiony == UP:
        y_pos -= BALL_SPEED + uniform(0.1,0.3)
        if y_pos <= 0:
            directiony = DOWN
    elif directiony == DOWN:
        y_pos += BALL_SPEED  + uniform(0.1, 0.3)
        if ball_rect.colliderect(paddle_rect):
            directiony = UP
        elif ball_rect.bottom >= HEIGHT:
            return True
    
def brick_ball_collision():
    """changes direction of ball once it collide with a brick depending on its sides"""
    global bricks, directionx,directiony, NUMBER_OF_LAYERS

    if bricks:
        for layer in bricks:
            if len(layer) == 0:
                bricks.remove(layer)
            for rect in layer:
                if rect.colliderect(ball_rect) and ball_rect.top <= rect.bottom and ball_rect.top >= rect.bottom - 5:
                    layer.remove(rect)
                    directiony = DOWN
                    continue
                
                if rect.colliderect(ball_rect) and ball_rect.right >= rect.left and ball_rect.right <= rect.left + 5:
                    layer.remove(rect)
                    directionx = LEFT
                    continue
                if rect.colliderect(ball_rect) and ball_rect.left <= rect.right and ball_rect.left >= rect.right -5:
                    layer.remove(rect)
                    directionx = RIGHT
                    continue
                
                if rect.colliderect(ball_rect) and ball_rect.bottom >= rect.top and ball_rect.bottom <= rect.top + 5:
                    layer.remove(rect)
                    directiony = UP
                    continue
    else:
        if NUMBER_OF_LAYERS == 10:
            gameOver()
            
        NUMBER_OF_LAYERS += 1
        return True
        



def showGameOverScreen():
    gameOver_text_surf = FONT.render("Game Over",True,"black")
    gameOver_rect = gameOver_text_surf.get_rect( center = (int(WIDTH/2),int(HEIGHT/2)))

    # command to start game text
    command_text_surf = FONT.render("Press any key to start",True,DARK_GRAY)
    command_text_rect = command_text_surf.get_rect( center = (WIDTH-100,HEIGHT - 100))

    while True:
        DISPLAYSURF.fill(LIGHT_BLUE)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameOver()
            
            if event.type == pygame.KEYDOWN:
                return
        DISPLAYSURF.blit(gameOver_text_surf,gameOver_rect)
        DISPLAYSURF.blit(command_text_surf,command_text_rect)

        pygame.display.update()

def gameOver():
    pygame.quit()
    exit()

def startGameScreen():

    #game title text
    title_surf = FONT.render("BREAKOUT",True,"black")
    title_rect = title_surf.get_rect( center = (int(WIDTH/2), 15))
    x,y = LEFT,DOWN # tracks direction of the title text 

    # command to start game text
    command_text_surf = FONT.render("Press any key to start",True,DARK_GRAY)
    command_text_rect = command_text_surf.get_rect( center = (WIDTH-100,HEIGHT - 100))

    while True:
        DISPLAYSURF.fill(LIGHT_BLUE)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return 
            
            if event.type == QUIT:
                gameOver()
        
        DISPLAYSURF.blit(command_text_surf,command_text_rect)
        DISPLAYSURF.blit(title_surf,title_rect)
        
        if x == LEFT:
            title_rect.left -= 5
        
        if x == RIGHT:
            title_rect.left += 5
        
        if y == UP:
            title_rect.top -= 5
        if y == DOWN:
            title_rect.top += 5

        if title_rect.left <=0:
            x = RIGHT
        if title_rect.right >= WIDTH:
            x = LEFT
        if title_rect.bottom >= HEIGHT:
            y = UP
        if title_rect.top <=0 :
            y = DOWN
    
        pygame.display.update()
        FPSCLOCK.tick(60)
        



   # FPSCLOCK.tick(30)
if __name__ == '__main__':
    main()

