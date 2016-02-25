import pygame
import random
import sys
from settings import *

class obstacle(pygame.sprite.Sprite):
    def __init__(self, power):
        super().__init__()
        self.power = power
        self.w = 40
        self.h = 40
        self.x = random.randint(0 + self.w, display_width-self.w)
        self.y = 0-self.h + 5
        self.speed = 4
        self.image = pygame.image.load("Imagens/player.png")
        self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))

    def update(self):
        self.rect.y += self.speed

    def __del__(self):
        pass
