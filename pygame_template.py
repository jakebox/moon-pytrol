import pygame

pygame.init()  # vroom vroom pyamegame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

# Screen details setup
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jake's Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

time_elapsed_since_last_action = 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop (input from user mouse, keyboard, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic

    # --- Drawing code
    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, [0, 0, 100, 50])

    dt = clock.tick() 

    print(time_elapsed_since_last_action)

    time_elapsed_since_last_action += dt


    pygame.display.flip()  # updates the screen

    clock.tick(60)  # frames per second

pygame.quit()  # Close the window and quit.
