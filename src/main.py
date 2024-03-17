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
player = Player(500, 800, "assets/imgs/red-car.png")

track = pygame.image.load("assets/imgs/circle-track-border.png")
track_border = pygame.image.load("assets/imgs/circle-track-border.png")
track_border_mask = pygame.mask.from_surface(track_border)
start = pygame.image.load("assets/imgs/start.png")

# Game loop
while running:
    dt = 0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((30, 30, 30))
    screen.blit(start, (600, 700))
    screen.blit(track, (0,0))


    # Player Update
    player.update(screen,dt, track_border ,track_border_mask)

    # Updating screen
    clock.tick(60)
    pygame.display.flip()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

pygame.quit()
