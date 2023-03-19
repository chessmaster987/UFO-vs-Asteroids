import pygame
import random as rd
from random import randrange
from pygame import font, time

pygame.init()
pygame.display.set_caption('UFO vs Asteroids')

FPS = pygame.time.Clock()

WHITE = (255, 255, 255)

screen = width, height = (1500, 800)

main_window = pygame.display.set_mode(screen)

image_obj = pygame.transform.scale(pygame.image.load('./imgs/ufo.png').convert_alpha(), (45, 45))
image_enemy = pygame.transform.scale(pygame.image.load('./imgs/asteroid.png').convert_alpha(), (70, 50))
image_weapon = pygame.transform.scale(pygame.image.load('./imgs/weapon.png').convert_alpha(), (45, 35))
image_bckg = pygame.transform.scale(pygame.image.load('./imgs/background.jpg').convert(), screen) 

bckgX = 0
bckgX2 = image_bckg.get_width()
image_bckg_speed = 3

obj_x = width // 2
obj_y = height // 2
obj_speed = 10

def create_enemy():
   enemy = pygame.Surface((20, 20))
   enemy_rect = pygame.Rect(width, rd.randint(0, height), *enemy.get_size())
   enemy_speed = rd.randint(5, 10)
   return [enemy, enemy_rect, enemy_speed]

def create_weapon():
   weapon_x = rd.randrange(0, width)
   weapon_y = 0
   weapon = pygame.Surface((20, 20))
   obj_rect = pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())
   weapon_rect = pygame.Rect(weapon_x, weapon_y, *weapon.get_size())
   weapon_speed = 1
   return [weapon, weapon_rect, weapon_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000) #time of creating asteroids
CREATE_WEAPON = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_WEAPON, 2000) #time of creating weapons
  
my_font = font.SysFont(None, 36)

score = 0

enemies = []
weapons = []

running = True
while running:
   FPS.tick(60)
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False 
      if event.type == CREATE_ENEMY:
         enemies.append(create_enemy())
      if event.type == CREATE_WEAPON:
         weapons.append(create_weapon())

   bckgX -= image_bckg_speed
   bckgX2 -= image_bckg_speed
   if bckgX < -image_bckg.get_width():
      bckgX = image_bckg.get_width()

   if bckgX2 < -image_bckg.get_width():
      bckgX2 = image_bckg.get_width()

   main_window.blit(image_bckg, (bckgX, 0))
   main_window.blit(image_bckg, (bckgX2, 0))

   main_window.blit(image_obj, (obj_x, obj_y))

   keys = pygame.key.get_pressed()
   obj_rect = pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())
   if keys[pygame.K_LEFT] and not obj_rect.left <= 0:
      obj_x -= obj_speed
   if keys[pygame.K_RIGHT] and not obj_rect.right >= width:
      obj_x += obj_speed
   if keys[pygame.K_UP] and not obj_rect.top <= 0:
      obj_y -= obj_speed
   if keys[pygame.K_DOWN]and not obj_rect.bottom >= height:
      obj_y += obj_speed

   main_window.blit(my_font.render(str(score), True, (255, 0, 0)), (width // 2, 5))

   for enemy in enemies:
      # Move enemy and blit to screen
      enemy[1] = enemy[1].move(-enemy[2], 0)
      main_window.blit(image_enemy, enemy[1])
      
      # Remove enemies that go off screen
      if enemy[1].left < 0:
         enemies.pop(enemies.index(enemy))
      
      # Check for collision with object
      if enemy[1].colliderect(pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())):
         text = my_font.render(f'YOU EARNED {score} POINTS', True, (0, 255, 0))
         text_rect = text.get_rect()
         text_x = width // 2 - text_rect.width // 2
         text_y = height // 2 - text_rect.height // 2
         main_window.blit(text, [text_x, text_y])
         pygame.display.update()
         time.wait(3000)
         running = False
         
   for weapon in weapons:
      # Move weapon and blit to screen
      weapon[1] = weapon[1].move(0, weapon[2])
      main_window.blit(image_weapon, weapon[1])
         
      # Remove weapons that go off screen
      if weapon[1].bottom >= height:
         weapons.pop(weapons.index(weapon))
         
      # Check for collision with object
      if weapon[1].colliderect(pygame.Rect(obj_x, obj_y, image_obj.get_width(), image_obj.get_height())):
         weapons.remove(weapon)
         score += 1

   pygame.display.flip()

   