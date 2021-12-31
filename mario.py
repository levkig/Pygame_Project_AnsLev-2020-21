import pygame

pygame.init()
width = 1800
height = 900
speed = 60
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aario")
clock = pygame.time.Clock()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('GREEN')
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.bottom -= 5
        if key[pygame.K_DOWN]:
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = 1400
        self.rect.y = 890
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.bottom -= 5
        if key[pygame.K_DOWN]:
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
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
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.rect.bottom -= 5
        if key[pygame.K_DOWN]:
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
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


class Pills(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('BLUE')
        self.rect = self.image.get_rect()
        self.rect.centerx = 900
        self.rect.bottom = 890
        self.speed_x = 0


mushroom = Mushroom()
pill = Pills()
turtle = Turtle(300, 890)
all_sprites = pygame.sprite.Group()
player = Player()
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
    all_sprites.draw(sc)
    pygame.display.flip()

pygame.quit()
