from ctypes.wintypes import POINT
import math
from pickle import POP
from turtle import Screen, distance
import pygame
import neat
import random
import sys

pygame.init()


#-----------------------------
# car game neat project
# by Brandon Short
#
# thanks to https://github.com/codewmax for 
# for helping me get started
#-----------------------------

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 32)
background_image = pygame.image.load("bg.png")

# obstacle class. in this case, a slew of blue cars
class Obs:
    def __init__(self, loc):
        self.image = pygame.image.load("obs.png")
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.top = loc < 310
        self.rect.y = loc

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)     
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

# player class, or a slew of red cars.
class Player:
    x = 80
    y = 310
    jump_vel = 8.5

    def __init__(self):
        self.avatar = pygame.image.load("player.png")
        self.jump_velocity = self.jump_vel
        self.run_action = True
        self.up = False
        self.jump_action = False
        self.init_y_pos = self.y
        self.rect = pygame.Rect(self.x, self.y, self.avatar.get_width(), self.avatar.get_height())
    # update the screens    
    def update(self):
        if self.run_action:
            self.move()
        if self.jump_action:
            self.jump()
    # jumping between the lanes
    def jump(self):
        if self.jump_action and self.up == False:
            self.rect.y -= 8
            
            if self.rect.y < 242:
                self.rect.y = 242
                self.up = True
                self.run_action = True
                self.jump_action = False
    
                
        elif self.jump_action and self.up == True:
            self.rect.y += 8
            
            if self.rect.y > 310:
                self.rect.y =310
                self.up = False
                self.run_action = True
                self.jump_action = False

    def move(self):
        self.rect.x = self.x
        if self.up == True:
            self.rect.y = 242
        else:
            self.rect.y = 310

    def display(self, SCREEN):
        SCREEN.blit(self.avatar,(self.rect.x, self.rect.y))
# remove the players that "died"
def remove(index):
    players.pop(index)
    ge.pop(index)
    nets.pop(index)

# evaluates and configures the genomes
def eval_genomes(genomes,config):
    global game_speed, points, players, obstacles, ge, nets
    clock = pygame.time.Clock()
    obstacles = []
    players = []
    #genomes
    ge = []
    #networks
    nets = []

    for id, genome in genomes:
        players.append(Player())
        ge.append(genome)
        ## feed forward network based on the config file
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        genome.fitness = 0

    game_speed = 20
    points = 0
    def score():
        global points, game_speed
        #points += 1
        if points %10 == 0:
            game_speed += 1
        print(points)
    
    counter = 0
    tcounter = 0
    
    #game loops
    while True:
        # this allows us to close the screen
        for event in pygame.event.get(): 
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # when everyone is dead we jump out of the loop
        if len(players) == 0:
            break
        #generates the other cars
        if len(obstacles) == 0:
            points += 1
            temp2 = 310
            temp = random.randint(0,1)
            if temp == 1:
                temp2 = 242

            obstacles.append(Obs(temp2))            
            counter = random.randint(80,150)
        counter = counter - 1

        SCREEN.blit(background_image, (0, 0))
        # update the players and draw them on screen
        for player in players:
            player.update()
            player.display(SCREEN)

        #update the obstacles and draw them on screen
        for ob in obstacles:
            ob.draw(SCREEN)
            ob.update()
            for i, player in enumerate(players):
                ge[i].fitness =+ points

                if player.rect.colliderect(ob.rect):
                    remove(i)

                      
               
        # test to see what the networks predict and act accordingly
        for i, player in enumerate(players):
            output = nets[i].activate((player.rect.y, ob.rect.x,(player.up == ob.top)))

            

            if output[0] > .5:
            
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_RIGHT]:
            
                #ge[i].fitness =- 100
                player.run_action = False
                player.jump_action = True
            output =0    
            
            
            
            if player.run_action == True:
                tcounter = tcounter + 1
                if tcounter == 50:
                    ge[i].fitness =- 200
                    tcounter = 0
            else:
                tcounter = 0


        text = font.render("score :{}".format(points), True, (255,255,255),(0,0,0))
        textRect = text.get_rect()
        textRect.center = (80, 50)
        SCREEN.blit(text, textRect)
        
        text1 = font.render("generation :{}".format(pop.generation + 1), True, (0,0,0),(255,255,255))
        textRect1 = text1.get_rect()
        textRect1.center = (300, 50)
        SCREEN.blit(text1, textRect1)

        
        text2 = font.render("player count :{}".format(len(players)), True, (0,0,0),(255,255,255))
        textRect2 = text2.get_rect()
        textRect2.center = (600, 50)
        SCREEN.blit(text2, textRect2)

        
        score()
        pygame.display.flip()
        clock.tick(30)
        pygame.display.update()
        

# running the model
def run(config_p):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_p
    )

    pop = neat.Population(config)
    pop.run(eval_genomes,1000)

if __name__ == '__main__':
    run('config.txt')
