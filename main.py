import pygame
import random as rd
from random import randrange

pygame.init()
pygame.display.set_caption('Flappy Goose')

WHITE = (255, 255, 255)

screen = width, height = (1200, 700)

main_window = pygame.display.set_mode(screen)

obj = pygame.Surface((20, 20))
obj.fill(WHITE)
obj_rect = obj.get_rect()
obj_speed = [1, 1]

running = True

while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False 
   rand_color = (randrange(255), randrange(255), randrange(255))
   obj_rect = obj_rect.move(obj_speed)
   if obj_rect.bottom >= height or obj_rect.top <= 0:
      obj_speed[1] = -obj_speed[1]
      obj.fill(rand_color)
   if obj_rect.right >= width or obj_rect.left <= 0:
      obj_speed[0] = -obj_speed[0]
      obj.fill(rand_color)
   main_window.fill((155, 155, 155))
   main_window.blit(obj, obj_rect)
   pygame.display.flip()