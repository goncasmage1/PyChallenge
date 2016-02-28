import pygame, pygame.event, time, random, sys
from pygame.locals import *

#ATRIBUICAO DE VALORES
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
orange = (255,215,0)
purple = (255,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
linen = (225,222,173)

cornsilk = (255,255,173)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
bright_orange = (255,140,0)

#COMANDOS DE INICIACAO
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Trivialidades")
clock = pygame.time.Clock()
pygame.mixer.init()

intro_background = pygame.image.load("Imagens/intro_background.png")
game_background = pygame.image.load("Imagens/game_background.png")
new_highscore = pygame.image.load("Imagens/new_record.png")

soundtrack = pygame.mixer.Sound("Sounds/soundtrack.ogg")
game_sound = pygame.mixer.find_channel()
game_sound.queue(soundtrack)

soundtrack_2 = pygame.mixer.Sound("Sounds/soundtrack_2.ogg")
god_sound = pygame.mixer.find_channel()
god_sound.queue(soundtrack_2)
god_sound.stop()

shoot = pygame.mixer.Sound("Sounds/shoot.ogg")
shoot_sound = pygame.mixer.find_channel()
shoot_sound.set_volume(0.5)
shoot_sound.queue(shoot)
shoot_sound.stop()

gasp = pygame.mixer.Sound("Sounds/gasp_sound.ogg")
gasp_sound = pygame.mixer.find_channel()
gasp_sound.set_volume(0.7)
gasp_sound.queue(gasp)
gasp_sound.stop()

death = pygame.mixer.Sound("Sounds/death_sound.ogg")
death_sound = pygame.mixer.find_channel()
death_sound.set_volume(0.7)
death_sound.queue(death)
death_sound.stop()


is_god = False
intro = True
selecting = True
reading = True
GG = False
side_shooting = False
ultima_cadeira = ""
score = 0
pause = False
just_dead = False

cadeiras_dict = {"CDI I": 2, "AL": 1, "IEI":0, "CDI II":2, "MO":1, "IAC":1, "IAED":1, "SO":1, "ES":2, "PO":0, "Comp":2}
cadeiras_ref = ["CDI I", "AL", "IEI", "CDI II", "MO", "IAC", "IAED", "SO", "ES", "PO", "Comp"]


#FUNCOES AUXILIARES

#sai do jogo
def quitgame():
	pygame.quit()
	quit()
	

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


def get_key():
	while 1:
		event = pygame.event.poll()
		if event.type == KEYDOWN:
			return event.key
		else:
			pass

def display_box(screen, message):
	"Print a message in a box in the middle of the screen"
	fontobject = pygame.font.Font(None,40)
	pygame.draw.rect(screen, black,
					(screen.get_width()/2 - screen.get_width()/4-2, screen.get_height() / 2 - 12, screen.get_width()/2 + 4,44))
	pygame.draw.rect(screen, white,
					(screen.get_width() / 2 - screen.get_width() / 4, screen.get_height() / 2 - 10, screen.get_width() / 2,40))

	if len(message) != 0:
		text_size = fontobject.size(message)
		screen.blit(fontobject.render(message, 1, black),
				((screen.get_width()/2 - text_size[0]/2), (screen.get_height()/2 - text_size[1]/2)+10))
	pygame.display.flip()

def ask(screen):

	pygame.font.init()
	current_string = []
	display_box(screen, "".join(current_string))
	while 1:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		inkey = get_key()
		if inkey == K_BACKSPACE:
			current_string = current_string[0:-1]
		elif inkey == K_RETURN:
			break
		elif inkey == K_MINUS:
			current_string.append("_")
		elif inkey <= 127:
			current_string.append(chr(inkey))
		display_box(screen, "".join(current_string))
	return "".join(current_string)


def random_coor(occupied, width):
	previous = 0 + width*2
	random_list = []
	for i in range(len(occupied)):
		random_list += [random.randint(previous-width, occupied[i][0])]
		previous = occupied[i][1]

	return random.choice(random_list)


def ordenar_lista(lista):
	ordena = []
	for i in lista:
		if ordena == []:
			ordena += [i]
		else:
			for j in range(len(ordena)):
				if i[0] < ordena[j][0]:
					ordena = ordena[:j] + [i] + ordena[j:]
					break
				elif i[0] > ordena[-1][0]:
					ordena += [i]

	return ordena