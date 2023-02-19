import pygame, sys
import os
import random

from pygame.locals import *
from os import path

folder = os.path.dirname(__file__)
img_folder = os.path.join(folder, 'Image')

#Window
width = 900
height = 700
FPS = 60

#Game Variable
cols = 3
rows = 2


def draw_hole():
    x,y = 0,0
    for r in range(rows):
        x = 0
        for c in range(cols):
            screen.blit(hole, (x*300+50, y*200))

            #Hole for Zombie appear
            rect = pygame.Rect(x*300 + 100, y*200 + 20, 110, 180)
            # pygame.draw.rect(screen, (0,0,255), (rect))
            hole_list_rect.append(rect)

            x += 1
        y += 1

def random_zombie():
    random_hole = random.choice(hole_list_rect)
    zom_rect.midbottom = random_hole.midbottom

pygame.init()

#Game Init
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('World Saver')
clock = pygame.time.Clock()

#Game variable
mouse_pos = (0, 0)
pygame.mouse.set_visible(False)

#Image
hole_base = pygame.image.load(path.join(img_folder, 'Hole_4.png')).convert_alpha()
hole = pygame.transform.scale(hole_base, (212.1, 300))
hole_list_rect = []

zom_base = pygame.image.load(path.join(img_folder, 'zom.png')).convert_alpha()
zombie = pygame.transform.scale(zom_base, (141.7, 200))
zom_rect = zombie.get_rect()


#convert_alpha for transparent pixels picture

aim =[]
for i in range(1, 3):
    img = pygame.image.load(path.join(img_folder, 'aim{}.png'.format(i))).convert_alpha()
    aim.append(img)

aim_img = aim[0]
aim_rect = aim_img.get_rect()
#get_rect return rectangular coordinates

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                aim_img = aim[1]
                random_zombie()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                aim_img = aim[0]

        mouse_pos = pygame.mouse.get_pos()
        aim_rect.center = (mouse_pos[0], mouse_pos[1])

    # pygame.display.update()
    pygame.display.flip()

    screen.fill((207, 137, 0))
    # screen.blit(Back, (0,0))
    draw_hole()
    screen.blit(aim_img, aim_rect)
    screen.blit(zombie, zom_rect)

pygame.quit()