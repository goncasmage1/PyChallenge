import pygame
import random
import sys
from settings import *

class power_up(pygame.sprite.Sprite):
    def __init__(self, power, speed):
        super().__init__()
        self.power = power
        self.w = 40
        self.h = 40
        self.x = random.randint(0 + self.w, display_width-self.w)
        self.y = 0-self.h + 5
        self.speed = speed
        if self.power == 1:
            self.image = pygame.image.load("Imagens/shield.png")
            self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))
        elif self.power == 2:
            self.image = pygame.image.load("Imagens/double.png")
            self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))
        elif self.power == 3:
            self.image = pygame.image.load("Imagens/slow.png")
            self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))
        elif self.power == 4:
            self.image = pygame.image.load("Imagens/ammo.png")
            self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))

    def width(self):
        return self.w

    def height(self):
        return self.h

    def pos(self):
        return (self.rect.x, self.rect.y)

    def update(self):
        self.rect.y += self.speed

    def type(self):
        return self.power

    def __del__(self):
        pass
