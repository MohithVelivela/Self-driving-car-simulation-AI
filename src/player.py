import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Assigning all the player variable and initial setup
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1),
                                                                  int(self.image.get_height() *  0.1)))
        
        self.width = 100
        self.height = 50
        self.vel = (0,0)
        self.speed = 5

        self.rect = pygame.Rect(x, y, self.width(), self.height())

    def update(self, screen):
        # This function is called once a frame

        self.move()

        # Checking if the player is outside the screen or dies
        if self.rect.top > screen.get_height() + 100 or self.rect.left < 0:
            pass

        # temp variable to see if grounded
        moved_hitbox = self.rect

        # Drawing the player
        screen.blit(self.image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
