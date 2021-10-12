import pygame
import random


# Initialize pygame ####################################################################################################
pygame.init()

# GUI ##################################################################################################################

# Configure window
screen_x = pygame.display.Info().current_w
screen_y = pygame.display.Info().current_h
screen = pygame.display.set_mode((int(screen_x / 1.9), int(screen_y / 1.5)))
window_x, window_y = pygame.display.get_window_size()

# Background
#bg = pygame.image.load("BlockBreaker\\test_bg.png")


# colors
BLACK = (0, 0, 0)
WHITE = (225, 225, 225)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Caption
pygame.display.set_caption("Blockbreaker")

# Icon
icon = pygame.image.load("BlockBreaker\\blockbreaker_test_icon.png")
pygame.display.set_icon(icon)

# Rectangle #######################################################################################
def draw_rect(color, pos_x, pos_y, rect_w, rect_h):
    pygame.draw.rect(screen, color, pygame.Rect(pos_x, pos_y, rect_w, rect_h))
    return (color, pos_x, pos_y, rect_w, rect_h) # Returnerar så vi kan sedan se info om de skapade blocksen

# Ball #################################################################################################################

def draw_ball(x_pos, y_pos, radius):
    pygame.draw.circle(screen, WHITE, (x_pos, y_pos), radius, 0)

# Blocks ###################################################################################

def build_level():
    """ Creates a level of blocks with random colors """
    start_x = 15
    start_y = 15

    blockk_w = window_x // 10
    blockk_h = window_y // 20

    lst = []

    for y in range(4): # LOOP KAN FÖRFINAS?
        for x in range(9):
            random_color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA])

            lst.append(draw_rect(random_color, start_x, start_y, blockk_w, blockk_h))
            start_x += blockk_w + 5
        
        start_x = 15 # Nollställer
        start_y += blockk_h + 5 # SKA FLYTTA NED EFTER FULL RAD

    return lst

# Update Blocks:
def update_blocks(lst_of_blocks, removed_blocks):
    """ Checks and updates changes about the blocks """

    #DELETES BROKEN BLOCKS
    for tpl in removed_blocks: # SER UT ATT TA BORT OÖNSKADE BLOCKS
        for block_info in lst_of_blocks:
            if tpl[0] in block_info and tpl[1] in block_info:
                lst_of_blocks.remove(block_info) # removes block


    for block in lst_of_blocks:
        draw_rect(block[0], block[1], block[2], block[3], block[4])
        # indx: 0 = RGB, 1 = x_pos, 2 = y_pos, 3 = block_w, 4 = block_h

def block_pos_list(lst):
    """ Creates a list containing tuples of x and y coordinates
     for each respective block. (x, y) """

    pos_lst = []

    for element in lst:
        pos_tpl = (element[1], element[2])
        pos_lst.append(pos_tpl)
    return pos_lst

# Game engine ##########################################################################################################

# FPS
FPS = 60

# TEXT
myfont = pygame.font.SysFont('Comic Sans MS', 50)
game_over_txt = myfont.render('GAME OVER', True, WHITE)



# WALLS
left_wall = 0
right_wall = window_x

top_wall = 0
bot_wall = window_y

# Platform/player
platform_w = 64
platform_h = 8 * 1.618
platform_start_posx = ((window_x / 2) - (platform_w / 2))
platform_start_posy = window_y - window_y / 10

# Ball
ball_start_posx = (window_x / 2)
ball_start_posy = (window_y / 2)

# BLOCKS
block_w = window_x // 10
block_h = window_y // 20


def main(platform_x_pos, ball_xpos, ball_ypos):
    clock = pygame.time.Clock()
    loop = True

    platform_speed = 8

    ball_r = 12
    ball_speed = 8

    current_block_state = build_level() # Start layout
    blocks_positions = block_pos_list(current_block_state) # pos-lista för alla blocks
    removed_blocks_lst = [] # lista med "förstörda" blocks
    #print(current_block_state)
    #print(blocks_positions)

    GO_RIGHT = True # standardvärde för att bollen åker till höger
    GO_UP = True # standardvärde för att bollen åker uppåt

    while loop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Platform movement
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_LEFT] and platform_x_pos - platform_speed > 0:
            platform_x_pos -= platform_speed
        if user_input[pygame.K_RIGHT] and platform_x_pos + platform_speed + platform_w < window_x:
            platform_x_pos += platform_speed

        #BALL COLLISION:
        # wallbounce x-axis 
        ball_left_side = (ball_xpos - ball_r) # + ball_speed ?
        ball_right_side = (ball_xpos + ball_r)

        if ball_left_side < left_wall: # LEFT
            ball_xpos += ball_speed
            GO_RIGHT = True
        elif ball_right_side > right_wall: # RIGHT
            ball_xpos -= ball_speed
            GO_RIGHT = False
        else:
            if GO_RIGHT:
                ball_xpos += ball_speed
            else:
                ball_xpos -= ball_speed


        # Wallbounce y-axis
        ball_top_side = ( ball_ypos - ball_r)
        ball_bot_side = ( ball_ypos + ball_r)

        if ball_top_side < top_wall: # TOP WALL
            ball_ypos += ball_speed
            GO_UP = False
        # COLLISION WITH PLATFORM
        if  (platform_x_pos - platform_w) <= ball_xpos <= (platform_x_pos + platform_w) and (platform_start_posy) <= ball_bot_side <= (platform_start_posy + platform_h):
            ball_ypos -= ball_speed
            GO_UP = True
        else:
            if GO_UP:
                ball_ypos -= ball_speed
            else:
                ball_ypos += ball_speed


        # COLLISION WITH BLOCKS
        for tpl in blocks_positions:
            if (tpl[0] - block_w) <= ball_xpos <= (tpl[0] + block_w) and tpl[1] <= ball_ypos <= (tpl[1] + block_h):
                blocks_positions.remove(tpl)
                removed_blocks_lst.append(tpl)
                #print(f"BYE BYE {tpl}")


        GAME_OVER = False
        # IF BALL LOST
        if ball_ypos > bot_wall:
            GAME_OVER = True
            ball_speed = 0

        # new frame update
        screen.fill(BLACK)
        #screen.blit(bg, [0, 0])
        update_blocks(current_block_state, removed_blocks_lst)
        draw_rect(WHITE, platform_x_pos, platform_start_posy, platform_w, platform_h) # Platform
        draw_ball(ball_xpos, ball_ypos, ball_r) # Ball

        if GAME_OVER:
            screen.blit(game_over_txt,(window_x//3.5, window_y//2))
        
        
        

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    
    main(platform_start_posx, ball_start_posx, ball_start_posy)
    