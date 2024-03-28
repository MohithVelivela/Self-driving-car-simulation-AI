import pygame
from player import Player
import neat
import os 
import sys
import random
from math import sin, radians, degrees, copysign
import math
import time

config_path = "src/config.txt"
config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

# Setting up pygame and window
pygame.init()
"""screen_height = 1080
screen_width = 1920"""

"""screen = pygame.display.set_mode((screen_width, screen_height))"""

clock = pygame.time.Clock()

running = True

playerGroup = pygame.sprite.Group()
Player.containers = playerGroup
#player = Player()



Maps = { "Oval" : ["src/assets/imgs/Oval_track.png","src/assets/imgs/Oval_track.png",pygame.Vector2(950,820)],
	  "Triangular" : ["src/assets/imgs/Triangular_track.png","src/assets/imgs/Triangular_track.png",pygame.Vector2(660,880)],
	  "Infinity" : ["src/assets/imgs/Infinity_track.png","src/assets/imgs/Infinity_track.png",pygame.Vector2(550,840)]
	}

Current_Track = "Oval"

WIDTH = 1280
HEIGHT = 720

CAR_SIZE_X = 60    
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255) # Color To Crash on Hit
screen = pygame.display.set_mode((WIDTH,HEIGHT))

current_generation = 0 # Generation counter

dt = 0.5



# Game loop
"""while running:
    dt = 0.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Drawing the background
    screen.fill((30, 30, 30))
    screen.blit(start, (600, 700))
    screen.blit(track, (0,0))


    # Player Update
    player.update(screen,dt, track_border ,track_border_mask,config)
    #print("Hello\n")

    # Updating screen
    clock.tick(60)
    pygame.display.flip()
    pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')"""

def run_simulation(genomes, config):
    
        # Empty Collections For Nets and Cars
        nets = []
        cars = []

        # Initialize PyGame And The Display
        # pygame.init()
        # screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

        # For All Genomes Passed Create A New Neural Network
        global current_generation
        global Current_Track
        
            
        track_border_path = Maps[Current_Track][1]
        track_image_path = Maps[Current_Track][0]
        start_pos = Maps[Current_Track][2]
        track = pygame.image.load(track_image_path)
        track_border = pygame.image.load(track_border_path)
        track_border_mask = pygame.mask.from_surface(track_border)
        start = pygame.image.load("src/assets/imgs/start.png")

        if current_generation % 5 == 0:
            index = list(Maps.keys()).index(Current_Track)
            index = (index+1)%len(Maps)
            Current_Track = list(Maps.keys())[index]

        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0
	    	
            cars.append(Player(start_pos.x, start_pos.y, "src/assets/imgs/red-car.png"))

        # Clock Settings
        # Font Settings & Loading Map
        clock = pygame.time.Clock()
        generation_font = pygame.font.SysFont("Arial", 30)
        alive_font = pygame.font.SysFont("Arial", 20)
        
        game_map = pygame.image.load(track_image_path).convert() # Convert Speeds Up A Lot
        #print("init")

        #global current_generation
        current_generation += 1

        # Simple Counter To Roughly Limit Time (Not Good Practice)
        counter = 0

        while True: 
            #print("While_outer")
            for event in pygame.event.get():
                #print("for_in_1")
                if event.type == pygame.QUIT:
                    sys.exit(0)

            for i, car in enumerate(cars):
                output = nets[i].activate(car.get_data())
                steering_choice = [0 if output > 0 else 1 for output in output[:2]]
                accelerate_choice = [0 if output > 0 else 1 for output in output[2:]]

                steering, accelerate = 0, 0

                if steering_choice[0] == 1:
                    steering = 1
                elif steering_choice[1] == 1:
                    steering = -1

                if accelerate_choice[0] == 1:
                    accelerate = 1
                elif accelerate_choice[1] == 1:
                    accelerate = -1

                car.move(dt, steering, accelerate)

                # if car.steering:
                #     turning_radius = car.length / sin(radians(car.steering))
                #     angular_velocity = car.velocity.x / turning_radius
                # else:
                #     angular_velocity = 0 
                # car.velocity += (car.acceleration * dt, 0)
                # car.velocity.x = max(-car.max_velocity, min(car.velocity.x, car.max_velocity))
                # #print(f"Choice : {choice}")
                # if choice == 0:
                #     car.steering += car.rotate_speed * dt# Left
                # elif choice == 1:
                #     car.steering -= car.rotate_speed * dt# Right
                # elif choice == 2:
                #     if car.velocity.x < 0:
                #         car.acceleration = car.brake_deceleration
                #     else:
                #         car.acceleration += 1 * dt
                # else:
                #     if car.velocity.x > 0:
                #         car.acceleration = -car.brake_deceleration
                #     else:
                #         car.acceleration -= 1 * dt
            
            # Check If Car Is Still Alive
            # Increase Fitness If Yes And Break Loop If Not
            
            still_alive = 0
            best_car : Player = cars[0]
            max_distance = 0.0
            for i, car in enumerate(cars):
                if car.is_alive(track_border_mask):
                    if max_distance < car.dist_travelled:
                        max_distance = car.dist_travelled
                        best_car = car
                    still_alive += 1
                    car.update(screen,dt,track_border,track_border_mask,config)
                    genomes[i][1].fitness = car.get_reward()

            counter += 1
            if still_alive == 0 or counter == 600:
                break


            # Drawing the background 
            offset : pygame.Vector2 = pygame.Vector2(0,0)
            offset.x = best_car.rect.centerx - WIDTH//2
            offset.y = best_car.rect.centery - HEIGHT//2

            screen.fill((0,0,0))

            # Draw the track
            screen.blit(game_map, -offset)

            # Draw the lap start marker
            start_rect = start.get_rect()
            start_rect.center = start_pos - offset
            screen.blit(start, start_rect)

            # Draw All Cars That Are Alive
            for car in cars:
                #print("for_in_4")
                num_drawn = 0
                if car.is_alive(track_border_mask):
                    if num_drawn >= 15:
                        break
                    car.draw(screen, offset)
            
            # Display Info
            pygame.draw.rect(screen, (255,255,255) ,(0,0,180,100))
            text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.topleft = (10, 20)
            screen.blit(text, text_rect)

            text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (60, 70)
            screen.blit(text, text_rect.topleft)

            clock.tick(60)
            pygame.display.flip()
            pygame.display.set_caption(f'Current FPS: {str(clock.get_fps())}')

if __name__ == "__main__":
    
    # Load Config
    config_path = "src/config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)


"""pygame.quit()"""
