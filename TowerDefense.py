import pygame


grid_size = 50
num_row = 8
num_column = 12
screen_width = grid_size*num_column
screen_height = grid_size*num_row
screen = pygame.display.set_mode([screen_width, screen_height])
#screen.fill((0, 0, 0))

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

path = [ [8,0], [8,1], [8,2], [8,3], [8,4], [8,5], [8,6], [8,7], [8,8], [8,9], [7,9], [6,9], [5,9], [5,10], [5,11], [4,11], [3,11], [2,11], [2,12], [1, 12]]

def move_to(object, cx, cy, goal_x, goal_y, num_steps):
    rect = object.get_rect()
    cx += (goal_x - cx)/num_steps
    cy += (goal_y - cy)/num_steps
    rect.center = (cx, cy)
    screen.blit(object1, rect)
    screen.blit(object2, rect)
    return cx, cy

def draw_map():
    for b in range(num_row):
        grid_y = b*grid_size
        for j in range(num_column):
            grid_x = j*grid_size
            if map[b][j] == 0:
                screen.blit(path_block, (grid_x, grid_y))
            else:
#                screen.blit(path_block, (grid_x, grid_y))
                screen.blit(grass_block, (grid_x, grid_y))

pygame.display.update()
Running = True

def draw_enemy(enemy):
    tank = enemy[0]
    num_steps = enemy[1]
    cx = enemy[2]
    cy = enemy[3]
    old_direction = enemy[4]
    goal_x = enemy[5]
    goal_y = enemy[6]
    i = enemy[7]
    if num_steps > 1:
        num_steps -= 1
    else:
        if i < len(path)-1:
            i += 1
            num_steps = 30
            goal_y = path[i][0]*grid_size+grid_size/2
            goal_x = path[i][1]*grid_size+grid_size/2
            enemy[0] = tank
            enemy[5] = goal_x
            enemy[6] = goal_y
            enemy[7] = i
            direction = 0
            if goal_y > cy + 1:
                direction = -90
            if goal_y < cy-1:
                direction = +90
            if goal_x < cx - 1:
                direction = 180
            tank = pygame.transform.rotate(tank, direction-old_direction)
            old_direction = direction
            cx, cy = move_to(tank, cx, cy, goal_x, goal_y, num_steps)
            enemy[1] = num_steps
            enemy[2] = cx
            enemy[3] = cy
        else:
            return False

enemy_list = []
last_time = 0
num_enemy = 20
enemy_control = 0
while(Running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    if pygame.time.get_ticks() - last_time > 2000 and enemy_control < num_enemy:
        enemy_list.append([tank, 0, -40, 520, 0, 0, 0, -1])
        last_time = pygame.time.get_ticks()
        enemy_control += 1
    draw_map()
    pygame.display.update()
    for enemy in enemy_list:
        draw_enemy(enemy)
