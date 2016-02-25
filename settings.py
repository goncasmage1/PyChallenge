import pygame
import random
import sys

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

bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0,0,255)
bright_orange = (255,140,0)

#COMANDOS DE INICIACAO
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Trivialidades")
clock = pygame.time.Clock()

intro_background = pygame.image.load("Imagens/intro_background.png")
game_background = pygame.image.load("Imagens/game_background.png")

is_god = False
intro = True
selecting = True
GG = False
side_shooting = False
ultima_cadeira = ""
score = 0
pause = False

cadeiras_dict = {"CDI I": 2, "AL": 1, "IEI":0, "CDI II":2, "MO":1, "IAC":1, "IAED":1, "SO":1, "ES":2, "PO":0, "Comp":2}
cadeiras_ref = ["CDI I", "AL", "IEI", "CDI II", "MO", "IAC", "IAED", "SO", "ES", "PO", "Comp"]