import pygame
import random as rd
from random import randrange

pygame.init()
pygame.display.set_caption('UFO vs Asteroids')

FPS = pygame.time.Clock()

WHITE = (255, 255, 255)

screen = width, height = (1200, 700)

main_window = pygame.display.set_mode(screen)

image_obj = pygame.image.load('./imgs/ufo.jpg')
image_enemy = pygame.image.load('./imgs/asteroid.jpg')

obj_x = width // 2
obj_y = height // 2
obj_speed = 5

def create_enemy():
   enemy = pygame.Surface((20, 20))
   enemy_rect = pygame.Rect(width, rd.randint(0, height), *enemy.get_size())
   enemy_speed = rd.randint(5, 10)
   return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 750) #time of creating asteroids
  
enemies = []

running = True
while running:
   FPS.tick(60)
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False 
      if event.type == CREATE_ENEMY:
         enemies.append(create_enemy())

   main_window.fill((WHITE))
   main_window.blit(image_obj, (obj_x, obj_y))

   keys = pygame.key.get_pressed()
   if keys[pygame.K_LEFT]:
      obj_x -= obj_speed
   if keys[pygame.K_RIGHT]:
      obj_x += obj_speed
   if keys[pygame.K_UP]:
      obj_y -= obj_speed
   if keys[pygame.K_DOWN]:
      obj_y += obj_speed
   
   for enemy in enemies:
      enemy[1] = enemy[1].move(-enemy[2], 0)
      main_window.blit(image_enemy, enemy[1])
      if enemy[1].left < 0:
         enemies.pop(enemies.index(enemy)) #clear the left asteroids
         
   pygame.display.flip()