import pygame
from sys import exit
from random import randint


class Bird(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    mid = pygame.transform.scale_by(pygame.image.load('redbird-midflap.png'),
                                    2)
    up = pygame.transform.scale_by(pygame.image.load('redbird-upflap.png'), 2)
    down = pygame.transform.scale_by(pygame.image.load('redbird-downflap.png'),
                                     2)
    self.frames = [mid, up, down]
    self.index = 0
    self.angle = 0

    self.image = self.frames[self.index]
    self.rect = self.image.get_rect(center=(75, 400))
    self.g = 0

  def input(self):
    self.g = -13

  def fall(self):
    self.g += 1
    self.rect.y += self.g
    if self.rect.top < 0: self.rect.top = 0
    if self.rect.bottom > 800: self.rect.bottom = 800

  def animate(self):
    self.image = pygame.transform.rotate(self.image, self.angle)
    self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery))
    screen.blit(self.image, self.rect)
    print(self.angle)
    if self.g > 0:
      self.index = 0
      if self.angle > -85: self.angle-=4
    else:
      self.index += 0.1
      if self.angle < 20: self.angle+=10
    if self.index >= 3:
      self.index = 0
    self.image = self.frames[int(self.index)]

  def update(self,  flap):
    if flap:
      self.input()
    else:
      self.fall()
      self.animate()

class Pipe(pygame.sprite.Sprite):
  def __init__(self, x, y, top):
    super().__init__()
    if not top:
      self.image = pygame.transform.scale2x(pygame.image.load('pipe-green.png'))
      self.rect = self.image.get_rect(midtop = (x, y+135))
    else:
      self.image = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load('pipe-green.png')), 180)
      self.rect = self.image.get_rect(midbottom = (x, y-135))
  
  def update(self):
    self.rect.x-=4
    screen.blit(self.image, self.rect)

    if self.rect.x < -100:
      self.kill()

class Base(pygame.sprite.Sprite):
  def __init__(self, x=0):
    super().__init__()
    self.image = pygame.transform.scale(pygame.image.load('base.png'), (800, 100))
    self.rect = self.image.get_rect(topleft = (x, 700))
  
  def update(self):
    self.rect.x-=4
    if self.rect.x < -800: self.kill()

pygame.init()
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Flappy Bird (Clone)')
clock = pygame.time.Clock()

game_active = False

msg = pygame.transform.scale_by(pygame.image.load('message.png'), 2)
msg_rect = msg.get_rect(center=(200, 400))

bg = pygame.transform.scale(pygame.image.load('background-day.png'),(400, 800))
bg_rect = bg.get_rect(topleft=(0, 0))

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

pipes = pygame.sprite.Group()
score = 0

font = pygame.font.Font('flappy-font.ttf', 50)
text = font.render(str(score), False, (255,255,255))
text_rect = text.get_rect(center = (200, 100))

base = pygame.sprite.Group()
base.add(Base())

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == 69:
      if game_active:
        text = font.render(str(score), False, (255,255,255))
        text_rect = text.get_rect(center = (200, 100))
        screen.blit(text, text_rect)
        score+=1
       
        y = randint(200,500)
        pipes.add(Pipe(600, y, False))
        pipes.add(Pipe(600, y, True))

        base.add(Base(400))
    if not game_active and (event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and event.key == pygame.K_SPACE)):
      game_active = True
      bird.add(Bird())
      time = 0
      score = 0
      base.add(Base())
      pygame.time.set_timer(69, 1500)
    if game_active and (event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and event.key == pygame.K_SPACE)):
      bird.update(True)
  screen.blit(bg, bg_rect)
  if not game_active:
    screen.blit(msg, msg_rect)
  if game_active:
    if pygame.sprite.groupcollide(bird, pipes, True, True) or pygame.sprite.groupcollide(bird, base, True, True):
      game_active = False
      pipes.empty()
      base.empty()
      score = 0
      text = font.render(str(score), False, (255,255,255))
      text_rect = text.get_rect(center = (200, 100))
      screen.blit(text, text_rect)
      continue
    bird.update(False)
    pipes.update()
    base.update()
    screen.blit(text, text_rect)
    base.draw(screen)
   

  pygame.display.update()
  clock.tick(60)
