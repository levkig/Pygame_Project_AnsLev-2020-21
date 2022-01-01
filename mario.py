import pygame
import random

player_img = pygame.image.load('mario.png')
player_img.set_colorkey('White')
player_img2 = pygame.transform.scale(player_img, (110, 113))

mushroom_img = pygame.image.load('mushroom.png')
mushroom_img.set_colorkey('White')
mushroom_img2 = pygame.transform.scale(mushroom_img, (90, 90))

pygame.init()
width = 1800
height = 900
speed = 60
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aario")
clock = pygame.time.Clock()

sc.fill((255, 255, 255))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacles):
        pygame.sprite.Sprite.__init__(self)
        self.obstacles = obstacles
        self.image = player_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.bottom -= 5
        if key[pygame.K_DOWN]:
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            for obc in self.obstacles:
                if self.rect.x == obc[0] + 40 and self.rect.bottom > obc[1]:
                    print('test')
                    return
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
            for obc in self.obstacles:
                if self.rect.x == obc[0] - 100 and self.rect.bottom > obc[1]:
                    print('test')
                    return
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = mushroom_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        pass


class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.speed_x = 0


class Pills(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('BLUE')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0


mushroom = Mushroom(1500, 800)
pill = Pills(0, 0)
turtle = Turtle(300, 890)
all_sprites = pygame.sprite.Group()
player = Player(0, 800, obstacles=[(1200, 750)])
all_sprites.add(player)
all_sprites.add(mushroom)
all_sprites.add(turtle)
all_sprites.add(pill)
run = True
while run:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()
    sc.fill('BLACK')
    pygame.draw.rect(sc, 'WHITE', (1200, 750, 50, 150))
    all_sprites.draw(sc)
    pygame.display.flip()
    pygame.init()
pygame.quit()
