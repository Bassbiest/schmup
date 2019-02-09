# Shmup game
# pygame template - skeleton for a new pygame project
import pygame as pg
import random
import os

# Parameters for the game window
WIDTH = 480
HEIGHT = 600
FPS = 60

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (225, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# set up assets
game_folder = os.path.dirname(__file__) # directory of this very file
image_folder = os.path.join(game_folder, "Sprites")
sound_folder = os.path.join(game_folder, "Sounds")

# initialize pygame and create window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Shmup!")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob(Mobkind, spritegroups):
    m = Mobkind()
    for group in spritegroups:
        group.add(m)

def draw_shield_bar(surf, x, y, percantage):
    if percantage < 0:
        percantage = 0
    BAR_LENGHT = 60
    BAR_HEIGHT = 12
    fill = (percantage/100) * BAR_LENGHT
    outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill_rect = pg.Rect(x+1, y+1, fill-2, BAR_HEIGHT-2)
    pg.draw.rect(surf, WHITE, outline_rect)
    pg.draw.rect(surf, BLUE, fill_rect)

def draw_lives(surf, x, y, lives, image):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(image, img_rect)

def spawn_powerup(hit):
    if random.random() > 0.9:
        pow = Pow(hit.rect.center)
        all_sprites.add(pow)
        powerups_group.add(pow)
    else:
        pass

def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "SHMUP!", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Arrow keys to move, Space to fire", 22,
            WIDTH/2, HEIGHT/2)
    draw_text(screen, "Press Space to begin", 18, WIDTH/2, HEIGHT*3/4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS/2)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                waiting = False


