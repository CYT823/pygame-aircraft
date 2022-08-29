'''
References:
    [1] Pygame Docs, https://www.pygame.org/docs/
    [2] Pygame tutorial, https://youtu.be/61eX0bFAsYs
'''
import pygame
import random
import os

# parameters
running = True
WIDTH = 500
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# create player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.radius = 25
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
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# create rock object
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.radius = self.rect.width * 0.9 / 2
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 8)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(2, 10)

# create bullet object
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

def create_rocks():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

if __name__ == "__main__":
    # init game and build game window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pygame-aircraft")

    # create joy decvices objects
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    # clock object - setting the highest fps
    clock = pygame.time.Clock()

    # load img
    bg_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()
    player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
    rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
    bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()

    # create sprites (game objects)
    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    for i in range(8):
        create_rocks()

    # looping...
    while running:
        # FPS setting
        clock.tick(FPS) # Program won't run more than 60 frames per second.
        
        # user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # ESC to exit
                if event.key == pygame.K_ESCAPE:
                    running = False
                # SPACE to shoot
                if event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.JOYAXISMOTION:
                print(event)

        # upadte game
        all_sprites.update() # call every game object's update function
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # kill both rock object and bullet object if there is a collision happened
        for hit in hits:
            create_rocks()
        die = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle)
        if die:
            running = False
        
        # render
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        pygame.display.update()

    pygame.quit()