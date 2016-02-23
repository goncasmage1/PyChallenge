import pygame
import random
import sys
from settings import *

class bullet(pygame.sprite.Sprite):
    def __init__(self, x, dir):
        super().__init__()

        self.x = x + 25
        self.y = display_height-60
        self.w = 5
        self.h = 5
        self.backgroundColor = white

        #meio
        if dir == 2:
            self.image = pygame.image.load("Imagens/bullet_mid.png")
            self.rect = self.image.get_rect(center = (self.x+self.w*2,self.y-60))
            self.image.set_colorkey(self.backgroundColor) # pixels in obstacle with this color are transparent in the background
            self.move_pos = ((0, -10))
        #esquerda
        if dir == 1:
            self.image = pygame.image.load("Imagens/bullet_left.png")
            self.rect = self.image.get_rect(center = (self.x+self.w-20,self.y-50))
            self.image.set_colorkey(self.backgroundColor) # pixels in obstacle with this color are transparent in the background
            self.move_pos = ((-10, -10))
        #direita
        if dir == 3:
            self.image = pygame.image.load("Imagens/bullet_right.png")
            self.rect = self.image.get_rect(center = (self.x+self.w+20,self.y-50))
            self.image.set_colorkey(self.backgroundColor) # pixels in obstacle with this color are transparent in the background
            self.move_pos = ((10, -10))


    def pos(self):
        return (self.rect.x, self.rect.y)

    def update(self):
        self.rect = self.rect.move(self.move_pos)

    def __del__(self):
        pass
