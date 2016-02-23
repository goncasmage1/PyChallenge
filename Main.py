import pygame, pygame.event, time, random
from pygame.locals import *
from player import *
from obstacle import *
from bullet import *
from settings import *


"""
PROBLEMAS:

butoes nao funcionam 100%
colliderect nao funciona
health_bar() "nao suporta divisao com metodos, so que o metodo e suposto ser um numero..."
"""

"""
TO DO:

arranjar uma maneira estavel de gerar mais cadeiras
"""
#FUNCOES "AUXILIARES"

#sai do jogo
def quitgame():
	pygame.quit()
	quit()


#permite o jogador tentar outra vez
def retry():
	global GG
	GG = False
	game_loop()


def game_intro():
	global selecting
	selecting = False


#comeca o jogo em god mode
def god_mode():
	global is_god, side_shooting
	is_god = True
	side_shooting = True
	game_loop()


def is_on_screen(coor):
	if coor[0] < 0 or coor[0] > display_width or coor[1] < 0 or coor[1] > display_height:
		return False
	else:
		return True

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
	global GG
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	#se a funcao receber o ultimo argumento
	if mode != 0:
		if x + w > mouse[0] > x and y + h > mouse[1] > y:
			pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
			if click[0] == 1 and action != None:
				action(mode)
		else:
			pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

	#se a funcao nao receber o ultimo argumento
	else:
		if x + w > mouse[0] > x and y + h > mouse[1] > y:
			pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
			if click[0] == 1 and action != None:
				action()
		else:
			pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

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
			button("Jogar",display_width/2 - 100,display_height/3,200,100,green,bright_green,40,select_mode,0)
		if intro:
			button("Sair",display_width/2 - 100,display_height/3*2,200,100,red,bright_red,40,quitgame,0)

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
			button("Student Mode", display_width/3-200, display_height/2, 240, 50, green, bright_green, 30, game_loop, 0)

		if selecting:
			button("Professor Mode", (display_width/3)*2-50, display_height/2, 240, 50, red, bright_red, 30, god_mode, 0)

		if selecting:
			button("Voltar", 100, 600, 100, 50, orange, bright_orange, 30, game_intro, 0)

		pygame.display.update()
		clock.tick(15)


def game_loop():
	global is_god, intro, selecting, GG, side_shooting, score, intro

	intro = False
	selecting = False
	colliding = False
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

	while not GG:
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

		user = (aluno.sprites())[0]

		#detecao de colisoes
		for obstaculo in obstacleGroup:
			print(user.hp())

			if pygame.sprite.collide_rect(user, obstaculo):
				colliding = True

				if is_god:
					score += 20
					obstacleGroup.remove(obstaculo)
				else:
					if user.is_dead():
						user.update_hp(3)
						GG = True
						break

					elif not colliding:
						print(colliding)
						user.update_hp(-1)

			elif not colliding:
				print("no")
				not_colliding = True

			if pygame.sprite.spritecollideany(obstaculo, bulletSprites):
				if obstaculo.dif() == 0:
					if is_god:
						score += 40
					else:
						score += 5
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

		#health_bar(aluno.hp)

		#update
		bulletSprites.update()
		bulletSprites.draw(gameDisplay)
		obstacleGroup.update()
		clock.tick(60)


def crash():
	global score
	screen_text_center("Nao SobrevivISTe!", display_width/2, display_height/4, 70)
	screen_text_center("score: " + str(score), display_width/2, display_height/2, 40)

	while GG:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
		if GG:
			button("Tentar novamente",150,450,200,50,green,bright_green,20,retry,0)
		if GG:
			button("Sair",550,450,100,50,red,bright_red,20,quitgame,0)

		if GG:
			pygame.display.update()
			clock.tick(15)


game_intro()
crash()
pygame.quit()
quit()
