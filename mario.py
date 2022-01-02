import pygame

player_img = pygame.image.load('mario.png')
player_img.set_colorkey('White')
player_img2 = pygame.transform.scale(player_img, (110, 110))

mushroom_img = pygame.image.load('mushroom.png')
mushroom_img.set_colorkey('White')
mushroom_img2 = pygame.transform.scale(mushroom_img, (90, 90))

turtle_img = pygame.image.load('turtle.png')
turtle_img.set_colorkey('White')
turtle_img2 = pygame.transform.scale(turtle_img, (150, 100))

pill_img = pygame.image.load('pill.png')
pill_img.set_colorkey('White')
pill_img2 = pygame.transform.scale(pill_img, (150, 100))

all_sprites = pygame.sprite.Group()

run = True
pygame.init()
width = 1800
height = 900
speed = 60
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aario")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacles_hor, obstacles_ver, mushroom_info):
        pygame.sprite.Sprite.__init__(self)
        self.obstacles_hor = obstacles_hor
        self.obstacles_ver = obstacles_ver
        self.mushroom_info = mushroom_info
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
            for obc in self.obstacles_ver:
                if self.rect.bottom == obc[1] + 5 and self.rect.x > obc[0] - 100:
                    if self.rect.bottom == obc[1] + 5 and self.rect.x < obc[0] + obc[2]:
                        return
            self.rect.bottom += 5
        if key[pygame.K_LEFT]:
            for obc in self.obstacles_hor:
                if self.rect.x == obc[0] + 40 and self.rect.bottom > obc[1]:
                    return
            self.speed_x = -5
        if key[pygame.K_RIGHT]:
            for obc in self.obstacles_hor:
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
        if self.rect.bottom == self.mushroom_info.pa:
            all_sprites.remove(mushroom_info)
        if self.rect.right == self.mushroom_info.ya or \
                self.rect.left == self.mushroom_info.ta or self.rect.x == self.mushroom_info.ra:
            print(1)


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = mushroom_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ra = x
        self.pa = self.rect.top
        self.ta = self.rect.right
        self.ya = self.rect.left


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
    def __init__(self, x, y, width_rect, height_rect):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width_rect = width_rect
        self.height_rect = height_rect

    def draw(self):
        pygame.draw.rect(sc, 'WHITE', (self.x, self.y, self.width_rect, self.height_rect))


class HorizontalWall(pygame.sprite.Sprite):
    def __init__(self, x, y, width_rect, height_rect):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width_rect = width_rect
        self.height_rect = height_rect

    def draw(self):
        pygame.draw.rect(sc, 'WHITE', (self.x, self.y, self.width_rect, self.height_rect))


pill = Pills(0, 0)
turtle = Turtle(300, 800)
mushroom_info = Mushroom(x=1500, y=800)
player = Player(0, 800, obstacles_hor=[(1200, 750, 50, 150)],
                obstacles_ver=[(600, 650, 200, 50), (300, 700, 200, 50)], mushroom_info=mushroom_info)
ver_wall = VerticalWall(1200, 750, 50, 150)
hor_wall = HorizontalWall(600, 650, 200, 50)
hor_wall2 = HorizontalWall(300, 700, 200, 50)
all_sprites.add()
all_sprites.add(player)
all_sprites.add(mushroom_info)
all_sprites.add(turtle)
all_sprites.add(pill)
obstacles = [hor_wall, ver_wall, hor_wall2]


while run:
    clock.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    sc.fill('Black')
    for item in obstacles:
        item.draw()
    all_sprites.update()
    all_sprites.draw(sc)
    pygame.display.flip()
pygame.quit()
