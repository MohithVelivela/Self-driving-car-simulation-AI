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
        self.rect = pygame.Rect(x, y, self.width(), self.height())

    def update(self, screen):
        # This function is called once a frame
        dt = pygame.time.Clock().get_time() / 1000
        
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        self.move()

        # Checking if the player is outside the screen or dies
        if self.rect.top > screen.get_height() + 100 or self.rect.left < 0:
            pass

        # temp variable to see if grounded
        moved_hitbox = self.rect

        # Drawing the player
        screen.blit(self.image, self.rect)

    def move(self):
        dt = pygame.time.Clock().get_time() / 1000
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            if car.velocity.x < 0:
                car.acceleration = car.brake_deceleration
            else:
                car.acceleration += 1 * dt
        elif pressed[pygame.K_s]:
            if car.velocity.x > 0:
                car.acceleration = -car.brake_deceleration
            else:
                car.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(car.velocity.x) > dt * car.brake_deceleration:
                car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
            else:
                car.acceleration = -car.velocity.x / dt
        else:
            if abs(car.velocity.x) > dt * car.free_deceleration:
                car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
            else:
                if dt != 0:
                    car.acceleration = -car.velocity.x / dt
        car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

        if pressed[pygame.K_d]:
            car.steering -= 30 * dt
        elif pressed[pygame.K_a]:
            car.steering += 30 * dt
        else:
            car.steering = 0
        car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
