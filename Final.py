import pygame
import random
from rover import Rover, UpBullet, SideBullet
from worldgen import WorldGen, GenHole
from ufo import UFO, Bomb

pygame.init()  # vroom vroom pyamegame

#################
## VARS

GROUND_POS = 285 # (to be passed into sprites)

rover_speed = 0.5
rover_starting_x = 120

ROVER_GRAVITY = 0.16

UFO_SPEED = 1

WORLD_SPEED = 0.8 # (speed of scrolling)

## END VARS
#################

def shoot():
    if len(side_bullet_sprites_list) == 0:
        new_bullet = UpBullet(rover) # make new bullet sprite
        new_side_bullet = SideBullet(rover)
        all_sprites_list.add(new_bullet) # adding it to the container to be drawn
        all_sprites_list.add(new_side_bullet)
        bullet_sprites_list.add(new_bullet)
        bullet_sprites_list.add(new_side_bullet)
        side_bullet_sprites_list.add(new_side_bullet)
    elif len(side_bullet_sprites_list) >= 1:
        new_bullet = UpBullet(rover)
        all_sprites_list.add(new_bullet)
        bullet_sprites_list.add(new_bullet)

def genHole(x, holetype):
    hole = GenHole(WORLD_SPEED, -10, GROUND_POS, x, holetype)
    #all_sprites_list.add(hole)
    hole_list.add(hole)

#################
## SETUP STUFF
BLACK = (0, 0, 0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 340
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moon Patrol")
done = False
clock = pygame.time.Clock()
## END SETUP STUFF
#################

all_sprites_list = pygame.sprite.Group()
hole_list = pygame.sprite.Group()
ufo_sprites_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()
bullet_sprites_list = pygame.sprite.Group()
side_bullet_sprites_list = pygame.sprite.Group()

rover = Rover(ROVER_GRAVITY, GROUND_POS)
rover.rect.x = rover_starting_x
rover.rect.y = 50

all_sprites_list.add(rover)

ufo = UFO(UFO_SPEED, GROUND_POS, all_sprites_list, bomb_list)
ufo.rect.x = 70
ufo.rect.y = 59

ufo_sprites_list.add(ufo)
all_sprites_list.add(ufo)

world = WorldGen(WORLD_SPEED, 30, GROUND_POS - 30)

ufos_killed = 0
time_since_hole_gen = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rover.jump()
                if event.key == pygame.K_q:
                    ufo.dropBomb(all_sprites_list, bomb_list)
                if event.key == pygame.K_w:
                    if rover.status == "alive": shoot()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("press")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and rover.rect.x <= 230:
        rover_speed = 1.8
        if rover.rect.x >= 228:
            rover.rect.x = 228
    elif keys[pygame.K_LEFT]:
        rover_speed = -0.4
        if rover.rect.x <= 70:
            rover.rect.x = 70
    elif pygame.K_LEFT not in keys or pygame.K_RIGHT not in keys:
        rover_speed = 0.5
        if rover.rect.x > rover_starting_x: rover.rect.x -= 1.3
        if rover.rect.x < rover_starting_x and rover.rect.y <= 286: rover.rect.x += 1.3

    # --- Game logic
    dt = clock.tick()

    ## Player death by UFO
    player_bombed_hitlist = pygame.sprite.spritecollide(rover, bomb_list, False) # single object on group collision
    for bomb in player_bombed_hitlist:
        if rover.rect.y <= GROUND_POS:
            rover.kill()
            rover.status = "dead"
        else:
            print("hit and a miss")

    ## Player death by hole
    player_holed_hitlist = pygame.sprite.spritecollide(rover, hole_list, False)
    for hole in player_holed_hitlist:
        rover.kill()
        rover.status = "dead"


    ## UFO death by bullet
    for bullet in bullet_sprites_list:
        hit_list = pygame.sprite.spritecollide(bullet, ufo_sprites_list, False) # If bullet collides with UFO, kill UFO
        for i in hit_list:
            bullet.kill()
            ufo.kill()
            ufo.status = "dead"
            ufos_killed += 1


    ## Generating holes
    time_since_hole_gen += dt
    if time_since_hole_gen > random.randrange(9, 25):
        genHole(random.randrange(680, 720), 0) # move the snake here
        time_since_hole_gen = 0


#    if pygame.time.get_ticks() % 1000 <= 500:
#        print("holes:", len(hole_list))


    # --- Drawing code
    screen.fill(BLACK)

    ## WORLD GENERATION
    world.drawBackground(screen)
    world.drawForeground(screen)
    world.drawGround(screen)

    hole_list.update()
    hole_list.draw(screen)
    # DRAW
    all_sprites_list.draw(screen)

    ## ROVER CONTROL
    rover.blitWheels(screen)
    #rover.updateWheels()
    rover.calc_grav()
    rover.update(rover_speed)

    bullet_sprites_list.update()

    ## UFO CONTROL
    ufo.update()
    bomb_list.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()  # Close the window and quit.
