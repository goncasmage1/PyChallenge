
import pygame, pygame.event, time, random
from pygame.locals import *
from player import *
from obstacle import *
from power_up import *
from bullet import *
from settings import *

def help_screen():
	global reading
	while reading:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.blit(intro_background, (0, 0))
		screen_text("Comandos:", 50, 110, 30 ,black )
		screen_text("A - esquerda", 50, 140, 30 ,black )
		screen_text("D - direita", 50, 170, 30 ,black )
		screen_text("UP - disparar", 50, 200, 30 ,black )
		screen_text("Sistema das ECT's", 50, 270, 30 ,black )
		screen_text("Deixas a disciplina passar: ", 60, 310, 25 ,black )
		screen_text("Verde:-2 ECT's ", 70, 340, 20 ,black )
		screen_text("Azul:-4 ECT's ", 70, 370, 20 ,black )
		screen_text("Vermelha:+3 ECT's ", 70, 400, 20 ,black )
		screen_text("Atinges a disciplina: ", 60, 440, 25 ,black )
		screen_text("Verde:+2 ECT's ", 70, 470, 20 ,black )
		screen_text("Azul:+10 ECT's ", 70, 500, 20 ,black )
		screen_text("Vermelha:+10 ECT's (mas e imortal) ", 70, 530, 20 ,black )
		screen_text_center("Horario de Duvidas", display_width/2-2, display_height/12-1, 50, black)
		screen_text_center("Horario de Duvidas", display_width/2, display_height/12, 50, white)

		pygame.display.update()
		clock.tick(15)