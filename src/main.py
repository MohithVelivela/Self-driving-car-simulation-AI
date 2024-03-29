import pygame
from player import Player
import neat
import os 
import sys
import random
from math import sin, radians, degrees, copysign
import math


config_path = "./config.txt"
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
player = Player()

track = pygame.image.load("assets/imgs/circle-track-border.png")
track_border = pygame.image.load("assets/imgs/circle-track-border.png")
track_border_mask = pygame.mask.from_surface(track_border)
start = pygame.image.load("assets/imgs/start.png")



WIDTH = 1920
HEIGHT = 1080

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
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # For All Genomes Passed Create A New Neural Network
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0

            cars.append(Player())

        # Clock Settings
        # Font Settings & Loading Map
        clock = pygame.time.Clock()
        generation_font = pygame.font.SysFont("Arial", 30)
        alive_font = pygame.font.SysFont("Arial", 20)
        game_map = pygame.image.load("assets/imgs/circle-track-border.png").convert() # Convert Speeds Up A Lot
        #print("init")

        global current_generation
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
                #print("for_in_2")
                output = nets[i].activate(car.get_data())
                choice = output.index(max(output))
                if car.steering:
                    turning_radius = car.length / sin(radians(car.steering))
                    angular_velocity = car.velocity.x / turning_radius
                else:
                    angular_velocity = 0 
                car.velocity += (car.acceleration * dt, 0)
                car.velocity.x = max(-car.max_velocity, min(car.velocity.x, car.max_velocity))
                #print(f"Choice : {choice}")
                if choice == 0:
                    car.steering += car.rotate_speed * dt# Left
                elif choice == 1:
                    car.steering -= car.rotate_speed * dt# Right
                elif choice == 2:
                    if car.velocity.x < 0:
                        car.acceleration = car.brake_deceleration
                    else:
                        car.acceleration += 1 * dt
                else:
                    if car.velocity.x > 0:
                        car.acceleration = -car.brake_deceleration
                    else:
                        car.acceleration -= 1 * dt
            
            # Check If Car Is Still Alive
            # Increase Fitness If Yes And Break Loop If Not
            still_alive = 0
            for i, car in enumerate(cars):
                #print("for_in_3")
                if car.is_alive(track_border_mask):
                    still_alive += 1
                    car.update(screen,dt,track_border,track_border_mask,config)
                    genomes[i][1].fitness += car.get_reward()

            if still_alive == 0:
                break

            counter += 1
            if counter == 30 * 40: # Stop After About 20 Seconds
                break

            # Draw Map And All Cars That Are Alive
            screen.blit(game_map, (0, 0))
            for car in cars:
                #print("for_in_4")
                if car.is_alive(track_border_mask):
                    car.draw(screen)
            
            # Display Info
            text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            screen.blit(text, text_rect)

            text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            screen.blit(text, text_rect)

            pygame.display.flip()
            clock.tick(40) # 40 FPS

if __name__ == "__main__":
    
    # Load Config
    config_path = "./config.txt"
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
