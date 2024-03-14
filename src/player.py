import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import time



class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image, angle=0.0, length=4, max_steering=2, max_acceleration=2.0):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Assigning all the player variable and initial setup
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), 
                                                        int(self.image.get_height() *  0.2)))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 25
        self.brake_deceleration = 5
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

    def update(self, screen,dt, track_border):
        # This function is called once a frame
        
       
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
	
        if self.collide(track_border):
            #TODO Replace with reset to end the game
            font = pygame.font.Font(None, 72)
            self.reset()
            self.position = Vector2(500, 800)  
            screen.blit(font.render("Game Over! Better Luck Next time", True, (255, 0, 0)), (600, 500))
            pygame.display.flip()
            time.sleep(1)
            
            #self.bounce()

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        screen.blit(rotated, rect)
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
