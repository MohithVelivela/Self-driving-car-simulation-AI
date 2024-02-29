import pygame
from player import Player


# Setting up pygame and window
pygame.init()
screen_height = 750
screen_width = 1100

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

running = True

playerGroup = pygame.sprite.Group()
Player.containers = playerGroup
player = Player(screen_width / 2, screen_height / 2, "lightning-mcqueen_disney_gallery_5d80191aeae5a.png")

# Game loop
while running:
    dt = 0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((0, 0, 0))
    rotated = pygame.transform.rotate(player.image, player.angle)
    rect = rotated.get_rect()
    screen.blit(rotated, player.position)
    pygame.display.flip()


    player.update(screen,dt)

    # Updating screen
    clock.tick(60)
    pygame.display.update()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

pygame.quit()
