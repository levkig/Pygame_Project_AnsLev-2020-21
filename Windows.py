import pygame
from time import sleep
import random
from game import main

run = True
pygame.font.init()
pygame.init()
sc = pygame.display.set_mode((1800, 900))
f1 = pygame.font.Font(None, 100)
text1 = f1.render('НАЧАТЬ ИГРУ', True, 'White')
f2 = pygame.font.Font(None, 50)
text2 = f2.render('ПОДТВЕРДИТЬ', True, 'White')
f3 = pygame.font.Font(None, 50)
text3 = f3.render('ОТМЕНА', True, 'White')
f4 = pygame.font.Font(None, 50)
text4 = f4.render('Escape', True, 'White')
f5 = pygame.font.Font(None, 50)
text5 = f5.render('Space', True, 'White')
boss_group = pygame.sprite.Group()

yes = pygame.draw.rect(sc, 'GREEN', (750, 350, 300, 100))
no = pygame.draw.rect(sc, 'RED', (750, 550, 300, 100))
sc.blit(text1, (660, 50))
sc.blit(text2, (765, 360))
sc.blit(text3, (820, 560))
sc.blit(text4, (830, 600))
sc.blit(text5, (850, 400))
mushroom = pygame.sprite.Group()
turtle_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()

pygame.mixer.music.load('music.mp3')

pygame.display.update()
pos = pygame.mouse.get_pos()
key = pygame.mouse.get_pressed()

while run:
    key = pygame.key.get_pressed()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if key[pygame.K_ESCAPE]:
            run = False
        if key[pygame.K_SPACE]:
            ochko, hp, balls = main()
            sc = pygame.display.set_mode((1800, 900))

            f1 = pygame.font.Font(None, 100)
            text1 = f1.render('ВЫ ВЫИГРАЛИ', True, 'White')
            f2 = pygame.font.Font(None, 70)
            text2 = f2.render('КОЛИЧЕСТВО МЯЧЕЙ:', True, 'WHITE')
            f3 = pygame.font.Font(None, 50)
            text3 = f3.render('ВЫЙТИ', True, 'White')
            f4 = pygame.font.Font(None, 50)
            text4 = f4.render('Escape', True, 'White')
            f5 = pygame.font.Font(None, 70)
            text5 = f5.render('КОЛИЧЕСТВО ОЧКОВ:', True, 'WHITE')
            f6 = pygame.font.Font(None, 90)
            text6 = f6.render(str(ochko), True, 'White')
            f7 = pygame.font.Font(None, 90)
            text7 = f7.render(str(balls), True, 'WHITE')

            no = pygame.draw.rect(sc, 'RED', (750, 550, 300, 100))

            sc.blit(text1, (630, 50))
            sc.blit(text2, (50, 200))
            sc.blit(text3, (820, 560))
            sc.blit(text4, (830, 600))
            sc.blit(text5, (50, 300))
            sc.blit(text6, (700, 300))
            sc.blit(text7, (700, 200))
            pygame.display.update()
            key = pygame.mouse.get_pressed()

            run = True
            while run:
                key = pygame.key.get_pressed()
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        run = False
                    if key[pygame.K_ESCAPE]:
                        run = False
            pygame.quit()
