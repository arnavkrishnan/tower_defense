import pygame
import math
pygame.init()

#create screen
grid_size = 80 #map is grid base,size of the map row X col
num_row = 8
num_col = 12
screen_width = grid_size*num_col
screen_height = grid_size*num_row
tower_selected = int(0)
money = 100
tower_cost = 50
enemy_price = 10
tower_list = []
new_tower = []
bullet_list = []
health = 20
firing_rate  = 30
speed = 1
interval = 2000
pi = 3.14159265359

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

bullet = pygame.image.load('images/towerDefense_tile298.png')

def draw_text(text,size, cx, cy):
	font = pygame.font.Font('freesansbold.ttf',size)
	bigtext = font.render(text, True, (255,255,255))
	textrect = bigtext.get_rect()
	textrect.center = (cx,cy)
	screen.blit(bigtext, textrect)

def draw_bullet (a_bullet):
	firing = a_bullet[0]
	firing = pygame.transform.rotate(firing, a_bullet[3])
	rect = firing.get_rect()
	a_bullet[1] += -10*math.sin(pi*a_bullet[3]/180.0)
	a_bullet[2] += -10*math.cos(pi*a_bullet[3]/180.0)
	a_bullet[4] -= 1
	rect.center = (a_bullet[1], a_bullet[2])
	screen.blit(firing, rect)

def collision(cx, cy, r, rx, ry, d):
	if abs(cx-rx) < r+d and abs(cy-ry) < r+d:
		return True
	else:
		return False


def draw_tower(tower):
	tower_base = tower[0]
	tower_gun = tower[1]
	x = tower[2]
	y = tower[3]
	a = tower[4]
	tower_gun = pygame.transform.rotate(tower_gun, a)
	rect = tower_gun.get_rect()
	rect.center = (x+int(grid_size/2), y+int(grid_size/2))
	screen.blit(tower_base, (x, y))
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

def move_to(object, object2, cx, cy, goal_x, goal_y, num_steps):
	rect = object.get_rect()
	cx += (goal_x - cx)/num_steps
	cy += (goal_y - cy)/num_steps
	rect.center = (cx, cy)
	#screen.blit(enemy_person, rect)
	screen.blit(object, rect)
	screen.blit(object2, rect)
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
			num_steps = 30/speed
			goal_y = path[i][0]*grid_size+grid_size/2
			goal_x = path[i][1]*grid_size+grid_size/2
			direction = 0
			if goal_y > cy+1:
				direction = -90
			if goal_y < cy-1:
				direction = 90
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
	acannon = pygame.transform.rotate(cannon, direction)
	cx, cy = move_to(atank, acannon, cx, cy, goal_x, goal_y, num_steps)
	enemy[1] = num_steps
	enemy[2] = cx
	enemy[3] = cy
	return True


running = True
enemy_list = []
last_time = 0
while running:
	draw_map()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			grid_x = pos[0]//grid_size
			grid_y = pos[1]//grid_size
			if ((grid_x == 5 or grid_x == 6) and grid_y == 7):
				tower_selected = 1
			else:
				for tower in tower_list:
					if grid_x == tower[2]//grid_size and grid_y == tower[3]//grid_size:
						tower[4] += 45
						break
		elif event.type == pygame.MOUSEBUTTONUP and tower_selected == 1 and money >= tower_cost:
			pos = pygame.mouse.get_pos()
			grid_x = pos[0]//grid_size
			grid_y = pos[1]//grid_size
			if map[grid_y][grid_x] == 2:
				new_tower = [tower_base, tower_gun, grid_x*grid_size, grid_y*grid_size, 0, 0]
				tower_list.append(new_tower)
				money -= tower_cost
				draw_tower(new_tower)
				tower_selected = 0

	mouse_pressed = pygame.mouse.get_pressed()
	if mouse_pressed[0] == 1 and tower_selected == 1:
		pos = pygame.mouse.get_pos()
		tower = [tower_base, tower_gun, pos[0]-grid_size//2, pos[1]-grid_size//2, 0]
		draw_tower(tower)

	if pygame.time.get_ticks() - last_time > interval:
		enemy_list.append([tank, 0, -40, 520, 0, 0, 0, -1])
		last_time = pygame.time.get_ticks()

	tower_icon = [tower_base, tower_gun, 5.5*grid_size, 7*grid_size, 0]
	draw_tower(tower_icon)


	for enemy in enemy_list:
		if not draw_enemy(enemy):
			enemy_list.remove(enemy)
			health -= 1

	for a_bullet in bullet_list:
		draw_bullet(a_bullet)
		if a_bullet[4] <= 0:
			bullet_list.remove(a_bullet)
		else:
			for enemy in enemy_list:
				if collision(a_bullet[1], a_bullet[2], a_bullet[0].get_width()//4, enemy[2], enemy[3], enemy[0].get_width()//8):
					enemy_list.remove(enemy)
					bullet_list.remove(a_bullet)
					money += enemy_price
					break
	draw_text("$"+str(money),30, 40, 30) # money
	draw_text("health: "+str(health),30, 880, 30) # health

	for tower in tower_list:
		draw_tower(tower)
		if tower[5] == 0:
			x = tower[2]+grid_size//2-(grid_size//2)*math.sin(pi*tower[4]/180.0)
			y = tower[3]+grid_size//2-(grid_size//2)*math.cos(pi*tower[4]/180.0)
			a_bullet = [bullet, x, y, tower[4], 10]
			bullet_list.append(a_bullet)
		tower[5] = (tower[5]+1)%firing_rate



	pygame.time.Clock().tick(30)
	pygame.display.update()

pygame.quit()
