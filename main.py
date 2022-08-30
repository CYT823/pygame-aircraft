'''
References:
    [1] Pygame Docs, https://www.pygame.org/docs/
    [2] Pygame tutorial, https://youtu.be/61eX0bFAsYs
'''
from email.contentmanager import raw_data_manager
import pygame
import random
import os

# global parameters
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
        self.health = 100

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
        shoot_sound.play()

# create rock object
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(2, 5)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-5, 5)
    
    def rotate(self):
        self.total_degree = (self.total_degree + self.rotate_degree) % 360 
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
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

# create rock object
def create_rocks():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# score record
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_family, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surface.blit(text_surface, text_rect)

# health record
def draw_health(surface, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENTH
    outline_rect = pygame.Rect(x, y, BAR_LENTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

if __name__ == "__main__":
    # init game and build game window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pygame-aircraft")

    # create joy decvices objects
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    # clock object - setting the highest fps
    clock = pygame.time.Clock()

    # load images
    bg_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()
    player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
    bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
    rock_imgs = []
    for i in range(7):
        rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
    font_family = pygame.font.match_font("arial")

    # load sounds(shoot, explode, bgm)
    shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
    explode_sounds = []
    for i in range(2):
        explode_sounds.append(pygame.mixer.Sound(os.path.join("sound", f"expl{i}.wav")))
    pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1) # backgound music looping

    # create sprites (game object groups)
    all_sprites = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # create player and rock object
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        create_rocks()

    # parameters
    score = 0
    
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

        # update game
        all_sprites.update() # call every game object's update function
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # kill both rock object and bullet object if there is a collision happened
        for hit in hits:
            random.choice(explode_sounds).play()
            score += hit.radius
            create_rocks()
        damages = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
        for damage in damages:
            player.health -= damage.radius
            if player.health < 0:
                running = False
            create_rocks()
        
        # render
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH/2, 10)
        draw_health(screen, player.health, 10, 15)
        pygame.display.update()

    pygame.quit()