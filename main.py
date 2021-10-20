import pygame
import random
from sound_effects import *

# Initialize pygame
pygame.init()

# Configure window
screen_x = pygame.display.Info().current_w
screen_y = pygame.display.Info().current_h
screen = pygame.display.set_mode((int(screen_x / 1.9), int(screen_y / 1.5)))
window_x, window_y = pygame.display.get_window_size()

# Background
#bg = pygame.image.load("BlockBreaker\\test_bg.png")

# Caption
pygame.display.set_caption("BlockBreaker")

# Icon
icon = pygame.image.load("blockbreaker_test_icon.png")
pygame.display.set_icon(icon)

# colors
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# GLOBAL CONSTANTS --------------------------------------------------

# Tickrate
FPS = 60

# Fonts
BigFont = pygame.font.SysFont('rog fonts', window_x//10)
SmallFont = pygame.font.SysFont('consolas', window_x//20)

# Texts
game_over_txt = BigFont.render('GAME OVER', True, WHITE)
you_win_txt = BigFont.render("YOU WIN!", True, WHITE)
restart_txt = SmallFont.render('Press "r" to restart', True, WHITE)

# BLOCKS
block_w = (window_x - 40 - 30) // 10 # window_x minus luckor mellan blocks ( -(5*8) & -(15+15) )
block_h = window_y // 20

# WALLS
left_wall = 0
right_wall = window_x
top_wall = 0
bot_wall = window_y

# Platform/Player
platform_w = window_x // 8
platform_h = (window_x // 10) // 10 
platform_start_posx = ((window_x / 2) - (platform_w / 2))
platform_start_posy = window_y - window_y / 10

platform_speed = (window_x//90)

# Ball
ball_r = window_x // 65


# FUNCTIONS --------------------------------------------------

# DRAW BALL
def draw_ball(x_pos, y_pos, radius):
    pygame.draw.circle(screen, WHITE, (x_pos, y_pos), radius, 0)

# BUILD LEVEL
def build_level():
    """ Creates a level of blocks with random colors, returns list of blocks """
    start_x = 15
    start_y = 15

    lst = []

    c = 255
    for y in range(4):
        for x in range(10):
            # random_color = random.choice([ (255, c, 80), (255, 100, c), (c, 255, 80)] )
            # random_color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA])
            lst.append( ((255, c, 100 ), start_x, start_y, block_w, block_h) )
            start_x += block_w + 5
        
        start_x = 15 # Nollställer
        start_y += block_h + 5 # FLYTTA NED EFTER FULL RAD
        c -= 75 # FÅR EJ ÖVERSTIGA 85 då RBG-värdet blir < 0

    return lst

# BLOCK UPDATES
def update_blocks(lst_of_blocks, removed_blocks):
    """ Looks for removed blocks and updates the change """

    #DELETES BROKEN BLOCKS
    for tpl in removed_blocks:
        for block_info in lst_of_blocks:
            if tpl[0] == block_info[1] and tpl[1] == block_info[2]:
                lst_of_blocks.remove(block_info) # removes block

def draw_living_blocks(lst_of_blocks):
    """ Draws the remaining blocks """
    for block in lst_of_blocks:
        pygame.draw.rect(screen, block[0], pygame.Rect(block[1], block[2], block[3], block[4]))
        # indx: 0 = RGB, 1 = x_pos, 2 = y_pos, 3 = block_w, 4 = block_h

def block_pos_list(block_lst):
    """ Creates a list containing tuples of x and y coordinates
     for each respective block. (x, y) """

    pos_lst = []

    for element in block_lst:
        pos_tpl = (element[1], element[2])
        pos_lst.append(pos_tpl)
    return pos_lst

# COLLISION
def touching_block(x_pos, y_pos, ball_x, ball_y):
    return (x_pos) <= ball_x <= (x_pos + block_w) and y_pos <= ball_y <= (y_pos + block_h)

def touching_platform(plat_x_pos, ball_x, ball_y_bottom):
    return (plat_x_pos) <= ball_x <= (plat_x_pos + platform_w) and (platform_start_posy) <= ball_y_bottom <= (platform_start_posy + platform_h)

# DIRECTION OF BALL
def RIGHT(): # 
    return 1
def LEFT():
    return -1
def UP():
    return -1
def DOWN():
    return 1


# MAIN FUNCTION --------------------------------------------------

def main():
    clock = pygame.time.Clock()
    loop = True

    # LEVEL CONSTRUCTION
    current_block_state = build_level() # Start layout
    blocks_positions = block_pos_list(current_block_state) # pos-lista för alla blocks
    removed_blocks_lst = [] # lista med "förstörda" blocks
    
    # VARS:
    # BALL SPEED
    ball_speed = (window_x//110) # hur många pixlar som adderas varje iteration

    # Platform Position
    platform_x_pos = platform_start_posx
    
    # Ball Position
    random_spawn = random.randint(left_wall, right_wall)
    ball_xpos = (random_spawn)
    ball_ypos = (window_y // 2)

    # Ball Direction
    X_DIRECTION = random.choice([LEFT(), RIGHT()]) # slumpat startvärde för vilket håll bollen åker
    Y_DIRECTION = UP()

    # BOOL for soundeffect
    PLAY = True # så ljudet bara spelas en gång

    # GAME LOOP
    while loop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Platform movement
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_LEFT] and platform_x_pos > 0:
            platform_x_pos -= platform_speed
        if user_input[pygame.K_RIGHT] and platform_x_pos + platform_w < window_x:
            platform_x_pos += platform_speed

        #BALL COLLISION:
        ball_left_side = (ball_xpos - ball_r)
        ball_right_side = (ball_xpos + ball_r)

        ball_top_side = ( ball_ypos - ball_r)
        ball_bot_side = ( ball_ypos + ball_r)

        # BALL MOVEMENT
        if ball_left_side <= left_wall: # Studs vänster vägg
            X_DIRECTION = RIGHT()
            ball_xpos += ball_speed
        elif ball_right_side >= right_wall: # Studs höger vägg
            X_DIRECTION = LEFT()
            ball_xpos -= ball_speed
        elif ball_top_side <= top_wall: # Studs tak
            Y_DIRECTION = DOWN()
            ball_ypos += ball_speed
        else:
            ball_xpos += (X_DIRECTION * ball_speed)
            ball_ypos += (Y_DIRECTION * ball_speed)

        # COLLISION WITH PLATFORM
        if touching_platform(platform_x_pos, ball_xpos, ball_bot_side): 
            Y_DIRECTION = UP()
            ball_ypos += (Y_DIRECTION * ball_speed)


        # COLLISION WITH BLOCKS
        for tpl in blocks_positions:
            if touching_block(tpl[0],tpl[1],ball_xpos, ball_ypos):
                sound_kill_block()
                Y_DIRECTION = DOWN()
                ball_ypos += (Y_DIRECTION * ball_speed)
                blocks_positions.remove(tpl)
                removed_blocks_lst.append(tpl)
                update_blocks(current_block_state, removed_blocks_lst)


        # UPDATE SCREEN
        screen.fill(BLACK)
        #screen.blit(bg, [0, 0])
        draw_living_blocks(current_block_state)
        pygame.draw.rect(screen, WHITE, pygame.Rect(platform_x_pos, platform_start_posy, platform_w, platform_h))
        draw_ball(ball_xpos, ball_ypos, ball_r) # Ball
        
        # IF LOSE (If ball lost)
        if ball_ypos > bot_wall:
            if PLAY:
                sound_game_over()
                PLAY = False
                
            ball_speed = 0
            screen.blit(game_over_txt,((window_x // 2) - (game_over_txt.get_width()//2), (window_y//2) - (game_over_txt.get_height()//2) ))
            screen.blit(restart_txt,((window_x // 2) - (restart_txt.get_width()//2), window_y//1.5))
            if user_input[pygame.K_r]:
                return True

        # IF WIN (If all blocks are destroyed)
        if len(current_block_state) == 0:
            if PLAY:
                sound_you_win()
                PLAY = False

            ball_speed = 0
            screen.blit(you_win_txt,((window_x // 2) - (you_win_txt.get_width()//2), (window_y//2) - ((you_win_txt.get_height()//2)) ))
            screen.blit(restart_txt,((window_x // 2) - (restart_txt.get_width()//2), window_y//1.5))
            if user_input[pygame.K_r]:
                return True


        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':

    while main():
        main()
    