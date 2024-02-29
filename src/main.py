import pygame

# Setting up pygame and window
pygame.init()
screen_height = 750
screen_width = 1100

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

running = True

player_x = 100
player_y = 100
player_speed = 5

# Game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((0, 0, 0))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y , 100, 50))

    # Updating screen
    clock.tick(60)
    pygame.display.update()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

pygame.quit()