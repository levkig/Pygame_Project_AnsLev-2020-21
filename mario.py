import pygame

pygame.init()
width = 1000
height = 600
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('GREEN')
        self.rect = self.image.get_rect()
        self.rect.x = 750
        self.rect.y = 540
        self.speed_x = 0

    def update(self):
        pass

enemy = Enemy()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
all_sprites.add(enemy)

run = True
while run:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()
    sc.fill('BLACK')
    pygame.draw.rect(sc, 'RED', (600, 510, 50, 80))
    pygame.draw.rect(sc, 'RED', (900, 510, 50, 80))
    all_sprites.draw(sc)
    pygame.display.flip()

pygame.quit()
