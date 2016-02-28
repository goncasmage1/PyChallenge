import pygame, pygame.event, time, random
from pygame.locals import *
from player import *
from obstacle import *
from power_up import *
from bullet import *
from settings import *

#FUNCOES

#permite o jogador tentar outra vez
def retry():
	global intro, selecting, colliding, collide_change, GG, score, obstacle_speed,\
	time_change, bullets, bulletSprites, aluno, obstacleGroup, cadeira, pause, pos_change, is_god

	intro = False
	selecting = False
	colliding = False
	collide_change = False
	pause = False
	GG = False
	score = 0
	pos_change = 0
	obstacle_speed = 3
	time_change = 0

	if is_god:
		god_sound.unpause()
	else:
		game_sound.unpause()
	bullets = []
	bulletSprites =pygame.sprite.Group()

	user.reset()
	obstacleGroup.empty()
	
	cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed)]
	obstacleGroup.add(cadeira)

	pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 1500))


def game_intro():
	global selecting
	selecting = False


#comeca o jogo em god mode
def god_mode():
	global is_god, side_shooting
	is_god = True
	side_shooting = True
	game_loop()


#sai do menu de pausa
def unpause():
	global pause
	pause = False


#menu de pausa
def paused():
	global pause

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
						pause = False
		
		#mostra o texto de introducao
		screen_text_center("Pausa",display_width/2,display_height/4,70, black)
		
		button("Continuar",150,450,100,50,green,bright_green,20,unpause, 0)
		button("Novo",350,450,100,50,orange,bright_orange,20,retry, 0)
		button("Sair",550,450,100,50,red,bright_red,20,quitgame, 0)
		
		pygame.display.update()
		clock.tick(15)


def game_intro():
	global intro

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(intro_background, (0, 0))

		#mostra o texto de introducao
		screen_text_center("Trivialidades", display_width/2-2, display_height/6-1, 50, black)
		screen_text_center("Trivialidades", display_width/2, display_height/6, 50, white)

		if intro:
			button("Jogar",display_width/2 - 100,display_height/3,200,100,green,bright_green,40,select_mode,0)
		if intro:
			button("Sair",display_width/2 - 100,display_height/3*2,200,100,red,bright_red,40,quitgame,0)

		table = open('highscore.txt','r')
		s = table.readline()
		screen_text_center("Highscore: " + s +" ECT'S" , 398, 549, 25, black)
		screen_text_center("Highscore: " + s +" ECT'S" , 400, 550, 25, white)
		table.close
		pygame.display.update()
		clock.tick(15)
	   

def select_mode():

	while selecting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(intro_background, (0, 0))

		#mostra o texto de introducao
		screen_text_center("Modo de jogo", display_width/2-2, display_height/8-1, 50, black)
		screen_text_center("Modo de jogo", display_width/2, display_height/8, 50, white)

		#mostra os botoes
		if selecting:
			button("Student Mode", display_width/3-200, display_height/2, 240, 50, green, bright_green, 30, game_loop, 0)

		if selecting:
			button("Professor Mode", (display_width/3)*2-50, display_height/2, 240, 50, red, bright_red, 30, god_mode, 0)

		if selecting:
			button("Voltar", 100, 600, 100, 50, orange, bright_orange, 30, game_intro, 0)

		pygame.display.update()
		clock.tick(15)


def deathscreen(new_score, name, old_score):
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	gameDisplay.blit(new_highscore, (0, 0))
	screen_text_center("Bateste o recorde do " + name + " de " + old_score + " ECT'S!", display_width/2, display_height/4, 35, black)
	screen_text_center("Introduz o teu nome:", display_width/2, display_height/4 + 80, 25, black)
	nome = ask(gameDisplay)
	escreve = open('highscore.txt','w')
	escreve.write(nome + " - " + str(new_score))
	escreve.close()

	pygame.display.update()
	clock.tick(15)

