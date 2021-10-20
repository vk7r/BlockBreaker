import pygame


# SOUNDS
def sound_wall_bounce():
    soundObj = pygame.mixer.Sound('sounds\click.wav')
    soundObj.play()

def sound_kill_block():
    soundObj = pygame.mixer.Sound('sounds\pop.wav')
    soundObj.play()

def sound_game_over():
    soundObj = pygame.mixer.Sound('sounds\gameover.wav')
    soundObj.play()

def sound_you_win():
    soundObj = pygame.mixer.Sound('sounds\win.wav')
    soundObj.play()
