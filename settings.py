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

cadeiras_dict = {"CDI I": 2, "AL": 1, "IEI":0, "CDI II":2, "MO":1, "IAC":1}
cadeiras_ref = ["CDI I", "AL", "IEI", "CDI II", "MO", "IAC"]

def msgSurface(text,textSize,textColor,backgroundColor,outlineColor, verticalOffset, horizontaOffset,screen):
    """
    outlineColor for text outter window color,
    vertical and horizontalOffset from original backgroundSurface center coordinates =(0,0) in background Surface
    must receive "main surface" ->special displayed surface in the last argument
    returns textSurface and center of rectangle in the rectangle referential(top-left (0,0))
    """

    width, height = screen.get_size()
    # can also set text object's font in arguments
    ## sets fonts
    textFont = pygame.font.Font('freesansbold.ttf', textSize)
    ## auxiliary function
    titleTextSurf, titleTextRect = makeTextObjs(text,textFont , textColor, black)
    titleTextRect.center = (int(width/2)+ horizontaOffset , int(height/2)+ verticalOffset)          ## set CenterCoords

    pygame.draw.rect(screen, outlineColor,titleTextRect,10) #draw built-in outline
    ## blit -> draws image on top of another
    screen.blit(titleTextSurf, titleTextRect) ## adds image
    return titleTextSurf, titleTextRect.center