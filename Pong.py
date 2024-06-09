import pygame
from pygame.locals import *
from sys import exit
import math, random

#Settings
WIN_WIDTH  = 1000
WIN_HEIGHT = 850

BALL_SPEED  = 5
BALL_SIZE = 10
BALL_X_DIR = "right"
BALL_Y_DIR = "up"

PADDLE_SPEED  = 15
PADDLE_HEIGHT = 100
PADDLE_WIDTH  = 5


LINE_WIDTH  = 5
LINE_HEIGHT = 25
TOTAL_LINES_TO_DISPLAY = int(WIN_HEIGHT/LINE_HEIGHT)

#SCORE_FONT = pygame.font.Font("fonts/Playground.ttf", 20)


#DIRECTIONS
UP    = "up"
DOWN  = "down"
LEFT  = "left"
RIGHT = "right"



def main():
    global DISPLAYSURF, paddle_surf, paddle_rect, player_y_pos,player_x_pos, ball_x_pos, ball_y_pos, opponent_paddle_rect, opponent_paddle_surf, SCORE_FONT, player_score_count, computer_score_count
    #set up window
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption("Pong")
    SCORE_FONT = pygame.font.Font("fonts/Playground.ttf", 100)

    #define initals
    player_x_pos = 100   # will be fixed
    player_y_pos = int(WIN_HEIGHT/2)

    player_score_count = 0
    computer_score_count = 0


    ball_x_pos = int(WIN_WIDTH/2)
    ball_y_pos = int(WIN_HEIGHT/2)

    #define objects
    paddle_surf = pygame.Surface((PADDLE_WIDTH,PADDLE_HEIGHT))
    paddle_surf.fill("white")
    paddle_rect = paddle_surf.get_rect(center = (player_x_pos, player_y_pos))

    opponent_paddle_surf = pygame.Surface((PADDLE_WIDTH,PADDLE_HEIGHT))
    opponent_paddle_surf.fill("white")
    opponent_paddle_rect = opponent_paddle_surf.get_rect( center = (WIN_WIDTH-100, int(WIN_HEIGHT/2)))


    #Game Loop
    while True:
        DISPLAYSURF.fill("black")
        run_game()

def run_game():
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    display_separator()
    handlePlayerInput()
    handleBallMovements()
    handleComputerOpponent()
    display_score()
    
    pygame.display.update()
    pygame.time.Clock().tick(120)

def display_separator():
    """displays the line separating players' regions"""
    line_pos = 0 #keep track of number of lines displayed

    line_surf = pygame.Surface((LINE_WIDTH, LINE_HEIGHT))
    line_surf.fill("white")
    line_rect = line_surf.get_rect( midtop = (WIN_WIDTH/2, line_pos))

    for i in range(TOTAL_LINES_TO_DISPLAY):
        DISPLAYSURF.blit(line_surf, line_rect)
        line_pos += 55
        line_rect.top =  line_pos

def handlePlayerInput():
    #display player's paddle
    global paddle_rect
    
    if pygame.key.get_pressed()[pygame.K_UP]:
        if paddle_rect.y <= 0:
            paddle_rect.y += PADDLE_SPEED
        paddle_rect.y -= PADDLE_SPEED
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if paddle_rect.bottom >= WIN_HEIGHT:
            paddle_rect.y -= PADDLE_SPEED
        paddle_rect.y += PADDLE_SPEED

    DISPLAYSURF.blit(paddle_surf, paddle_rect)

def handleComputerOpponent():
    global opponent_paddle_rect, opponent_paddle_surf

    if ball_y_pos > opponent_paddle_rect.centery:
        opponent_paddle_rect.centery += PADDLE_SPEED
    if ball_y_pos < opponent_paddle_rect.centery:
        opponent_paddle_rect.centery -= PADDLE_SPEED
    
    DISPLAYSURF.blit(opponent_paddle_surf, opponent_paddle_rect)

def handleBallMovements():
    global ball_y_pos, ball_x_pos, BALL_Y_DIR, BALL_X_DIR, paddle_rect, player_score_count, computer_score_count, BALL_SPEED

    #process ball direction
    if ball_x_pos >= WIN_WIDTH:
        BALL_X_DIR = RIGHT
        player_score_count += 1
    elif ball_x_pos <= 0:
        BALL_X_DIR = LEFT
        computer_score_count += 1

    if ball_y_pos >= WIN_HEIGHT:
        BALL_Y_DIR = DOWN
    elif ball_y_pos <= 0:
        BALL_Y_DIR = UP

    #process ball speed
    if BALL_X_DIR == LEFT:
        ball_x_pos += BALL_SPEED
    elif BALL_X_DIR == RIGHT:
        ball_x_pos -= BALL_SPEED
    
    if BALL_Y_DIR == UP:
        ball_y_pos += BALL_SPEED
    elif BALL_Y_DIR == DOWN:
        ball_y_pos -= BALL_SPEED


    #draw ball
    ball_rect = pygame.draw.circle(DISPLAYSURF, "pink", (ball_x_pos, ball_y_pos),BALL_SIZE)

    # check for  collision
    if paddle_rect.colliderect(ball_rect):
        if BALL_X_DIR == LEFT:
            BALL_X_DIR = RIGHT
        elif BALL_X_DIR == RIGHT:
            BALL_X_DIR = LEFT
    
        if BALL_Y_DIR == UP:
            BALL_Y_DIR = UP

        elif BALL_Y_DIR == DOWN:
            BALL_Y_DIR = DOWN

    if ball_rect.colliderect(opponent_paddle_rect):
        if BALL_X_DIR == LEFT:
            BALL_X_DIR = RIGHT
        elif BALL_X_DIR == RIGHT:
            BALL_X_DIR = LEFT
    
        if BALL_Y_DIR == UP:
            BALL_Y_DIR = UP

        elif BALL_Y_DIR == DOWN:
            BALL_Y_DIR = DOWN

    BALL_SPEED += 0.0001

    
            
def display_score():

    playerScore_surf = SCORE_FONT.render(str(player_score_count), True, "white")
    playerScore_rect = playerScore_surf.get_rect( center = (int(WIN_WIDTH/2 - 60), 50))

    computerScore_surf = SCORE_FONT.render(str(computer_score_count), True, "white")
    computerScore_rect = computerScore_surf.get_rect( center = (int(WIN_WIDTH/2 + 60), 50))

    DISPLAYSURF.blit(playerScore_surf, playerScore_rect)
    DISPLAYSURF.blit(computerScore_surf, computerScore_rect)


main()