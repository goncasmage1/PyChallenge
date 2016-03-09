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
	time_change, bullets, bulletSprites, aluno, obstacleGroup, cadeira, pause, pos_change,\
	is_god, just_dead, power_up_change, powers, event_4, event_6

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
	event_4 = False
	event_6 = False
	power_up_change = random.randint(5, 9)

	if just_dead and pygame.key.get_pressed()[pygame.K_a]:
		just_dead = False
		pos_change = -1

	elif just_dead and pygame.key.get_pressed()[pygame.K_d]:
		just_dead = False
		pos_change = 1

	if is_god:
		god_sound.unpause()
	else:
		game_sound.unpause()
	bullets = []
	bulletSprites =pygame.sprite.Group()

	user.reset()
	obstacleGroup.empty()
	powers.empty()
	
	cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed, user.slow_time())]
	obstacleGroup.add(cadeira)

	pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 1500))



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


#sai do menu de select
def unselect():
	global selecting
	selecting = False


#sai do menu de duvidas
def unread():
	global reading
	reading = False

#menu de pausa
def paused():
	global pause, just_dead

	just_dead = True

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
			button("Jogar",display_width/2 - 100,display_height/3,200,100,linen,cornsilk,40,select_mode,0)
		if intro:
			button("Sair",display_width/2 - 100,display_height/3*2,200,100,linen,cornsilk,40,quitgame,0)
		if intro:
			button("Duvidas",display_width - 220, display_height/2 + 20,200,50,linen,cornsilk,40,help_screen,0)

		table = open('highscore.txt','r')
		s = table.readline()
		screen_text_center("Highscore: " + s +" ECT'S" , 398, 549, 25, black)
		screen_text_center("Highscore: " + s +" ECT'S" , 400, 550, 25, white)
		table.close
		pygame.display.update()
		clock.tick(15)

def select_mode():
	global selecting
	selecting = True
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
			button("Voltar", 100, display_height-100, 100, 50, orange, bright_orange, 30, unselect, 0)

		pygame.display.update()
		clock.tick(15)

def help_screen():
	global reading
	while reading:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(intro_background, (0, 0))
		screen_text("Comandos:", 49, 109, 30 ,black )
		screen_text("Comandos:", 50, 110, 30 ,white )
		screen_text("A - esquerda", 59, 136, 26 ,black )
		screen_text("A - esquerda", 60, 137, 26 ,white )
		screen_text("D - direita", 59, 163, 26 ,black )
		screen_text("D - direita", 60, 164, 26 ,white )
		screen_text("SETAS - disparar", 59, 190, 26 ,black )
		screen_text("SETAS - disparar", 60, 191, 26 ,white )
		screen_text("P - pausa", 59, 217, 26 ,black )
		screen_text("P - pausa", 60, 218, 26 ,white )
		screen_text("Sistema dos ECT's", 59, 269, 30 ,black )
		screen_text("Sistema dos ECT's", 60, 270, 30 ,white )
		screen_text("Deixas a disciplina passar: ", 69, 309, 25 ,black )
		screen_text("Deixas a disciplina passar: ", 70, 310, 25 ,white )
		screen_text("Verde: - 2 ECT's ", 79, 339, 20 ,black )
		screen_text("Verde: - 2 ECT's ", 80, 340, 20 ,white )
		screen_text("Azul: - 4 ECT's ", 79, 369, 20 ,black )
		screen_text("Azul: - 4 ECT's ", 80, 370, 20 ,white )
		screen_text("Atinges a disciplina: ", 69, 439, 25 ,black )
		screen_text("Atinges a disciplina: ", 70, 440, 25 ,white )
		screen_text("Verde: + 2 ECT's ", 79, 469, 20 ,black )
		screen_text("Verde: + 2 ECT's ", 80, 470, 20 ,white )
		screen_text("Azul: + 5 ECT's ", 79, 499, 20 ,black )
		screen_text("Azul: + 5 ECT's ", 80, 500, 20 ,white )
		screen_text("Vermelha: + 10 ECT's (mas e imortal) ", 79, 529, 20 ,black )
		screen_text("Vermelha: + 10 ECT's (mas e imortal) ", 80, 530, 20 ,white )
		screen_text_center("Horario de Duvidas", display_width/2-2, display_height/12-1, 50, black)
		screen_text_center("Horario de Duvidas", display_width/2, display_height/12, 50, white)
		button("Voltar",550,450,150,50,orange,bright_orange,40,game_intro,0)

		pygame.display.update()
		clock.tick(15)

