import pygame
from math import sin, radians, degrees, copysign
import math
from pygame.math import Vector2
import time
import neat


CAR_SIZE_X = 60    
CAR_SIZE_Y = 60

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, image, angle=0.0, length=4, max_steering=0.8, max_acceleration=1.0):
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Assigning all the player variable and initial setup
        self.image = pygame.image.load(image)
        #print(self.image.get_width())
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), 
                                                        int(self.image.get_height() * 0.2)))
        #print(self.image.get_width())
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
        self.speed = 5
        self.lap = 0
        self.rotate_speed = 60
        self.alive = True
        self.dist_travelled = 0 
        self.time = 0

        self.rotated_image = self.image

        self.bounce_force = 0.5

        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

        # RayCast
        self.raycasts = []
        self.distance = []

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
        self.raycasts.append(((x,y),dist))
        self.distance.append(dist)
        """if len(self.distance) == 5:
            self.final = self.distance
        else:
            self.final = []
        print(self.final)
        print("len is 5")"""
    
    def draw(self,screen, offset : Vector2):
        screen.blit(self.rotated_image, self.position - offset) # Draw Sprite
        #self.draw_radar(screen, offset) #OPTIONAL FOR SENSORS
        
        

    def draw_radar(self, screen, offset):
        # Optionally Draw All Sensors / Radars
        for radar in self.raycasts:
            position = radar[0]
            pygame.draw.line(screen, (0, 0, 255), self.rect.center, position, 1)
            pygame.draw.circle(screen, (0, 0, 255), position, 5)

    def update(self, screen,dt, track_border : pygame.image, track_border_mask : pygame.mask,config):
        # This function is called once a frame

        self.raycasts.clear()
        self.distance.clear()

        for offset in range(-90, 120, 45):
            self.cast_rays(track_border, offset_angle = offset)
        #self.draw_radar(screen)
        

        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0    

        # if self.acceleration < 0 and self.velocity.x < 0:
        #     print("going back")
            
        #self.move(dt)
        # Calculate distance travelled
        self.dist_travelled += self.get_magnitude(self.velocity)
        self.time += 1
        # Drawing the player
        rotated = pygame.transform.rotate(self.image, self.angle)
        self.rotated_image = rotated
        rect = rotated.get_rect(center=self.image.get_rect(topleft = self.position).center)

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt
        self.rect = rect

        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
        #screen.blit(rotated, self.rect)
	
        if self.collide(track_border_mask):
            #TODO Replace with reset to end the game
            font = pygame.font.Font(None, 72)
            #self.reset()
            #self.position = Vector2(500, 800)  
            #screen.blit(font.render("Game Over! Better Luck Next time", True, (255, 0, 0)), (600, 500))
            self.alive = False
            #time.sleep(1)
            
            #self.bounce()

        """if self.is_lap_completed():
            self.lap_counter += 1
            print("Lap completed. Total laps:", self.lap_counter)"""

    def move(self, dt, steering, accelerate):
        pressed = pygame.key.get_pressed()

        if accelerate == 1:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif accelerate == -1:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                #self.acceleration -= 1 * dt
                self.acceleration = 0
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

        if steering == 1:
            self.steering -= self.rotate_speed * dt
        elif steering == -1:
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
        car_mask = pygame.mask.from_surface(self.rotated_image)
        offset = (int(self.position.x - x), int(self.position.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
        
    def reset(self):
        self.velocity = Vector2(0.0, 0.0)
        self.acceleration = 0.0
        self.steering = 0.0
        self.angle = 0.0

    def get_data(self):
        distance = self.distance
        return_values = [0, 0, 0, 0, 0, self.get_magnitude(self.velocity)]
        for i, radar in enumerate(distance):
            return_values[i] = int(distance[1] / 30)

        return return_values
    
    
    def is_alive(self,track_border_mask : pygame.mask):
        if self.collide(track_border_mask):
            self.alive = False
        return self.alive
    

    def get_reward(self):
        return self.dist_travelled / (CAR_SIZE_X / 2)
    

    def get_magnitude(self, vector : Vector2):
        return (vector.x**2 + vector.y**2)**0.5 

    # TODO should add Lap counter    




