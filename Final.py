import pygame
import random
import time
from rover import Rover, UpBullet, SideBullet, Explosion
from worldgen import WorldGen, GenHole, Rock
from ufo import UFO, Bomb
#pygame.mixer.pre_init(44100, -16, 1, 512)
#pygame.mixer.init()
pygame.init()  # vroom vroom pyamegame

#################
## VARS

GROUND_POS = 285 # (to be passed into sprites)

rover_speed = 0.5
rover_starting_x = 130

ROVER_GRAVITY = 0.16

UFO_SPEED = 1

WORLD_SPEED = 0.8 # (speed of scrolling)

## END VARS
#################

def intro_screen():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                done = True
        screen.fill(BLACK)

        pygame.display.flip()
        clock.tick(60)

def outro_screen():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    intro_screen() # restart game i guess here

        screen.fill(BLUE)

        pygame.display.flip()
        clock.tick(60)

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

def genUFO(speed, x):
    ufo = UFO(speed, GROUND_POS, all_sprites_list, bomb_list)
    ufo.rect.x = x
    ufo.rect.y = random.randrange(30, 59)
    all_sprites_list.add(ufo)
    ufo_sprites_list.add(ufo)

def oneInThree():
    if random.randrange(0, 3) == 1:
        return(1)
    else:
        return(0)

#################
## SETUP STUFF
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 340
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Moon Pytrol")
done = False
clock = pygame.time.Clock()

bg_music = pygame.mixer.Sound("assets/sounds/theme_bigger.wav")
start_music = pygame.mixer.Sound("assets/sounds/start-course.wav")
crash_sfx = pygame.mixer.Sound("assets/sounds/crash.wav")
game_over_music = pygame.mixer.Sound("assets/sounds/game_over.wav")
ufo_died_sfx = pygame.mixer.Sound("assets/sounds/shoot.wav")
shoot_sfx = pygame.mixer.Sound("assets/sounds/shoot.wav")

font = pygame.font.Font("assets/pixel_font.ttf", 20)
font_big = pygame.font.Font("assets/pixel_font.ttf", 50)
## END SETUP STUFF
#################

## Sprite containers
all_sprites_list = pygame.sprite.Group()
hole_list = pygame.sprite.Group()
rock_list = pygame.sprite.Group()
ufo_sprites_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()
bullet_sprites_list = pygame.sprite.Group()
side_bullet_sprites_list = pygame.sprite.Group()

explo_list = pygame.sprite.Group()

## Making rover
rover = Rover(ROVER_GRAVITY, GROUND_POS)
rover.rect.x = rover_starting_x
rover.rect.y = 50
all_sprites_list.add(rover)

'''
ufo.rect.x = 70
ufo.rect.y = 59

ufo_sprites_list.add(ufo)
all_sprites_list.add(ufo)
'''

world = WorldGen(WORLD_SPEED, 30, GROUND_POS - 30)

## Misc tracking variables
ufos_killed = 0
level = 4
time_since_hole_gen = 0
time_since_rock_gen = 0
time_since_ufo_gen = 0

