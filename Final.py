import pygame
import random
from rover import Rover, UpBullet, SideBullet
from worldgen import WorldGen, GenHole, Rock
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

def genRock(x, rocktype):
    rock = Rock(WORLD_SPEED, 1, GROUND_POS, x, rocktype)
    rock_list.add(rock)

#################
## SETUP STUFF
BLACK = (0, 0, 0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 340
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moon Pytrol")
done = False
clock = pygame.time.Clock()
## END SETUP STUFF
#################

all_sprites_list = pygame.sprite.Group()
hole_list = pygame.sprite.Group()
rock_list = pygame.sprite.Group()
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
time_since_rock_gen = 0

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
                if event.key == pygame.K_e:
                    genRock(500, 2)
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

    # --- GAME LOGIC --- #
    dt = clock.tick()

    # --- Collision Detection

    ## Player death by UFO
    player_bombed_hitlist = pygame.sprite.spritecollide(rover, bomb_list, False) # single object on group collision
    for bomb in player_bombed_hitlist:
        if rover.rect.y == GROUND_POS:
            rover.kill()
            rover.status = "dead"
        else:
            print("hit and a miss")

    ## Player death by hole
    player_holed_hitlist = pygame.sprite.spritecollide(rover, hole_list, False)
    for hole in player_holed_hitlist:
        rover.kill()
        rover.status = "dead"

    ## Player death by rock
    player_rocked_hitlist = pygame.sprite.spritecollide(rover, rock_list, False)
    for rock in player_rocked_hitlist:
        rover.kill()
        rover.status = "dead"
    

    ## UFO death by bullet
    for bullet in bullet_sprites_list:
        bullet_hit_list = pygame.sprite.spritecollide(bullet, ufo_sprites_list, False)
        for ufo_killed in bullet_hit_list:
            bullet.kill() # Remove bullet
            ufo_killed.kill() # Kill UFO
            ufo.status = "dead"
            ufos_killed += 1

    ## Rock death by bullet
    for sidebullet in side_bullet_sprites_list:
        side_bullet_hit_list = pygame.sprite.spritecollide(sidebullet, rock_list, False)
        for rock_killed in side_bullet_hit_list:
            sidebullet.kill() # Remove bullet
            rock_killed.kill() # Kill rock


    # --- World Generation Logic

    # (all of this is temporary until some sort of level system is put into place)

    ## Generating holes
    time_since_hole_gen += dt
    if time_since_hole_gen > random.randrange(50, 100):
        genHole(random.randrange(700, 720), random.randrange(0, 3))
        time_since_hole_gen = 0

    ## Spawning rocks
    time_since_rock_gen += dt
    if time_since_rock_gen > random.randrange(30, 41):
        genRock(random.randrange(650, 690), random.randrange(0, 4))
        time_since_rock_gen = 0


#    if pygame.time.get_ticks() % 1000 <= 500:
#        print("holes:", len(hole_list))


    # --- DRAWING CODE --- #
    screen.fill(BLACK)

    # --- World Generation
    world.drawBackground(screen)
    world.drawForeground(screen)
    world.drawGround(screen)

    hole_list.draw(screen)
    hole_list.update()

    rock_list.draw(screen)
    rock_list.update()

    # --- Drawing all sprites (few exceptions)
    all_sprites_list.draw(screen)

#    if rover.status == "dead":
#        pygame.draw.rect(screen, BLACK, [rover.rect.x, rover.rect.y, 100, 50])

    # --- Rover Control
    rover.blitWheels(screen)
    #rover.updateWheels()
    rover.calc_grav()
    rover.update(rover_speed)

    bullet_sprites_list.update()

    # --- UFO Control
    ufo.update()
    bomb_list.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()  # Close the window and quit.
