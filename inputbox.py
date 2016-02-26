import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from settings import *

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,25)
  pygame.draw.rect(screen, white,
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    screen.get_width() / 2,40))
  pygame.draw.rect(screen, black,
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    (screen.get_width() / 2) + 10,50))
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, black),
                ((screen.get_width() / 2-100), (screen.get_height() / 2)-5))
  pygame.display.flip()

def ask(screen):
  "ask(screen) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, "".join(current_string))
  while 1:
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

def main():

  #fich = open('highscore.txt','w')
  screen = pygame.display.set_mode((320,240))
  s = ask(screen) + " - "
  fich.write(s)


if __name__ == '__main__': main()
