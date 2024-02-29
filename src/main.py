import pygame

# Setting up pygame and window
pygame.init()
screen_height = 750
screen_width = 1100

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

running = True

# Game variables
gravity = 1

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((0, 0, 0))

    # Updating screen
    clock.tick(60)
    pygame.display.update()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

pygame.quit()