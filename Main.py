import pygame, pygame.event, time, random
from pygame.locals import *
from player import *
from obstacle import *
from bullet import *
from settings import *
from inputbox import *

# comentario desnecessario


#FUNCOES "AUXILIARES"

#sai do jogo
def quitgame():
	pygame.quit()
	quit()


#permite o jogador tentar outra vez
def retry():
	global intro, selecting, colliding, collide_change, pos_change, GG, score, bullets, bulletSprites, aluno, obstacleGroup, cadeira

	intro = False
	selecting = False
	colliding = False
	collide_change = False
	pos_change = 0
	GG = False
	score = 0
	bullets = []
	bulletSprites =pygame.sprite.Group()

	user.reset()
	obstacleGroup.empty()
	
	cadeira = [obstacle(random.choice(cadeiras_ref))]
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
		button("Sair",550,450,100,50,red,bright_red,20,quitgame, 0)
		
		pygame.display.update()
		clock.tick(15)


#escreve texto no ecra a comecar na posicao atribuida
def screen_text(text,x,y,size, color):
	text_surface = pygame.font.Font("freesansbold.ttf",size).render(text,True, color)
	text_surface_size = text_surface.get_size()
	text_rect = text_surface.get_rect()
	text_rect.center = (x + text_surface_size[0]/2,y)
	gameDisplay.blit(text_surface,text_rect)


#escreve texto no ecra centrado na posicao atribuida
def screen_text_center(text,x,y,size, color):
	text_surface = pygame.font.Font("freesansbold.ttf",size).render(text,True, color)

	text_rect = text_surface.get_rect()
	text_rect.center = (x,y)
	gameDisplay.blit(text_surface,text_rect)

#desenha um botao com uma acao associada
def button(msg,x,y,w,h,ic,ac,size,action,mode):

	global intro, selecting, GG

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
		if click[0] == 1 and action != None:
			action()

	else:
		pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

	screen_text_center(msg, x + w/2, y + h/2, size, black)





#FUNCOES DE JOGO
def game_intro():
	global intro

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.blit(intro_background, (0, 0))

		#mostra o texto de introducao
		screen_text_center("Trivialidades", display_width/2, display_height/6, 50, white)

		if intro:
			button("Jogar",display_width/2 - 100,display_height/3,200,100,green,bright_green,40,select_mode,0)
		if intro:
			button("Sair",display_width/2 - 100,display_height/3*2,200,100,red,bright_red,40,quitgame,0)
			
		table = open('highscore.txt','r')
		s = table.readline()
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


def deathscreen():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(Red)
		screen_text_center("Nao SobrevivISTe!", display_width/2, display_height/4, 70, white)
		button("Menu", 600, 500, 240, 50, green, bright_green, 30, game_intro, 0)
		name = ask(gameDisplay, "Name")
		le = open('highscore.txt','r')
		esq = open('highscore.txt','w')
		s = le.readline()
		name = ask(gameDisplay, "Name")
		for x in range(-1,-len(s),-1):
			if s[x] == ' ':
				nbr = s[x+1:]
			if eval(nbr) < score:
				esq.write(name + str(score))
		le.close()
		esq.close()

		pygame.display.update()
		clock.tick(15)

def game_loop():
	global is_god, intro, selecting, GG, side_shooting, score, intro, ultima_cadeira, aluno, user, bullets, bulletSprites, obstacleGroup, cadeira, pause, shooting

	intro = False
	selecting = False
	colliding = False
	collide_change = False
	pos_change = 0
	shooting = True
	shoot_time = 800
	color_change = black
	
	aluno = pygame.sprite.GroupSingle(player())
	user = (aluno.sprites())[0]
	bullets = []
	bulletSprites =pygame.sprite.Group()
	obstacleGroup = pygame.sprite.Group()
	cadeira = [obstacle(random.choice(cadeiras_ref))]
	obstacleGroup.add(cadeira)

	#desenhar o jogador e esperar 1 segundo

	#gameDisplay.fill(white)
	#aluno.draw()
	#pygame.display.update()
	#pygame.time.wait(1000)

	pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 1500))

	while True:

		pygame.display.update()

		#obtem a posicao do aluno
		for i in aluno:
			aluno_pos = i.pos()

		#EVENTOS
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			#evento do cronometro
			if event.type == USEREVENT + 1:
				cadeira = [obstacle(random.choice(cadeiras_ref))]
				obstacleGroup.add(cadeira)
				pygame.time.set_timer(USEREVENT + 1, random.randint(1000, 1500))

			if event.type == USEREVENT + 2:
				shooting = True

			if event.type == USEREVENT + 3:
				color_change = black

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
		screen_text_center("ECT'S: " + str(score) , 700, 20, 20, black)
		screen_text_center("Paciencia: " +str(user.hp()) , 100, 20, 20, color_change)

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
						GG = True
						break

			if pygame.sprite.spritecollideany(obstaculo, bulletSprites):
				if obstaculo.dif() == 0:
					if is_god:
						score += 40
					else:
						score += 2
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
				elif obstaculo.dif() == 1:
					if is_god:
						score += 80
					else:
						score += 10
					pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
				elif obstaculo.dif() == 2:
					if is_god:
						score += 150
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, True, True)
					else:
						pygame.sprite.groupcollide(obstacleGroup, bulletSprites, False, True)

			if obstaculo.pos()[1] > display_height + (obstaculo.height()):
				if obstaculo.dif() == 0:
					score += 1
				elif obstaculo.dif() == 1:
					score += 2
				elif obstaculo.dif() == 2:
					score += 3
				obstacleGroup.remove(obstaculo)

		if colliding and not collide_change:
			collide_change = True
			user.update_hp(-1)
			pygame.time.set_timer(USEREVENT + 3, 500)
			color_change = bright_red


		elif not colliding and collide_change:
			collide_change = False

		colliding = False

		if GG:
			crash()

		#update
		bulletSprites.update()
		bulletSprites.draw(gameDisplay)
		obstacleGroup.update()
		clock.tick(60)


def crash():
	global score, GG, ultima_cadeira
	screen_text_center(ultima_cadeira + " moeu-te o juizo!", display_width/2, display_height/8+50, 70, black)
	screen_text_center("score: " + str(score) + " ECT'S", display_width/2, display_height/3+40, 40, black)

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