def game_loop():
	global is_god, intro, selecting, GG, side_shooting, score, intro, ultima_cadeira, aluno, user,\
	bullets, bulletSprites, obstacleGroup, cadeira, pause, shooting, obstacle_speed, time_change, pos_change

	intro = False
	selecting = False
	colliding = False
	collide_change = False
	just_dead = False
	pos_change = 0
	shooting = True
	shoot_time = 800
	color_change = black
	obstacle_speed = 3
	speed_change = 0.05
	time_change = 0
	score_string = ""
	name_string = ""

	if is_god:
		game_sound.stop()
		god_sound.play(soundtrack)

	aluno = pygame.sprite.GroupSingle(player())
	user = (aluno.sprites())[0]
	bullets = []
	bulletSprites =pygame.sprite.Group()
	obstacleGroup = pygame.sprite.Group()
	cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed)]
	obstacleGroup.add(cadeira)

	pygame.time.set_timer(USEREVENT + 1, random.randint(1000 - time_change, 1500 - time_change))

	while True:

		pygame.display.update()

		#obtem a posicao do aluno
		for i in aluno:
			aluno_pos = i.pos()

		if just_dead and pygame.key.get_pressed()[pygame.K_a]:
			pos_change = -1

		elif just_dead and pygame.key.get_pressed()[pygame.K_d]:
			pos_change = 1

		#EVENTOS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			#evento do cronometro
			if event.type == USEREVENT + 1:
				cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed)]
				obstacleGroup.add(cadeira)					
				pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 1500))

			if event.type == USEREVENT + 2:
				shooting = True

			if event.type == USEREVENT + 3:
				color_change = black
				if is_god:
					god_sound.pause()
				else:
					game_sound.unpause()

			if event.type == pygame.KEYDOWN:

				#move o jogador
				if event.key == pygame.K_a:
					pos_change -= 1
				if event.key == pygame.K_d:
					pos_change += 1

				if event.key == pygame.K_p:
					pause = True
					paused()

				#move as balas
				if event.key == pygame.K_UP:
					if not is_god:
						if shooting:
							pygame.time.set_timer(USEREVENT + 2, shoot_time)
							shooting = False
							bulletA = [bullet(aluno_pos[0], 2)]
							bullets+=bulletA
							bulletSprites.add(bulletA[0])
					else:
						bulletA = [bullet(aluno_pos[0], 2)]
						bullets+=bulletA
						bulletSprites.add(bulletA[0])

				if event.key == pygame.K_LEFT and side_shooting:
					if not is_god:
						if shooting:
							pygame.time.set_timer(USEREVENT + 2, shoot_time)
							shooting = False
							bulletA = [bullet(aluno_pos[0], 1)]
							bullets+=bulletA
							bulletSprites.add(bulletA[0])
					else:
						bulletA = [bullet(aluno_pos[0], 1)]
						bullets+=bulletA
						bulletSprites.add(bulletA[0])

				if event.key == pygame.K_RIGHT and side_shooting:
					if not is_god:
						if shooting:
							pygame.time.set_timer(USEREVENT + 2, shoot_time)
							shooting = False
							bulletA = [bullet(aluno_pos[0], 3)]
							bullets+=bulletA
							bulletSprites.add(bulletA[0])
					else:
						bulletA = [bullet(aluno_pos[0], 3)]
						bullets+=bulletA
						bulletSprites.add(bulletA[0])

			if event.type == pygame.KEYUP:
					
				if event.key == pygame.K_a:
					pos_change += 1
				elif event.key == pygame.K_d:
					pos_change -= 1

		gameDisplay.blit(game_background, (0, 0))

		obstacleGroup.draw(gameDisplay)
		obstacleGroup.update()

		aluno.draw(gameDisplay)
		aluno.update(pos_change)

		#detecao de colisoes
		for obstaculo in obstacleGroup:

			if pygame.sprite.collide_rect(user, obstaculo):
				if obstaculo.dif() != 0:
					colliding = True

				if is_god:
					score += 20
					obstacleGroup.remove(obstaculo)
				else:
					if user.is_dead():
						user.update_hp(3)
						ultima_cadeira = obstaculo.nome()
						if is_god:
							god_sound.pause()
						else:
							game_sound.pause()
						death_sound.play(death)
						GG = True
						break

			if pygame.sprite.spritecollideany(obstaculo, bulletSprites):
				if obstaculo.dif() == 0:
					if is_god:
						score += 40
					else:
						score += 2
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					obstacle_speed += speed_change
					time_change += 25

				elif obstaculo.dif() == 1:
					if is_god:
						score += 80
					else:
						score += 10
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					obstacle_speed += speed_change
					time_change += 25

				elif obstaculo.dif() == 2:
					if is_god:
						score += 150
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					else:
						score += 10
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, False, True)
					obstacle_speed += speed_change
					time_change += 25

			#quando o jogador ultrapassa um obstaculo
			if obstaculo.pos()[1] > display_height + (obstaculo.height()):
				obstacle_speed += speed_change

				if obstaculo.dif() == 0:
					score -= 2
				elif obstaculo.dif() == 1:
					score -= 4
				#elif obstaculo.dif() == 2:
					#score += 3
				obstacleGroup.remove(obstaculo)

		#quando o jogador e atingido por um obstaculo
		if colliding and not collide_change:
			collide_change = True
			user.update_hp(-1)
			if user.hp() != 0:
				gasp_sound.play(gasp)
			pygame.time.set_timer(USEREVENT + 3, 500)
			color_change = bright_red

		#mecanismo de tranca
		elif not colliding and collide_change:
			collide_change = False

		colliding = False
		just_dead = False

		#se o jogador perde
		if GG:
			just_dead = True
			#verifica se bateu o highscore
			table = open('highscore.txt','r')
			s = table.readline()
			i = -1
			while s[i].isdigit():
				score_string = s[i] + score_string
				i-=1
			
			i = 0
			while s[i] != "-":
				name_string += s[i]
				i+=1

			name_string = name_string[:-1]
			i = 0
			table.close

			if score > eval(score_string):
				deathscreen(score, name_string, score_string)
			else:
				crash()
				score_string = ""
				name_string = ""

		else:
			screen_text_center("ECT'S: " + str(score) , 700, 20, 20, black)
			screen_text_center("Paciencia: " +str(user.hp()) , 100, 20, 20, color_change)

		#update
		bulletSprites.update()
		bulletSprites.draw(gameDisplay)
		obstacleGroup.update()
		clock.tick(60)


def crash():
	global score, GG, ultima_cadeira
	screen_text_center(ultima_cadeira + " moeu-te o juizo!", display_width/2, display_height/8+50, 70, black)
	screen_text_center("ECT'S: " + str(score), display_width/2, display_height/3+40, 40, black)

	while GG:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
		if GG:
			button("Tentar novamente",150,400,200,50,green,bright_green,20,retry,0)
		if GG:
			button("Sair",550,400,100,50,red,bright_red,20,quitgame,0)

		pygame.display.update()
		clock.tick(15)


game_intro()
pygame.quit()
quit()