def deathscreen(new_score, name, old_score):
	linen
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
	bullets, bulletSprites, obstacleGroup, cadeira, pause, shooting, obstacle_speed, time_change, pos_change,\
	power_up_change, powers

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
	event_4 = False
	event_6 = False
	score_string = ""
	name_string = ""

	shoot_sound.set_volume(0.4)

	if is_god:
		game_sound.stop()
		god_sound.play(soundtrack_2)

	aluno = pygame.sprite.GroupSingle(player())
	user = (aluno.sprites())[0]
	bullets = []
	bulletSprites =pygame.sprite.Group()
	obstacleGroup = pygame.sprite.Group()
	powers = pygame.sprite.Group()
	cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed, user.slow_time())]
	obstacleGroup.add(cadeira)

	pygame.time.set_timer(USEREVENT + 1, random.randint(1000 - time_change, 1500 - time_change))
	power_up_change = random.randint(5, 9)

	while True:

		pygame.display.update()

		if not pygame.mixer.get_busy():
			if is_god:
				god_sound.play(soundtrack_2)
			else:
				game_sound.play(soundtrack)

		#obtem a posicao do aluno
		for i in aluno:
			aluno_pos = i.pos()

		#criacao de cronometros
		if user.score_change() != 1:
			pygame.time.set_timer(USEREVENT + 5, 7000)

		#EVENTOS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			#eventos do cronometro
			if event.type == USEREVENT + 1:
				print(user.slow_time())
				cadeira = [obstacle(random.choice(cadeiras_ref), obstacle_speed, user.slow_time())]
				obstacleGroup.add(cadeira)

				if not is_god:
					if power_up_change <= 0:
						power_up_change = random.randint(5, 9)
						power = [power_up(random.randint(1, 4), obstacle_speed)]
						powers.add(power)

				pygame.time.set_timer(USEREVENT + 1, random.randint(1000-time_change, 1500-time_change))

			if event.type == USEREVENT + 2:
				shooting = True

			if event.type == USEREVENT + 3:
				color_change = black
				if is_god:
					god_sound.unpause()
				else:
					game_sound.unpause()

			if event.type == USEREVENT + 4 and event_4:
				user.end_slow()
				print("lol")
				event_4 = False
				for obstaculo in obstacleGroup:
					obstaculo.speed_change(obstaculo.speed*2)

			if event.type == USEREVENT + 5:
				user.end_score()

			if event.type == USEREVENT + 6 and event_6:
				event_6 = False
				side_shooting = False

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
							shoot_sound.play(shoot)
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

		powers.draw(gameDisplay)
		powers.update()

		aluno.draw(gameDisplay)
		aluno.update(pos_change)

		if just_dead:
			just_dead = False

		#detecao de colisoes (obstaculo)
		for obstaculo in obstacleGroup:

			#colisao com o jogador
			if pygame.sprite.collide_rect(user, obstaculo):
				if obstaculo.dif() != 0:
					if user.shield():
						score += 5 * user.score_change()
						obstacleGroup.remove(obstaculo)
						user.end_shield()
					else:
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

			#colisao com as balas
			if pygame.sprite.spritecollideany(obstaculo, bulletSprites):
				if obstaculo.dif() == 0:
					if is_god:
						score += 40
					else:
						score += 2 * user.score_change()
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					power_up_change -= 1
					if obstacle_speed <= 4.5:
						obstacle_speed += speed_change
					time_change += 25

				elif obstaculo.dif() == 1:
					if is_god:
						score += 80
					else:
						score += 5 * user.score_change()
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					power_up_change -= 1
					if obstacle_speed <= 4.5:
						obstacle_speed += speed_change
					time_change += 25

				elif obstaculo.dif() == 2:
					if is_god:
						power_up_change -= 1
						score += 150
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					else:
						score += 10 * user.score_change()
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, False, True)
					if obstacle_speed <= 4.5:
						obstacle_speed += speed_change
					time_change += 25

			#quando o jogador ultrapassa um obstaculo
			if obstaculo.pos()[1] > display_height + (obstaculo.height()):
				if obstacle_speed <= 4.5:
						obstacle_speed += speed_change
				power_up_change -= 1

				if obstaculo.dif() == 0:
					if not is_god:
						score -= 2
				elif obstaculo.dif() == 1:
					if not is_god:
						score -= 4
				obstacleGroup.remove(obstaculo)

		#detecao de colisoes (power_up)
		for power in powers:
			if pygame.sprite.spritecollideany(power, bulletSprites):
				pygame.sprite.groupcollide(powers, bulletSprites, True, True)
				power_up_change = random.randint(5, 9)

			if pygame.sprite.collide_rect(user, power):
				user.apply(power.type())
				powers.remove(power)
				power_up_change = random.randint(5, 9)

				if user.slow_time() and not event_4:
					event_4 = True
					for obstaculo in obstacleGroup:
						obstaculo.speed_change(obstaculo.speed/2)
					pygame.time.set_timer(USEREVENT + 4, 5000)

				if power.type() == 4 and not event_6:
					event_6 = True
					side_shooting = True
					pygame.time.set_timer(USEREVENT + 6, 10000)

			if power.pos()[1] > display_height + (power.height()):
				powers.remove(power)
				power_up_change = random.randint(5, 9)


		#quando o jogador e atingido por um obstaculo
		if colliding and not collide_change:
			collide_change = True
			if not is_god:
				user.update_hp(-1)
				if user.hp() != 0:
					gasp_sound.play(gasp)
					color_change = bright_red
			pygame.time.set_timer(USEREVENT + 3, 500)

		#mecanismo de tranca
		elif not colliding and collide_change:
			user.end_shield()
			collide_change = False

		colliding = False

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
	global score, GG, ultima_cadeira, just_dead
	screen_text_center(ultima_cadeira + " moeu-te o juizo!", display_width/2, display_height/8+50, 70, black)
	screen_text_center("ECT'S: " + str(score), display_width/2, display_height/3+40, 40, black)

	just_dead = True

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
