import pygame


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

map = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0] ]

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

draw_map()
pygame.display.update()
Running = True

while(Running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
