'''
Rover class for Moon Patrol
'''

import pygame

WHITE = (255, 255, 255)

def rot_center(image, old_rect, angle):
    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    new_rect.center = old_rect.center
    return rotated_image, new_rect

class Rover(pygame.sprite.Sprite):

    def __init__(self, grav, ground_pos):
        super().__init__()
        self.image = pygame.image.load("assets/rover.png")
        self.rect = self.image.get_rect()
        self.leftwheel = pygame.image.load("assets/leftwheel.png")
        self.rightwheel = pygame.image.load("assets/rightwheel.png")
        self.angle = 20
        self._leftwheel = self.leftwheel
        self.change_y = 0
        self.grav = grav
        self.ground_pos = ground_pos
        self.counter = 0

    def update(self, speed):
        self.speed = speed
        self.rect.x += self.speed
        self.rect.y += self.change_y
        #self.jiggle()

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.grav
 
        # See if we are on the ground.
        if self.rect.bottom >= self.ground_pos - 7 and self.change_y >= 0:
            self.change_y = 0
            self.rect.bottom = self.ground_pos - 7
 
    def jump(self):
        # If rover is on the ground, move up
        if self.rect.bottom == self.ground_pos - 7:
            self.change_y = -4

    def updateWheels(self):
        #self.leftwheel = pygame.transform.rotate(self._leftwheel, 10)
        self._leftwheel, self.rect = rot_center(self.leftwheel, self.rect, angle)
        self.angle += 5

    def blitWheels(self, screen):
        screen.blit(self._leftwheel, [self.rect.x + 3.5, self.rect.y + 30])
        screen.blit(self.rightwheel, [self.rect.x + 23.4, self.rect.y + 30])
        screen.blit(self._leftwheel, [self.rect.x + 42, self.rect.y + 30])

    def jiggle(self):
        if self.counter <= 5:
            self.rect.y += 0.5
            self.counter += 1
        if self.counter > 5:
            self.rect.y -= 0.5
            self.counter -= 1
        if self.counter == 11:
            self.counter = 0

class UpBullet(pygame.sprite.Sprite):

    def __init__(self, rover):
        super().__init__()
        self.image = pygame.Surface([2, 13])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centery = rover.rect.centery - 10
        self.rect.centerx = rover.rect.centerx - 13

    def update(self):
        self.rect.y -= 8 # Move the bullets up
        if self.rect.bottom < 0: # off the top of the SCREEN_WIDTH
            self.kill()

class SideBullet(pygame.sprite.Sprite):

    def __init__(self, rover):
        super().__init__()
        self.image = pygame.image.load("assets/sidebullet_smaller.png")
        self.rect = self.image.get_rect()
        self.call_pos = rover.rect.centerx
        self.rect.x = rover.rect.centerx + 7
        self.rect.y = rover.rect.centery - 4

    def update(self):
        self.rect.x += 5
        if self.rect.left >= self.call_pos + 160:
            self.kill()

# -------- Main Program Loop -----------

if __name__ == "__main__":

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    angle = 0
    ground_pos = 240
    rover_speed = 0.5
    rover_gravity = 0.4

    pygame.init()
    
    all_sprites_list = pygame.sprite.Group()
    bullet_sprites_list = pygame.sprite.Group()


    rover = Rover(rover_gravity, ground_pos)
    rover.rect.x = 320
    rover.rect.y = 200

    all_sprites_list.add(rover)

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
                new_bullet = UpBullet(rover) # make new bullet sprite
                new_side_bullet = SideBullet(rover)
                all_sprites_list.add(new_bullet) # adding it to the container to be drawn
                all_sprites_list.add(new_side_bullet)
                bullet_sprites_list.add(new_bullet)
                bullet_sprites_list.add(new_side_bullet)

        # Clear the screen
        screen.fill(BLACK)

        # Draw stuff
        all_sprites_list.draw(screen)
        rover.blitWheels(screen)
        #rover.updateWheels()
        rover.calc_grav()
        rover.update(rover_speed)

        rover.update(rover_speed)

        bullet_sprites_list.update()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
