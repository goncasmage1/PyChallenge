import pygame, pygame.event, time, random
from pygame.locals import *
from player import *
from obstacle import *
from bullet import *
from settings import *
from inputbox import *


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

	aluno = pygame.sprite.GroupSingle(player())
	obstacleGroup = pygame.sprite.Group()
	
	cadeira = [obstacle(random.choice(cadeiras_ref))]
	obstacleGroup.add(cadeira)

	#desenhar o jogador e esperar 1 segundo

	#gameDisplay.fill(white)
	#aluno.draw()
	#pygame.display.update()
	#pygame.time.wait(1000)

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


#escreve texto no ecra a comecar na posicao atribuida
def screen_text(text,x,y,size):
	text_surface = pygame.font.Font("freesansbold.ttf",size).render(text,True, black)
	text_surface_size = text_surface.get_size()
	text_rect = text_surface.get_rect()
	text_rect.center = (x + text_surface_size[0]/2,y)
	gameDisplay.blit(text_surface,text_rect)


#escreve texto no ecra centrado na posicao atribuida
def screen_text_center(text,x,y,size):
	text_surface = pygame.font.Font("freesansbold.ttf",size).render(text,True, black)

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

	if mode:
		screen_text_center(msg, x + w/2, y + h/2, size)


#desenha a barra de vida
def health_bar(vida):
	pygame.draw.rect(gameDisplay, black, (50, 50, 150, 40), 2)
	#pygame.draw.rect(gameDisplay, red, (50, 50, 150*(vida/100), 40))




#FUNCOES DE JOGO
def game_intro():
	global intro

	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)

		#mostra o texto de introducao
		screen_text_center("Trivialidades", display_width/2, display_height/6, 50)

		if intro:
			button("Jogar",display_width/2 - 100,display_height/3,200,100,green,bright_green,40,select_mode,intro)
		if intro:
			button("Sair",display_width/2 - 100,display_height/3*2,200,100,red,bright_red,40,quitgame,intro)
			
		table = open('highscore.txt','r')
		s = table.readline()
		screen_text_center("Highscore: " + s +" ECT'S" , 400, 570, 25)
		table.close
		pygame.display.update()
		clock.tick(15)
	   

def select_mode():

	while selecting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)

		#mostra o texto de introducao
		screen_text_center("Modo de jogo", display_width/2, display_height/8, 50)

		#mostra os botoes
		if selecting:
			button("Student Mode", display_width/3-200, display_height/2, 240, 50, green, bright_green, 30, game_loop, selecting)

		if selecting:
			button("Professor Mode", (display_width/3)*2-50, display_height/2, 240, 50, red, bright_red, 30, god_mode, selecting)

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
		screen_text_center("Nao SobrevivISTe!", display_width/2, display_height/4, 70)
		button("Menu", 600, 500, 240, 50, green, bright_green, 30, game_intro, 0)
		fich = open('highscore.txt','w')
		name = ask(gameDisplay, "Name")
		fich.write(name + str(score))


		pygame.display.update()
		clock.tick(15)

def game_loop():
	global is_god, intro, selecting, GG, side_shooting, score, intro, ultima_cadeira

	intro = False
	selecting = False
	colliding = False
	collide_change = False
	pos_change = 0
	bullets = []
	bulletSprites =pygame.sprite.Group()


	aluno = pygame.sprite.GroupSingle(player())
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

		if GG:
			crash()
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

			if event.type == pygame.KEYDOWN:

				#move o jogador
				if event.key == pygame.K_a:
					pos_change -= 1
				if event.key == pygame.K_d:
					pos_change += 1

				#move as balas
				if event.key == pygame.K_UP:
					bulletA = [bullet(aluno_pos[0], 2)]
					bullets+=bulletA
					bulletSprites.add(bulletA[0])
				if event.key == pygame.K_LEFT and side_shooting:
					bulletA = [bullet(aluno_pos[0]-14, 1)]
					bullets+=bulletA
					bulletSprites.add(bulletA[0])
				if event.key == pygame.K_RIGHT and side_shooting:
					bulletA = [bullet(aluno_pos[0]+10, 3)]
					bullets+=bulletA
					bulletSprites.add(bulletA[0])


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a:
					pos_change += 1
				elif event.key == pygame.K_d:
					pos_change -= 1

		gameDisplay.fill(white)

		obstacleGroup.draw(gameDisplay)
		obstacleGroup.update()

		aluno.draw(gameDisplay)
		aluno.update(pos_change)
		screen_text_center('score: ' +str(score) , 700, 550, 30)

		user = (aluno.sprites())[0]

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

		elif not colliding and collide_change:
			collide_change = False

		colliding = False

		#health_bar(aluno.hp)

		#update
		bulletSprites.update()
		bulletSprites.draw(gameDisplay)
		obstacleGroup.update()
		clock.tick(60)


def crash():
	global score, GG, ultima_cadeira
	screen_text_center(ultima_cadeira + " moeu-te o juizo!", display_width/2, display_height/4, 70)
	screen_text_center("score: " + str(score) + " ECT'S", display_width/2, display_height/2, 40)

	while GG:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
		if GG:
			button("Tentar novamente",150,400,200,50,green,bright_green,20,retry,GG)
		if GG:
			button("Sair",550,400,100,50,red,bright_red,20,quitgame,GG)

		pygame.display.update()
		clock.tick(15)


game_intro()
pygame.quit()
quit()
