import pygame
pygame.init()

#create screen
grid_size = 80 #map is grid base,size of the map row X col
num_row = 8
num_col = 12
screen_width = grid_size*num_col
screen_height = grid_size*num_row
tower_selected = int(0)
tower = []
tower_list = []

screen = pygame.display.set_mode([screen_width, screen_height]) # size of screen
background = pygame.image.load('images/grassy_bg2.png')
screen.blit(background, (0,0))

grass = pygame.image.load('images/towerDefense_tile129.png')
grass = pygame.transform.scale(grass, (grid_size, grid_size))

road = pygame.image.load('images/towerDefense_tile158.png')
road = pygame.transform.scale(road, (grid_size, grid_size))

base = pygame.image.load('images/towerDefense_tile018.png')
base = pygame.transform.scale(base, (grid_size, grid_size))

tank = pygame.image.load('images/towerDefense_tile268.png')
enemy_person = pygame.image.load('images/towerDefense_tile245.png')
cannon = pygame.image.load('images/towerDefense_tile291.png')

tower_base = pygame.image.load('images/towerDefense_tile181.png')
tower_base = pygame.transform.scale(tower_base, (grid_size, grid_size))

tower_gun = pygame.image.load('images/towerDefense_tile250.png')
tower_gun = pygame.transform.scale(tower_gun, (int(tower_gun.get_width()/1.2), int(tower_gun.get_height()/1.5)))

def draw_tower(tower):
	tower_base = tower[0]
	tower_gun = tower[1]
	x = tower[2]
	y = tower[3]
	a = tower[4]
	rect = tower_gun.get_rect()
	rect.center = (x+int(grid_size/2), y+int(grid_size/2))
	screen.blit(tower_base, (x, y))
	tower_gun = pygame.transform.rotate(tower_gun, a)
	screen.blit(tower_gun, rect)


#create map
map = [	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 0],
		[0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0],
		[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


path = [[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[5,6],[4,6],[3,6],[3,7],[3,8],[3,9],[2,9],[1,9],[0,9], [-1,9]]

def draw_map():
	screen.blit(background, (0,0))
	for i in range(num_row):
		grid_y = i*grid_size
		for j in range(num_col):
			grid_x = j*grid_size
			if map[i][j] == 1:
				screen.blit(road, (grid_x, grid_y))
			elif map[i][j] == 2:
				screen.blit(base, (grid_x, grid_y))

def move_to(object, cx, cy, goal_x, goal_y, num_steps):
	rect = object.get_rect()
	cx += (goal_x - cx)/num_steps
	cy += (goal_y - cy)/num_steps
	rect.center = (cx, cy)
	screen.blit(enemy_person, rect)
	#screen.blit(cannon, rect)
	return cx, cy

def draw_enemy(enemy):
	tank = enemy[0]
	num_steps = enemy[1]
	cx = enemy[2]
	cy = enemy[3]
	direction = enemy[4]
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
			direction = 0
			if goal_y > cy+1:
				direction = 90
			if goal_y < cy-1:
				direction = -90
			if goal_x < cx-1:
				direction = 180
			enemy[0] = tank
			enemy[4] = direction
			enemy[5] = goal_x
			enemy[6] = goal_y
			enemy[7] = i
		else:
			return False

	atank = pygame.transform.rotate(tank, direction)
	cx, cy = move_to(atank, cx, cy, goal_x, goal_y, num_steps)
	enemy[1] = num_steps
	enemy[2] = cx
	enemy[3] = cy
	return True

running = True
enemy_list = []
last_time = 0
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			grid_x = pos[0]//grid_size
			grid_y = pos[1]//grid_size
			if grid_x == 5 or grid_x == 6 and grid_y == 7:
				tower_selected = 1
		elif event.type == pygame.MOUSEBUTTONUP and tower_selected == 1:
			pos = pygame.mouse.get_pos()
			grid_x = pos[0]//grid_size
			grid_y = pos[1]//grid_size
			new_tower = [tower_base, tower_gun, grid_x*grid_size, grid_y*grid_size, 0]
			tower_list.append(new_tower)
			tower_selected = 0

	mouse_pressed = pygame.mouse.get_pressed()
	if mouse_pressed[0] == 1 and tower_selected == 1:
		pos = pygame.mouse.get_pos()
		tower = [tower_base, tower_gun, pos[0]-grid_size//2, pos[1]-grid_size//2, 0]
		draw_tower(tower)

	if pygame.time.get_ticks() - last_time > 2000:
		enemy_list.append([tank, 0, -40, 520, 0, 0, 0, -1])
		last_time = pygame.time.get_ticks()

	draw_map()

	tower_icon = [tower_base, tower_gun, 5.5*grid_size, 7*grid_size, 0]
	draw_tower(tower_icon)


	for enemy in enemy_list:
		if not draw_enemy(enemy):
			enemy_list.remove(enemy)

	pygame.time.Clock().tick(30)
	pygame.display.update()

pygame.quit()
