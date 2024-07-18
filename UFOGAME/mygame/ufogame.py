import pygame 
from sys import exit
from random import randint, choice, randrange

#Player Class
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/dog_run.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/player/dog_run2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/dog_jump.png').convert_alpha()
		
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,320))
		self.gravity = 0
	
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.1)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()
		if keys[pygame.K_RIGHT] and self.rect.bottom >= 300:
			self.rect.x += 4
		if keys[pygame.K_LEFT] and self.rect.bottom >= 300:
			self.rect.x -= 4
					

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 320:
			self.rect.bottom = 320

	def animation_state(self):
		if self.rect.bottom < 320: 
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'cat':
			cat_1 = pygame.image.load('graphics/cat.png').convert_alpha()
			cat_2 = pygame.image.load('graphics/cat_2.png').convert_alpha()
			cat_3 = pygame.image.load('graphics/cat_3.png').convert_alpha()
			cat_4 = pygame.image.load('graphics/cat_4.png').convert_alpha()
			self.frames = [cat_1,cat_2,cat_3,cat_4]
			y_pos = 170
		
			
		if type == 'rover':
			rover = pygame.image.load('graphics/rover.png').convert_alpha()
			rover_2 = pygame.image.load('graphics/rover2.png').convert_alpha()
			self.frames = [rover,rover_2]
			y_pos  = 300

		elif type == 'ufo':
			ufo = pygame.image.load('graphics/ufo.png').convert_alpha()
			ufo_2 = pygame.image.load('graphics/ufo_2.png').convert_alpha()
			self.frames = [ufo,ufo_2]
			y_pos = 270

		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1 
		if self.animation_index >= len(self.frames): self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def update(self):
		self.animation_state()
		self.rect.x -= 8
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}',False,(88, 142, 214))
	score_rect = score_surf.get_rect(center = (400,50))
	screen.blit(score_surf,score_rect)
	return current_time

def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return False
	else: return True

#Initialize the game window/screen
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Space Cats Attack')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.4)
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky2.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/Player/dog_jump.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Space Cats Attack',False,(88, 142, 214))
game_name_rect = game_name.get_rect(center = (400,50))

game_message = test_font.render('Press space to run',False,(88, 142, 214))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

		#Need to randomize this better
		if game_active:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice(['ufo','ufo','cat','cat','rover','rover'])))
		
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				game_active = True
				start_time = int(pygame.time.get_ticks() / 1000)


	if game_active:
		screen.blit(sky_surface,(0,0))
		screen.blit(ground_surface,(0,280))
		score = display_score()
		
		player.draw(screen)
		player.update()

		obstacle_group.draw(screen)
		obstacle_group.update()

		game_active = collision_sprite()
		
	else:
		screen.blit(sky_surface,(0,0))
		screen.blit(player_stand,player_stand_rect)

		score_message = test_font.render(f'Your score: {score}',False,(120,200,175))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: screen.blit(game_message,game_message_rect)
		else: screen.blit(score_message,score_message_rect)

	pygame.display.update()
	clock.tick(60)