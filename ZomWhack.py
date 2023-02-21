import pygame, sys
import os
import random

from pygame.locals import *
from os import path

#Folder
folder = os.path.dirname(__file__)
img_folder = os.path.join(folder, 'Image')
sound_folder = os.path.join(folder, 'Sound')

#Window
width = 900
height = 700
FPS = 60

#Game Variable
cols = 3
rows = 2


start_time = pygame.time.get_ticks()

background = (207, 137, 0)
white = (255, 255, 255)


def print_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    font_surface = font.render(text, True, font_color)
    screen.blit(font_surface, (x, y))

def draw_hole():
    x, y = 0, 0
    for r in range(rows):
        x = 0
        for c in range(cols):
            screen.blit(hole, (x * 300 + 60, y * 240 + 200))
            # pygame.draw.rect(screen, (255, 0, 0), (x * 300 + 60, y * 200 + 200, 180, 120))
            #Hole for Zombie appear
            rect = pygame.Rect(x * 300 + 105, y * 240 + 183, 100, 140)
            # pygame.draw.rect(screen, (0, 0, 255), (rect))
            # pygame.draw.rect(screen, (207, 137, 0), (x*300 + 105, y*200 + 183, 100, 140))
            hole_list_rect.append(rect)
            x += 1
        y += 1

def cover_zom():
    x, y = 0, 0
    for r in range(rows):
        x = 0
        for c in range(cols):
            pygame.draw.rect(screen, background, (x * 300 + 105, y * 240 + 315, 100, 126))
            x += 1
        y += 1

def random_zombie():
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    random_hole = random.choice(hole_list_rect)
    zom_rect.midtop = random_hole.midbottom
    return random_hole[1]

def start_countdown():
    global game_time, last_countdown
    playing = pygame.time.get_ticks()
    if playing - last_countdown > 1000:
        last_countdown = now
        game_time -= 1
    print_text(str(game_time), 36, white, width // 2, 20)

def hit_effect():
    blood_rect


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(path.join(sound_folder, 'background.mp3'))
pygame.mixer.music.play() # -1 means the music will loop indefinitely

#Game Init
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('World Saver')
clock = pygame.time.Clock()

#Ingame variable
mouse_pos = (0, 0)
pygame.mouse.set_visible(False)
ready_time = 5
score = 0
hit = 0
miss = 0
pos = 0
game_time = 30 + 1
game_over = False
last = pygame.time.get_ticks()
last_countdown = pygame.time.get_ticks()

#Sound
hit_sfx = pygame.mixer.Sound(path.join(sound_folder, 'hit.mp3'))
miss_sfx = pygame.mixer.Sound(path.join(sound_folder, 'miss.mp3'))
zombie_sfx = pygame.mixer.Sound(path.join(sound_folder, 'zombie.mp3'))

#Image
hole_base = pygame.image.load(path.join(img_folder, 'Hole_5.png')).convert_alpha()
hole = pygame.transform.scale(hole_base, (180, 120))
hole_list_rect = []

zom_base = pygame.image.load(path.join(img_folder, 'zom_1.png')).convert_alpha()
zombie = pygame.transform.scale(zom_base, (100, 140))
zom_rect = zombie.get_rect()

blood_base = pygame.image.load(path.join(img_folder, 'blood.png')).convert_alpha()
blood = pygame.transform.scale(blood_base, (80, 80))
blood_rect = blood.get_rect()
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
        if event.type == pygame.USEREVENT:
            pos = random_zombie()
        if event.type == MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:
                if zom_rect.collidepoint(mouse_pos):
                    score += 2
                    hit += 1
                    hit_sfx.play()
                    # screen.blit(blood, blood_rect)
                    pos = random_zombie()
                    pygame.time.delay(25)
                    zombie_sfx.play()
                else:
                    if score > 0:
                        score -= 1
                        miss += 1
                    # miss_sfx.play()
                    miss_sfx.play()
                    pos = random_zombie()
                aim_img = aim[1]
        if event.type == MOUSEBUTTONUP and not game_over:
            if event.button == 1:
                aim_img = aim[0]
        if event.type == KEYUP and game_over:
            if event.key == K_r:
                pygame.mixer.music.play()
                ready_time = 5
                score = 0
                pos = 0
                game_time = 30 + 1
                game_over = False

        mouse_pos = pygame.mouse.get_pos()
        aim_rect.center = (mouse_pos[0], mouse_pos[1])

    pygame.display.flip()

    now = pygame.time.get_ticks()
    if now - last > 1000 and ready_time > 0:
        last = now
        ready_time -= 1
        pos = random_zombie()

    zom_rect.y -= 1
    if zom_rect.y <= pos:
        zom_rect.y = pos


    screen.fill(background)
    draw_hole()

    
    if ready_time == 5:
        print_text('Ready?', 60, (180, 0, 0), (width // 2) - 60, 20)
    elif ready_time > 1:
        print_text(str(ready_time-1), 50, (255, 255, 0), width // 2, 20)
    elif ready_time == 1:
        print_text('Go', 60, (0, 255, 0), (width // 2) - 20, 20)
    else:
        screen.blit(zombie, zom_rect)
        if not game_over:
            start_countdown()
            print_text(f"Score: {score}", 36, (255, 255, 255), 10, 20)
            print_text(f"Hit: {hit}", 36, (255, 255, 255), 10, 40)
            print_text(f"Miss: {miss}", 36, (255, 255, 255), 10, 60)

    cover_zom()

    if game_time < 0:
        game_over = True
        print_text("GAME OVER", 36, (255, 255, 255), (width // 2) - 70, 30)
        print_text(f"SCORE: {score}", 36, (255, 255, 255), (width // 2) - 50, 60)
        print_text("PRESS R TO RESTART", 36, (255, 255, 255), (width // 2) - 120, 90)


    screen.blit(aim_img, aim_rect)

pygame.quit()