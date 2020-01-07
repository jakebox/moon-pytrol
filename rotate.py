"""
Image manipualtion examples
Aaron Lee - 2019
"""
import math

import pygame
import random
pygame.init()  # initializes pygame (necessary before any pygame functions)


# Global Variables
BLACK = (0, 0, 0)  # red, green, blue (RGB)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PINK = (255, 200, 200)
MAROON = (100, 0, 0)
ORANGE = (255, 150, 0)
PURPLE = (150, 50, 200)
GRAY = (240, 240, 240)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
done = False  # Loop until the user clicks the close button.

size = (SCREEN_WIDTH, SCREEN_HEIGHT)  # Set the width and height of the screen [width, height]
screen = pygame.display.set_mode(size)  # Screen object we draw to

pygame.display.set_caption("My Game")

clock = pygame.time.Clock()  # Used to manage how fast the screen updates

class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/leftwheel.png")
        self.rect = self.image.get_rect()

def rot_center(image, old_rect, angle):
    # rotate image around center of rect
    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    new_rect.center = old_rect.center
    return rotated_image, new_rect

all_sprites = pygame.sprite.Group()
timer = 0
# If you want a truly rotating object, you need to move it up and to the left, then rotate it, then move it back.
# for this I use the function rot_image() above
apple = Apple()
apple.rect.x = SCREEN_WIDTH / 2
apple.rect.y = SCREEN_HEIGHT / 2

all_sprites.add(apple)

for angle in range(0, 360, 10):
    apple = Apple()
    apple.rect.x = angle * 3  # draw bunch across screen
    apple.rect.y = apple.rect.height * 5  # move it down a row
    apple.image, apple.rect = rot_center(apple.image, apple.rect, angle)
    all_sprites.add(apple)


time_since_rot = 0
angle = 0
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop (input from user keyboard, mouse, game controller)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    dt = clock.tick(60)

    # --- Draw to screen
    screen.fill(GRAY)

    time_since_rot += dt

    '''
    if time_since_rot >= 50:
        if angle == 360:
            angle = 0
        else:
            angle += 10
            apple.image, apple.rect = rot_center(apple.image, apple.rect, angle)
            time_since_rot = 0
    if pygame.time.get_ticks() - timer > 500:
        timer = pygame.time.get_ticks()
        if angle == 360:
            angle = 0
        else:
            angle += 10
            apple.image, apple.rect = rot_center(apple.image, apple.rect, angle)
        print("hi")
    '''

    all_sprites.draw(screen)

    pygame.display.flip()  # Go ahead and update the screen with what we've drawn.

    #clock.tick(60)  # limit to 60 frames per second

pygame.quit()  # Close the window and quit.