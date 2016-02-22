import pygame
import random
import sys
from settings import *

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = display_width/2
        self.y = display_height - 40
        self.w = 40
        self.h = 40
        self.health = 100
        self.speed = 4
        self.image = pygame.image.load("Imagens/player.png")
        self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))

    def draw(self):
        gameDisplay.blit(self.image, (self.rect.x-self.w/2-10, self.rect.y-self.h/2))

    def pos(self):
        return (self.rect.x, self.rect.y)

    def width(self):
        return self.w

    def height(self):
        return self.h

    def update(self, value):
        self.rect.x += value*self.speed

    def hp(self):
        return self.health