# example Sprite class
class Sprite_01(pg.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # IMPORTANT, needs to be done with every sprite
        pg.sprite.Sprite.__init__(self)

        # .convert makes using the image faster
        self.image = pg.image.load(os.path.join(image_folder, "p1_stand.png")).convert()
        # make black in the sprite transparent
        self.image.set_colorkey(BLACK)
        # a usefull way of handling sprites is this rect method
        self.rect = self.image.get_rect()
        # puts the sprite in the middle of the screen using the center
        # of the rectangle to align it
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.y_speed = 5


        # an example square
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # self.rect = self.image.get_rect()
        # self.rect.center = (WIDTH/2, HEIGHT/2)


    # update function (name fixed) for moving around the screen
    def update(self):

        #example code to do stuff
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

class Player(pg.sprite.Sprite):
    # sprite for the Player
    def __init__(self):
        # IMPORTANT, needs to be done with every sprite
        pg.sprite.Sprite.__init__(self)

        # self.image = pg.Surface((50, 40))
        # self.image.fill(BLUE)
        self.image = pg.transform.scale(player_img, (56, 32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.pwrup_active = False
        self.pwrup_duration = pg.time.get_ticks()

    def update(self):
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.bottom = HEIGHT-10
        if self.pwrup_active and pg.time.get_ticks() - self.pwrup_duration > 3500:
            self.pwrup_duration = pg.time.get_ticks()
            self.pwrup_active = False
            self.shoot_delay = 250

        self.speedx = 0
        # checking if keys are pressed
        keystate = pg.key.get_pressed()
        # change speed if key are pressed
        if keystate[pg.K_LEFT]:
            self.speedx = -8
        if keystate[pg.K_RIGHT]:
            self.speedx = 8
        if keystate[pg.K_f]:
            self.shoot()
        self.rect.x += self.speedx
        # confining the sprite to the window boarders
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            shoot_sound.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)

# first enemy
class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        # use different images to prevent information loss, when rotating
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig
        # change size of rect
        self.rect = self.image.get_rect().inflate(-5, -5)
        # set circular hitbox
        self.radius = int(self.rect.width*0.95/2)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        # randomized spawn
        self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-150, -80)
        # randomized movement
        self.speedy = random.randrange(5, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-13, 13)
        self.last_update = pg.time.get_ticks()
        self.health = 30

    def update(self):
        self.rotate()
        # set new position
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # check if offscreen
        if self.rect.top > HEIGHT+10:
            # put them back at the top
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-100, -40)
            # ranomize their speed again
            self.speedy = random.randrange(2, 5)
        # confine mob to left and right boarders
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = self.speedx * -1

    def rotate(self):
            now = pg.time.get_ticks()
            if now - self.last_update > 50:
                self.last_update = now
                self.rot = (self.rot + self.rot_speed) % 360
                self.image = pg.transform.rotate(self.image_orig, self.rot)
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(laser_img, (5, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.damage = 10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves offscreen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(["shield", "weapon"])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves offscreen
        if self.rect.top > HEIGHT:
            self.kill()

# Load all game graphics
background = pg.image.load(os.path.join(image_folder, "space_background.png")).convert()
background_rect = background.get_rect()
player_img = pg.image.load(os.path.join(image_folder, "playerShip2_blue.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
#meteor_img = pg.image.load(os.path.join(image_folder, "meteorBrown_med1.png")).convert()
laser_img = pg.image.load(os.path.join(image_folder, "laserGreen11.png")).convert()
# define variaty of images for a certain sprite
meteor_images = []
meteor_list = ["meteorGrey_big1.png", "meteorGrey_big3.png", "meteorGrey_med1.png",
                "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
                "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pg.image.load(os.path.join(image_folder, img)).convert())
explosion_animation = {}
explosion_animation["large"] = []
explosion_animation["small"] = []
explosion_animation["player"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    image = pg.image.load(os.path.join(image_folder, filename)).convert()
    image.set_colorkey(BLACK)
    image_large = pg.transform.scale(image, (65, 65))
    explosion_animation["large"].append(image_large)
    image_small = pg.transform.scale(image, (32, 32))
    explosion_animation["small"].append(image_small)
    filename = "sonicExplosion0{}.png".format(i)
    img = pg.image.load(os.path.join(image_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_animation["player"].append(img)
powerup_images = {}
powerup_images["shield"] = pg.image.load(os.path.join(image_folder, "shield_gold.png")).convert()
powerup_images["weapon"] = pg.image.load(os.path.join(image_folder, "bolt_gold.png")).convert()



# load all game Sounds
shoot_sound = pg.mixer.Sound(os.path.join(sound_folder, "Laser_Shoot.wav"))
# for randomizing Sounds
Player_explosion = pg.mixer.Sound(os.path.join(sound_folder, "Player_explosion.wav"))
Player_explosion1 = pg.mixer.Sound(os.path.join(sound_folder, "rumble1.ogg"))
explosion_sounds = []
for sound in ["meteor_explosion1.wav", "meteor_explosion2.wav"]:
    explosion_sounds.append(pg.mixer.Sound(os.path.join(sound_folder, sound)))

pg.mixer.music.load(os.path.join(sound_folder, "main_theme.ogg"))
pg.mixer.music.set_volume(0.2)
pg.mixer.music.play(loops = -1)





# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        score = 0
        # creating a Group for sprites so Update does not get messy
        all_sprites = pg.sprite.Group()
        # creating a group for checking special rules they have in common
        mobs = pg.sprite.Group()
        # another group for bullets, again for special rules
        bullets = pg.sprite.Group()
        powerups_group = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # spawn several mobs
        for i in range(12):
            m = Mob()
            all_sprites.add(m) # for drawing
            mobs.add(m) # for rule checking
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        # check for closing the window
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()
            if event.key == pg.K_ESCAPE:
                running = False
    # Update
    all_sprites.update()

    # check if bullet hit mob
    hits = pg.sprite.groupcollide(mobs, bullets, False, True)
    for hit in hits:
        if hit.radius < 10:
            hit.kill()
            score += 50 - hit.radius
            random.choice(explosion_sounds).play()
            explosion = Explosion(hit.rect.center, "large")
            all_sprites.add(explosion)
            newmob(Mob, (all_sprites, mobs))
            spawn_powerup(hit)
        elif hit.radius > 8 and hit.radius < 20:
            if hit.health < 30:
                hit.kill()
                score += 50 - hit.radius
                random.choice(explosion_sounds).play()
                explosion = Explosion(hit.rect.center, "large")
                all_sprites.add(explosion)
                newmob(Mob, (all_sprites, mobs))
                spawn_powerup(hit)
            else:
                hit.health -= 15
        else:
            if hit.health == 10:
                hit.kill()
                score += 50 - hit.radius
                random.choice(explosion_sounds).play()
                explosion = Explosion(hit.rect.center, "large")
                all_sprites.add(explosion)
                newmob(Mob, (all_sprites, mobs))
                spawn_powerup(hit)
            else:
                hit.health -= 10

    # check to see if a mob hit the player
    hits = pg.sprite.spritecollide(player, mobs, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius
        explosion = Explosion(hit.rect.center, "small")
        all_sprites.add(explosion)
        newmob(Mob, (all_sprites, mobs))
        if player.shield <= 0:
            Player_explosion.play()
            death_explotion = Explosion(player.rect.center, "player")
            all_sprites.add(death_explotion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check if player hit powerup_images
    hits = pg.sprite.spritecollide(player, powerups_group, True)
    for hit in hits:
        if hit.type == "shield":
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "weapon":
            player.pwrup_active = True
            player.pwrup_duration = pg.time.get_ticks()
            player.shoot_delay = 150



    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explotion.alive():
        game_over = True

    # Draw / Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(score), 18, WIDTH/10, 10)
    draw_shield_bar(screen, WIDTH-70, 10, player.shield)
    draw_lives(screen, WIDTH/2-15*player.lives, 10, player.lives, player_mini_img)
    # after drawing everything, flip the display
    pg.display.flip()

pg.quit()

##################################
# CREDITS #
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
