import pygame
from math import sin, radians, degrees, copysign
import math
from pygame.math import Vector2
import time



class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image, angle=0.0, length=4, max_steering=2, max_acceleration=1.0):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Assigning all the player variable and initial setup
        self.image = pygame.image.load(image)
        print(self.image.get_width())
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), 
                                                        int(self.image.get_height() * 0.2)))
        print(self.image.get_width())
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 25
        self.brake_deceleration = 10
        self.free_deceleration = 0.5
        self.acceleration = 0.0
        self.steering = 0.0                                                        
        self.width = 100
        self.height = 50
        self.speed = 5
        self.lap = 0
        self.rotate_speed = 60

        self.bounce_force = 0.5

        self.rect = pygame.Rect(x, y, self.width, self.height)

        # RayCast
        self.raycasts = []

    def cast_rays(self, border : pygame.image, offset_angle = 0):
        length = 0

        x = int(self.rect.center[0] + math.cos(math.radians(360 - (self.angle + offset_angle))) * length)
        y = int(self.rect.center[1] + math.sin(math.radians(360 - (self.angle + offset_angle))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while border.get_at((x, y)).a == 0:
            length = length + 1
            x = int(self.rect.center[0] + math.cos(math.radians(360 - (self.angle + offset_angle))) * length)
            y = int(self.rect.center[1] + math.sin(math.radians(360 - (self.angle + offset_angle))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))
        self.raycasts.append(((x, y), dist))

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.raycasts:
            position = radar[0]
            pygame.draw.line(screen, (0, 0, 255), self.rect.center, position, 1)
            pygame.draw.circle(screen, (0, 0, 255), position, 5)

    def update(self, screen,dt, track_border : pygame.image, track_border_mask : pygame.mask):
        # This function is called once a frame

        for offset in range(-90, 120, 45):
            self.cast_rays(track_border, offset_angle = offset)
        self.draw_radar(screen)
        

        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0    

        self.move(dt)

        # Drawing the player
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=self.image.get_rect(topleft = self.position).center)

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        self.rect = rect

        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
        screen.blit(rotated, self.rect)

        self.raycasts.clear()
	
        if self.collide(track_border_mask):
            #TODO Replace with reset to end the game
            font = pygame.font.Font(None, 72)
            self.reset()
            self.position = Vector2(500, 800)  
            screen.blit(font.render("Game Over! Better Luck Next time", True, (255, 0, 0)), (600, 500))
            pygame.display.flip()
            time.sleep(1)
            
            #self.bounce()

        """if self.is_lap_completed():
            self.lap_counter += 1
            print("Lap completed. Total laps:", self.lap_counter)"""

    def move(self, dt):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_w]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif pressed[pygame.K_s]:
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

        if pressed[pygame.K_d]:
            self.steering -= self.rotate_speed * dt
        elif pressed[pygame.K_a]:
            self.steering += self.rotate_speed * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def bounce(self):
        if False:
            self.velocity = Vector2(0,0)
        else:
            self.velocity = -self.velocity

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.position.x - x), int(self.position.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
        
    def reset(self):
        # Reset player's properties
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.steering = 0.0
        self.angle = 0.0
    
    # TODO should add Lap counter    
    """def is_lap_completed():
    	initial_x = 500
    	
    	if """
