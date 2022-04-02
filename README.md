# neat_car_driving_project

# dependencies
  Before running this code make sure you have pygame and neat-python installed
  This can be done by running
    
  pip install pygame
  pip install neat-python
    
  In the command prompt.
  
  # how it works
  
The game is simple enough, a car has to weave between traffic without being hit. A point is earned for every car it passes, the cars appear in random order, and the cars speed up every 10 points.

My model initially starts with 3 input layers, 1 output layer, and no hidden layers. this can be changed in the neat config file. The output determines if the car switches lanes.
The fitness is determined by the score the cars achieve. normally it doesnt take more than 80 generations for the cars to figure out how to dodge, at the most it took 8 minutes to train on my computer.

neat documentation can be found [here](https://neat-python.readthedocs.io/en/latest/index.html)
pygame documentation can be found [here](https://www.pygame.org/docs/)
