import pygame
import numpy as np

grid_size = 50
num_row = 8
num_column = 12
screen_width = grid_size*num_column
screen_height = grid_size*num_row
screen = pygame.display.set_mode([screen_width, screen_height])
screen.fill((0, 0, 0))

grass_block = pygame.image.load('grass_block.png')
grass_block = pygame.transform.scale(grass_block, (grid_size, grid_size))

path_block = pygame.image.load('grass.png')
path_block = pygame.transform.scale(path_block, (grid_size, grid_size))

map = np.zeros((num_row,num_column),np.int32)

def draw_map():
    for i in range(num_row):
        grid_y = i*grid_size
        for j in range(num_column):
            grid_x = j*grid_size
            if map[i][j] == 0:
                screen.blit(path_block, (grid_x, grid_y))
            else:
#                screen.blit(path_block, (grid_x, grid_y))
                screen.blit(grass_block, (grid_x, grid_y))

state='initialize'; i=0; j=0; map[i][j]=1;
draw_map()
pygame.display.update()
Running = True

while(Running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        # Start initialization state: User creates the path
        # Only down (k) and right (l) keys are allowed
        # Starting with top left
        if (event.type == pygame.KEYDOWN)&(state=='initialize'):
            if event.key == pygame.K_l:
                if j<num_column-1: j+=1 # Can't move off screen
            if event.key == pygame.K_k:
                if i<num_row-1: i+=1 # Can't move off screen
            map[i][j]=1 # Add a path block in desired location
            draw_map()
            pygame.display.update()
            if (i==num_row-1)&(j==num_column-1): # Path established
                state='play'
                print("PLAY!")
        # End of Initialization
        # Code for gameplay goes here
