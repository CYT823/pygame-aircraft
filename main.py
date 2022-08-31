'''
References:
    [1] Pygame Docs, https://www.pygame.org/docs/
    [2] Pygame tutorial, https://youtu.be/61eX0bFAsYs
'''
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
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun_level = 1
        self.gun_time = 0
        self.current_motion = 0

    def update(self):
        now = pygame.time.get_ticks()
        if self.gun_level > 1 and now - self.gun_time > 5000:
            self.gun_level -= 1
            self.gun_time = now

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT -10
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        elif key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0
        
        # This is for xbox controller
        self.rect.x += self.current_motion * self.speedx
        
    def shoot(self):
        if not(self.hidden):
            if self.gun_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun_level == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun_level >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.centerx, self.rect.centery)
                bullet3 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gun_upgrade(self):
        self.gun_level = self.gun_level + 1 if self.gun_level < 3 else 3
        self.gun_time = pygame.time.get_ticks()

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
        self.speedy = random.randrange(1, 8)
        self.total_degree = 0
        self.rotate_degree = random.randrange(-5, 5)
    
    def rotate(self):
        self.total_degree = (self.total_degree + self.rotate_degree) % 360 
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        # get origin center >> set new rect >> set center for new rect
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

# explosion object
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = explode_animation[self.size][0]
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explode_animation[self.size]):
                self.kill()
            else:
                self.image = explode_animation[self.size][self.frame]
                # get origin center >> set new rect >> set center for new rect
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

# super power gift
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(["shield", "gun"])
        self.image = superpower_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() # create rectangle for the surface
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()

# create rock object
def create_rocks():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# score record
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(font_family, size)
    text_surface = font.render(text, True, color)
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

# lives record
def draw_lives(surface, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 35 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# init frame which show how to play and press any key to start the game
def draw_init():
    screen.blit(bg_img, (0, 0))
    draw_text(screen, "Earth Defense", 64, WHITE, WIDTH/2, HEIGHT/4)
    draw_text(screen, "<ESC>  to  quit", 22, WHITE, WIDTH*4/5, HEIGHT/3+35)
    draw_text(screen, "Move: ← →", 22, BLACK, WIDTH/4, HEIGHT*6/8)
    draw_text(screen, "Shoot: SPACE", 22, BLACK, WIDTH*3/4, HEIGHT*6/8)
    draw_text(screen, "Press any key to start!", 22, BLACK, WIDTH/2, HEIGHT*7/8-20)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS) # Program won't run more than 60 frames per second.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:
                    return True
                else:
                    return False
            

if __name__ == "__main__":
    # parameters
    score = 0
    show_init = True

    # init game and build game window
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Earth Defense")
    
    # create joy decvices objects
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    # clock object - setting the highest fps
    clock = pygame.time.Clock()

    # load images
    bg_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()
    
    player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(BLACK)
    pygame.display.set_icon(player_mini_img)

    bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
    
    rock_imgs = []
    for i in range(7):
        rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())
    
    explode_animation = {}
    explode_animation["large"] = []
    explode_animation["small"] = []
    explode_animation["player"] = []
    for i in range(9):
        explode_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
        explode_img.set_colorkey(BLACK)
        explode_animation["large"].append(pygame.transform.scale(explode_img, (75, 75)))
        explode_animation["small"].append(pygame.transform.scale(explode_img, (30, 30)))
        
        player_explode_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
        player_explode_img.set_colorkey(BLACK)
        explode_animation["player"].append(player_explode_img)
    
    superpower_imgs = {}
    superpower_imgs["shield"] = pygame.image.load(os.path.join("img", "shield.png")).convert()
    superpower_imgs["gun"] = pygame.image.load(os.path.join("img", "gun.png")).convert()
    
    # setting font 
    font_family = os.path.join("GenJyuuGothicX-P-Heavy.ttf")
    
    # load sounds(shoot, explode, bgm)
    shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
    die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
    power_shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
    power_gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
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
    powers = pygame.sprite.Group()

    # create player and rock object
    player = Player()
    all_sprites.add(player)
    for i in range(10):
        create_rocks()

    # looping...
    while running:
        if show_init:
            isClosed = draw_init()
            if isClosed:
                break
            show_init = False
        
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
            elif event.type == pygame.JOYBUTTONDOWN:
                # A:0 B:1 X:2 Y:3 LB:4 RB:5 menu:7
                if event.button == 0 or event.button == 4 or event.button == 5:
                    player.shoot()
                elif event.button == 2:
                    running = False
            elif event.type == pygame.JOYAXISMOTION:
                # axis 0:horizontal, 1:vertical
                # current_motion 0:stop, 1:right, -1:left for xbox controller
                if event.axis == 0:
                    if (event.value * 10) > 0.8:
                        player.current_motion = 1
                    elif (event.value * 10) < -0.8:
                        player.current_motion = -1
                    else:
                        player.current_motion = 0

        # update game
        all_sprites.update() # call every game object's update function
        
        hits = pygame.sprite.groupcollide(rocks, bullets, True, True) # kill both rock object and bullet object if there is a collision happened
        for hit in hits:
            random.choice(explode_sounds).play()
            score += hit.radius
            explosion = Explosion(hit.rect.center, "large")
            all_sprites.add(explosion)
            if score < 2000:
                if random.random() > 0.6:
                    power = Power(hit.rect.center)
                    all_sprites.add(power)
                    powers.add(power)
            elif score < 4000:
                if random.random() > 0.8:
                    power = Power(hit.rect.center)
                    all_sprites.add(power)
                    powers.add(power)
            elif score < 5000:
                if random.random() > 0.9:
                    power = Power(hit.rect.center)
                    all_sprites.add(power)
                    powers.add(power)
            elif score < 8000:
                if random.random() > 0.95:
                    power = Power(hit.rect.center)
                    all_sprites.add(power)
                    powers.add(power)
            else:
                if random.random() > 0.98:
                    power = Power(hit.rect.center)
                    all_sprites.add(power)
                    powers.add(power)
                
            create_rocks()
        
        damages = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
        for damage in damages:
            player.health -= damage.radius
            if player.health < 0:
                death_explosion = Explosion(player.rect.center, "player")
                all_sprites.add(death_explosion)
                die_sound.play()
                player.lives -= 1
                player.health = 100
                player.hide()
            explosion = Explosion(damage.rect.center, "small")
            all_sprites.add(explosion)
            create_rocks()
        
        eats = pygame.sprite.spritecollide(player, powers, True)
        for eat in eats:
            if eat.type == "shield":
                player.health += 20
                if player.health > 100:
                    player.health = 100
                power_shield_sound.play()
            elif eat.type == "gun":
                player.gun_upgrade()
                power_gun_sound.play()

        if player.lives == 0 and not(death_explosion.alive()):
            show_init = True
            # init sprites
            all_sprites = pygame.sprite.Group()
            rocks = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            powers = pygame.sprite.Group()
            # init player and rock object
            player = Player()
            all_sprites.add(player)
            for i in range(10):
                create_rocks()
            # init parameters
            score = 0
        
        # render
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WHITE, WIDTH/2, 10)
        draw_health(screen, player.health, 5, 15)
        draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
        pygame.display.update()

    pygame.quit()