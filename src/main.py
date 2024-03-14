import pygame
from player import Player


# Setting up pygame and window
pygame.init()
screen_height = 1080
screen_width = 1920

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

running = True

playerGroup = pygame.sprite.Group()
Player.containers = playerGroup
player = Player(500, 800, "assets/imgs/car_dir_updated.png")

track = pygame.image.load("assets/imgs/circle-track-border.png")
track_border = pygame.image.load("assets/imgs/circle-track-border.png")
track_border_mask = pygame.mask.from_surface(track_border)

# Game loop
while running:
    dt = 0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((0, 0, 0))
    screen.blit(track, (0,0))
    player.update(screen,dt, track_border_mask)

    # Updating screen
    clock.tick(60)
    pygame.display.flip()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

pygame.quit()
