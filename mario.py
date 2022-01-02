import pygame

player_img = pygame.image.load('mario.png')
player_img.set_colorkey('White')
player_img2 = pygame.transform.scale(player_img, (110, 113))

mushroom_img = pygame.image.load('mushroom.png')
mushroom_img.set_colorkey('White')
mushroom_img2 = pygame.transform.scale(mushroom_img, (90, 90))

turtle_img = pygame.image.load('turtle.png')
turtle_img.set_colorkey('White')
turtle_img2 = pygame.transform.scale(turtle_img, (150, 100))

pill_img = pygame.image.load('pill.png')
pill_img.set_colorkey('White')
pill_img2 = pygame.transform.scale(pill_img, (150, 100))

run = True
pygame.init()
width = 1800
height = 900
speed = 60
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aario")
clock = pygame.time.Clock()


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
            for obc in self.obstacles:
                if self.rect.bottom == 600 + 10 and self.rect.x > obc[0] - 50:
                    return
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            for obc in self.obstacles:
                if self.rect.x == obc[0] + 40 and self.rect.bottom > obc[1]:
                    return
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
            for obc in self.obstacles:
                if self.rect.x == obc[0] - 100 and self.rect.bottom > obc[1]:
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
        self.speed_x = 5
        self.run = run

    def update(self):
        pass


class Turtle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = turtle_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.speed_x = 0


class Pills(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pill_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0


class VerticalWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 150))
        self.image.fill('GREEN')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 50))
        self.image.fill('GREEN')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


all_sprites = pygame.sprite.Group()
mushroom = Mushroom(1500, 800)
pill = Pills(0, 0)
turtle = Turtle(300, 800)
player = Player(0, 800, obstacles=[(1200, 750)])

all_sprites.add()
all_sprites.add(player)
all_sprites.add(mushroom)
all_sprites.add(turtle)
all_sprites.add(pill)
while run:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    sc.fill('Black')
    pygame.draw.rect(sc, 'WHITE', (1200, 750, 50, 150))
    pygame.draw.rect(sc, 'WHITE', (1200, 600, 200, 50))
    all_sprites.update()
    all_sprites.draw(sc)
    pygame.display.flip()
pygame.quit()
