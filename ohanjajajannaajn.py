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

# Background color
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

# Player ###############################################################################################################

# Avatar & position
rect_x = 64
rect_y = 8 * 1.618
avatar_x = (window_x / 2) - rect_x / 2
avatar_y = window_y - window_y / 10

# Avatar speed
avatar_speed = 8


def draw_rect(color, pos_x, pos_y, rect_w, rect_h):
    pygame.draw.rect(screen, color, pygame.Rect(pos_x, pos_y, rect_w, rect_h))
    return (color, pos_x, pos_y, rect_w, rect_h) # Returnerar så vi kan sedan se info om de skapade blocksen

# Ball #################################################################################################################
circle_r = 13
circle_x = (window_x / 2)
circle_y = avatar_y - circle_r


def draw_ball(ball_x, ball_y):
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), circle_r, 0)


# Blocks ###################################################################################

block_w = window_x // 10
block_h = window_y // 20

def build_level():
    """ Creates a level of blocks with random colors """
    start_x = 15
    start_y = 15

    lst = []

    for y in range(4): # LOOP KAN FÖRFINAS?
        for x in range(9):
            random_color = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA])

            lst.append(draw_rect(random_color, start_x, start_y, block_w, block_h))
            start_x += block_w + 5
        
        start_x = 15 # Nollställer
        start_y += block_h + 5 # SKA FLYTTA NED EFTER FULL RAD

    return lst

# Update Blocks:
def update_blocks(lst_of_blocks):
    """ Checks and updates changes about the blocks """
    for block in lst_of_blocks:
        draw_rect(block[0], block[1], block[2], block[3], block[4])
        # indx: 0 = RGB, 1 = x_pos, 2 = y_pos, 3 = block_w, 4 = block_h



# Game engine ##########################################################################################################

# FPS
FPS = 60


def main(pos_x, pos_y, ball_x, ball_y):
    clock = pygame.time.Clock()
    loop = True

    flux_x = True
    flux_y = True

    # Start pos of ball
    ball_x = window_x/2 
    ball_y = window_y/2

    current_block_state = build_level()
    #print(current_block_state)

    while loop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        # Check for collision to platform
        #Hur ska detta lösas? skapa en ny move funktion?
        # Specifika variabler för varje objekt
        # Som platform_speed och ball_speed
        # och platform_pos och ball_pos
        """if ball_y - circle_r / 2 - avatar_speed < avatar_y and flux_y:
            ball_y -= avatar_speed
        else:
            flux_y = False
            ball_y += avatar_speed
            if ball_y + circle_r / 2 + avatar_speed > window_y:
                flux_y = True  """      
           


        # Platform movement
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_LEFT] and pos_x - avatar_speed > 0:
            pos_x -= avatar_speed
        if user_input[pygame.K_RIGHT] and pos_x + avatar_speed + rect_x < window_x:  # elif
            pos_x += avatar_speed

        # Ball boarders & movement
        # x-movement
        if ball_x - circle_r / 2 - avatar_speed > 0 and flux_x:
            ball_x -= avatar_speed # Ha ballspeed och avatarspeed separat?
        else:
            flux_x = False
            ball_x += avatar_speed
            if ball_x + circle_r / 2 + avatar_speed > window_x:
                flux_x = True

        # y-movement
        
        if ball_y - circle_r / 2 - avatar_speed > 0 and flux_y:
            ball_y -= avatar_speed
        else:
            flux_y = False
            ball_y += avatar_speed
            if ball_y + circle_r / 2 + avatar_speed > window_y:
                flux_y = True
        
        # Output
        screen.fill(BLACK)
        update_blocks(current_block_state)
        # MÅSTE FYLLA IN DEN KORREKTA REPRESENTATIONEN AV BLOCKSEN
        
        draw_rect(WHITE, pos_x, pos_y, rect_x, rect_y) # Platform
        draw_ball(ball_x, ball_y) # Ball
        #draw_rect(RED, 10, 10, block_w, block_h) #blocks
        
        

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    
    main(avatar_x, avatar_y, circle_x, circle_y)

    

    # Skapa blocks
    # Ska det vara en Class eller lista?

    # Skapa en hit() funktion som lämnar true eller false om man
    # träffar en vägg eller plattform. (då samma kod används för bägge fall)
    #
    # Funktionerna change_y_pos() och change_x_pos()