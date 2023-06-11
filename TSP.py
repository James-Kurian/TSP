import pygame
import numpy as np
import math
from MA import MA
# import random
 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
 
# initialize pygame
pygame.init()
screenX = 700
screenY = 500
screen_size = (screenX, screenY)


cities = []
adjacencyMatrix = []
numCities = 30

#random city pos
for i in range(numCities):
    cities.append((math.ceil(np.random.rand()*700), math.ceil(np.random.rand()*500)))

#circular city pos
# angleInc = (math.pi * 2) / numCities
# angle = 0
# radius = 200
# for i in range(numCities):
#     cities.append(( screenX/2 + radius * math.cos(angle), screenY/2 + radius * math.sin(angle)))
#     angle+=angleInc

#gen adjacency matrix
for pos in cities:
    distances = []
    for pos2 in cities:
        distances.append( math.sqrt( ((pos2[0]-pos[0])**2) + ((pos2[1]-pos[1])**2))  )
    adjacencyMatrix.append(distances)
 
# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("TSP")
surface_size = (25, 45)
 
# clock is used to set a max fps
clock = pygame.time.Clock()


##memetic algorithm setup
crossRate = 0.5
maxIterations = 1000
popSize = 1000
strLength = 5
mutationRate = 0.1
maxLocalSearchJump = 2
neighbourSize = 2
localSearchIterations = 10
seed = math.floor(np.random.rand()*1000)
print("Seed: " + str(seed)) 
printGenerations = False
np.random.seed(seed)
TSPSolver = MA(cities, 0, crossRate, mutationRate, maxIterations, popSize, maxLocalSearchJump, neighbourSize, localSearchIterations, adjacencyMatrix, printGenerations)
startPop = TSPSolver.getPop()


 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
    
    screen.fill(BLACK)
    for pos in cities:
       pygame.draw.circle(screen, (255,255,255), pos, 5)


    # LOGIC

    TSPSolver.runIterations(1)
    currBest = TSPSolver.getBest()
    print(currBest)
    for i in range(len(currBest)-1):
        pygame.draw.line(screen, (255,255,255),cities[currBest[i]], cities[currBest[i+1]])


 
    pygame.display.flip()
     
    # how many updates per second
    clock.tick(20)
 
pygame.quit()






# if __name__ == "__main__":
#     crossRate = 0.5
#     maxIterations = 60
#     popSize = 4
#     strLength = 5
#     mutationRate = 0.3
#     maxLocalSearchJump = 2
#     neighbourSize = 2
#     localSearchIterations = 10
#     seed = math.floor(np.random.rand()*1000)
#     print("Seed: " + str(seed)) 
#     printGenerations = True
#     np.random.seed(seed)
  
    
#     simpleGeneticAlgorithm = MA(lambda x : (-0.25*(x-5)**4)+0.15*((x-5)**3)+5*((x-5)**2), crossRate, mutationRate, maxIterations, strLength, popSize, maxLocalSearchJump, neighbourSize, localSearchIterations, printGenerations)
#     startPop = simpleGeneticAlgorithm.getPop()
#     simpleGeneticAlgorithm.run()
