'''
References:
    [1] Pygame Docs, https://www.pygame.org/docs/
    [2] Pygame tutorial, https://youtu.be/61eX0bFAsYs
'''
import pygame
import random

# parameters
running = True
WIDTH = 500
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# create player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

# create rock object
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)


# init game and build game window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pygame-aircraft")

# create joy decvices objects
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# clock object
clock = pygame.time.Clock()

# create sprites(game objects)
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)

# looping...
while running:
    # FPS setting
    clock.tick(FPS) # Program won't run more than 60 frames per second.
    
    # user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.JOYAXISMOTION:
            print(event)

    # upadte game
    all_sprites.update() # call every game object's update function

    # render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()

# pygame.sprite
# pygame module with basic game object classes