import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Assigning all the player variable and initial setup
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.1),int(self.image.get_height() *  0.1)))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2
        self.acceleration = 0.0
        self.steering = 0.0                                                        
        self.width = 100
        self.height = 50
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, screen,dt):
        # This function is called once a frame
        
        
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        self.move(dt)

        # Checking if the player is outside the screen or dies
        if self.rect.top > screen.get_height() + 100 or self.rect.left < 0:
            pass

        # temp variable to see if grounded
        moved_hitbox = self.rect

        # Drawing the player
        screen.blit(self.image, self.rect)

    def move(self, dt):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if pressed[pygame.K_RIGHT]:
            self.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
