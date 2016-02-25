import pygame
import random
import sys
from settings import *

class obstacle(pygame.sprite.Sprite):
    def __init__(self, nome, speed):
        super().__init__()
        self.type = type
        self.w = 40
        self.h = 40

        font = pygame.font.Font(None, 30 + (self.difficulty)*5)
        text = font.render(self.name, 0, black)
        text_rect = text.get_rect()
        text_rect.center = ((self.w)/2,(self.h)/2)
        self.x = random.randint(0 + self.w, display_width-self.w)
        self.y = 0-self.h + 5
        self.surface = pygame.Surface((self.w, self.h))
        self.surface.fill(self.color)
        self.surface.blit(text, text_rect)
        self.image = self.surface
        self.rect = self.image.get_rect(center = (self.x-self.w/2,self.y-self.h/2))
        print (self.rect.size)
        self.speed = speed

    def dif(self):
        return self.difficulty

    def is_destructable(self):
        if self.difficulty == 2:
            return False
        else:
            return True

    def nome(self):
        return self.name

    def width(self):
        return self.w

    def height(self):
        return self.h

    def pos(self):
        return (self.rect.x, self.rect.y)

    def speed(self):
        return self.speed

    def update(self):
        self.rect.y += self.speed

    def __del__(self):
        pass
