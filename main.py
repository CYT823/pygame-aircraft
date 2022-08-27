'''
References:
    [1] Pygame Docs, https://www.pygame.org/docs/
    [2] Pygame tutorial, https://youtu.be/61eX0bFAsYs
'''
import pygame

# parameters
running = True

# init game and build game window
pygame.init()
pygame.display.set_mode((500, 600))

# create joy decvices objects
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# clock object
clock = pygame.time.Clock()

# looping...
while running:
    clock.tick(60) # Program will never run at more than 40 frames per second.
    # user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == "K_q":
        #         running = False
    # upadte game

    # render
    
pygame.quit()