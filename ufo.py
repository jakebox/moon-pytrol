'''
UFO class for Moon-Pytrol
'''

import pygame
import random

class UFO(pygame.sprite.Sprite):

    def __init__(self, speed, ground_pos, all_sprites_list, bomb_list):
        super().__init__()
        self.image = pygame.image.load("assets/alien2.png")
        self.rect = self.image.get_rect()
        self.ground_pos = ground_pos
        self.movementSpeed = speed
        self.status = "alive"
        self.screened_yet = 0
        self.last_dropped_bomb = 0

    def update(self, dt):
        if self.screened_yet == 0: # Making sure UFO doesn't go off screen
            if self.rect.x >= 50:
                self.screened_yet = 1
        if self.screened_yet == 1:
            if self.rect.x >= 500:
                self.movementSpeed = -self.movementSpeed #* random.random()
                self.rect.y += random.randrange(15, 23)
            elif self.rect.x <= 30: #and self.screened_yet == 1:
                self.movementSpeed = -self.movementSpeed# * random.random()
                self.rect.y += random.randrange(15, 23)
        self.rect.x += self.movementSpeed
        self.last_dropped_bomb += dt

    def dropBomb(self, all_list, bomb_list):
        if self.status == "alive":
            bomb = Bomb(self.rect.x + 10, self.rect.y, self.ground_pos, 3.5)
            all_list.add(bomb)
            bomb_list.add(bomb)

class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y, ground_pos, bomb_speed):
        super().__init__()
        self.image = pygame.image.load("assets/ufobomb_smaller.png")
        self.rect = self.image.get_rect()
        self.ground_pos = ground_pos
        self.bomb_speed = bomb_speed 
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.bomb_speed

        if self.rect.bottom >= self.ground_pos + 15: # failsafe-ish, remove later when logic/true game added
            self.kill()

# -------- Main Program Loop -----------

if __name__ == "__main__":

    WHITE = (255, 255, 255)
    ground_pos = 240
    ufo_speed = 0.5

    pygame.init()
    
    all_sprites_list = pygame.sprite.Group()
    bomb_list = pygame.sprite.Group()

    ufo = UFO(ufo_speed, ground_pos, all_sprites_list, bomb_list)
    ufo.rect.x = 35
    ufo.rect.y = 59

    all_sprites_list.add(ufo)

    pygame.display.set_caption("Jake's Game")
    screen_width = 640
    screen_height = 300
    screen = pygame.display.set_mode([screen_width, screen_height])
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ufo.dropBomb(all_sprites_list, bomb_list)

        # Clear the screen
        screen.fill(WHITE)

        # Draw stuff
        all_sprites_list.draw(screen)

        ufo.update()

        bomb_list.update()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