in_outro = False
dead_sequence_played_yet = False
intro_screen()


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rover.jump()
                if event.key == pygame.K_w:
                    if rover.status == "alive":
                        shoot()
                        shoot_sfx.play(0)
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
        if rover.rect.bottom + 7 >= GROUND_POS:
            rover.kill()
            rover.status = "dead"

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
        bullet_ufo_hit_list = pygame.sprite.spritecollide(bullet, ufo_sprites_list, False)
        for ufo_killed in bullet_ufo_hit_list:
            bullet.kill() # Remove 3bullet
            ufo_killed.death()
            ufo_killed.kill() # Kill UFO
            ufo_died_sfx.play(0)
            #ufo.status = "dead"
            ufos_killed += 1

    ## Bomb death by bullets
    for bullet in bullet_sprites_list:
        bullet_bomb_hit_list = pygame.sprite.spritecollide(bullet, bomb_list, False)
        for bomb_killed in bullet_bomb_hit_list:
            bomb_killed.kill()

    for sidebullet in side_bullet_sprites_list:
        sidebullet_bomb_hit_list = pygame.sprite.spritecollide(sidebullet, bomb_list, False)
        for bomb_killed in sidebullet_bomb_hit_list:
            bomb_killed.kill()

    ## Rock death by bullet
    for sidebullet in side_bullet_sprites_list:
        side_bullet_hit_list = pygame.sprite.spritecollide(sidebullet, rock_list, False)
        for rock_killed in side_bullet_hit_list:
            sidebullet.kill() # Remove bullet
            rock_killed.death()

    ## Making sure rock isn't touching hole
    for rock in rock_list:
        rock_dont_touch_hole = pygame.sprite.spritecollide(rock, hole_list, True)


    # --- World Generation Logic

    if level == 1:
        time_since_hole_gen += dt
        if time_since_hole_gen > random.randrange(60, 80):
            genHole(random.randrange(700, 730), 0) # Gen small hole
            time_since_hole_gen = 0

    elif level == 2:
        time_since_hole_gen += dt
        if time_since_hole_gen > random.randrange(40, 60):
            genHole(random.randrange(700, 730), 0) # Gen small hole
            time_since_hole_gen = 0

        time_since_ufo_gen += dt
        if time_since_ufo_gen > random.randrange(70, 120) and len(ufo_sprites_list) == 0:
            ufo_gen_spot = random.randrange(-60, -20)
            genUFO(random.random() * 1.8 + 1.3, ufo_gen_spot)
            genUFO(random.random() * 1.8 + 1, ufo_gen_spot - random.randrange(60, 90))
            time_since_ufo_gen = 0

        for ufo in ufo_sprites_list:
            if ufo.last_dropped_bomb > random.randrange(20, 30):
                ufo.dropBomb(all_sprites_list, bomb_list)
                ufo.last_dropped_bomb = 0

    elif level == 3:
        time_since_hole_gen += dt
        if time_since_hole_gen > random.randrange(35, 55):
            if oneInThree() == 1:
                genHole(random.randrange(700, 730), 1) # 1/3 chance of gen medium hole
            else:
                genHole(random.randrange(700, 730), 0)
            time_since_hole_gen = 0

        time_since_ufo_gen += dt
        if time_since_ufo_gen > random.randrange(65, 100) and len(ufo_sprites_list) == 0:
            ufo_gen_spot = random.randrange(-60, -20)
            genUFO(random.random() * 1.8 + 1.5, ufo_gen_spot)
            genUFO(random.random() * 1.8 + 1.2, ufo_gen_spot - random.randrange(60, 90))
            time_since_ufo_gen = 0

        for ufo in ufo_sprites_list:
            if ufo.last_dropped_bomb > random.randrange(10, 20):
                ufo.dropBomb(all_sprites_list, bomb_list)
                ufo.last_dropped_bomb = 0

    elif level == 4:
        time_since_hole_gen += dt
        if time_since_hole_gen > random.randrange(40, 70):
            if oneInThree() == 1:
                genHole(random.randrange(700, 730), 1) # 1/3 chance of gen medium hole
            else:
                genHole(random.randrange(700, 730), 0)
            time_since_hole_gen = 0

        time_since_ufo_gen += dt
        if time_since_ufo_gen > random.randrange(70, 110) and len(ufo_sprites_list) == 0:
            ufo_gen_spot = random.randrange(-60, -20)
            genUFO(random.random() * 1.8 + 1.5, ufo_gen_spot)
            genUFO(random.random() * 1.8 + 1.2, ufo_gen_spot - random.randrange(60, 90))
            time_since_ufo_gen = 0

        for ufo in ufo_sprites_list:
            if ufo.last_dropped_bomb > random.randrange(15, 30):
                ufo.dropBomb(all_sprites_list, bomb_list)
                ufo.last_dropped_bomb = 0

        time_since_rock_gen += dt
        if time_since_rock_gen > random.randrange(40, 50):
            genRock(random.randrange(650, 690), random.randrange(0, 2))
            time_since_rock_gen = 0

    elif level == 5:
        time_since_hole_gen += dt
        if time_since_hole_gen > random.randrange(40, 70):
            if oneInThree() == 1:
                genHole(random.randrange(700, 730), 1) # 1/3 chance of gen medium hole
            else:
                genHole(random.randrange(700, 730), 0)
            time_since_hole_gen = 0

        time_since_ufo_gen += dt
        if time_since_ufo_gen > random.randrange(50, 120) and len(ufo_sprites_list) == 0:
            ufo_gen_spot = random.randrange(-100, -20)
            genUFO(random.random() * 1.8 + 1.5, ufo_gen_spot)
            genUFO(random.random() * 1.8 + 1.2, ufo_gen_spot - random.randrange(70, 130))
            genUFO(random.random() * 1.8 + 1, ufo_gen_spot - random.randrange(160, 180))
            time_since_ufo_gen = 0

        for ufo in ufo_sprites_list:
            if ufo.last_dropped_bomb > random.randrange(20, 35):
                ufo.dropBomb(all_sprites_list, bomb_list)
                ufo.last_dropped_bomb = 0

        time_since_rock_gen += dt
        if time_since_rock_gen > random.randrange(50, 70):
            genRock(random.randrange(650, 690), random.randrange(0, 2))
            time_since_rock_gen = 0

#    if pygame.time.get_ticks() % 1000 <= 500:
#        print("holes:", len(hole_list))


    # --- GAME FLOW LOGIC --- #
    if rover.status != "dead":
        bg_music.set_volume(0.8)
        bg_music.play(-1)
    elif rover.status == "dead" and dead_sequence_played_yet == False:
        bg_music.stop()
        crash_sfx.set_volume(0.6)
        crash_sfx.play(0)
        explosion = Explosion(rover.rect.x, rover.rect.y)
        explo_list.add(explosion)
        you_died = font_big.render("You Died!", True, BLACK)
        while pygame.mixer.get_busy():
            screen.fill(BLACK)
            world.drawBackground(screen)
            world.drawForeground(screen)
            world.drawGround(screen)
            hole_list.draw(screen)
            all_sprites_list.draw(screen)
            screen.blit(you_died, [110, SCREEN_HEIGHT / 2])
            explo_list.draw(screen)
            explo_list.update()
            pygame.display.flip()
            clock.tick(5)

        game_over_music.set_volume(0.4)
        game_over_music.play(0)
        dead_sequence_played_yet = True
        print("rover killed, game over")

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

    score_txt = font.render("Score: " + str(ufos_killed), True, BLACK)
    screen.blit(score_txt, [50, SCREEN_HEIGHT - 40])

    if rover.status == "dead" and pygame.mixer.get_busy() == False:
        print("Rover dead, music done")
        outro_screen()

    # --- Rover Control
    rover.blitWheels(screen)
    #rover.updateWheels()
    rover.calc_grav()
    rover.update(rover_speed)

    bullet_sprites_list.update()

    # --- UFO Control
    ufo_sprites_list.update(dt)
    bomb_list.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()  # Close the window and quit.
