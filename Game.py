import pygame
import random
pygame.init()

player_img = pygame.image.load('mario.png')
player_img.set_colorkey('White')
player_img2 = pygame.transform.scale(player_img, (110, 110))
mushroom = pygame.sprite.Group()
turtle_group = pygame.sprite.Group()
bomb_group = pygame.sprite.Group()

cake_img = pygame.image.load('cake.png')
cake_img.set_colorkey('White')
cake_img2 = pygame.transform.scale(cake_img, (90, 90))

mushroom_img = pygame.image.load('mushroom.png')
mushroom_img.set_colorkey('White')
mushroom_img2 = pygame.transform.scale(mushroom_img, (90, 90))

turtle_img = pygame.image.load('turtle.png')
turtle_img.set_colorkey('White')
turtle_img2 = pygame.transform.scale(turtle_img, (150, 90))
boss_group = pygame.sprite.Group()

pill_img = pygame.image.load('pill.png')
pill_img.set_colorkey('White')
pill_img2 = pygame.transform.scale(pill_img, (150, 100))

bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
run = True
pygame.init()
width = 1800

height = 900
speed = 60
neg = 2
sc = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aario")
clock = pygame.time.Clock()
used = False
right_side = False
left_side = False


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
        self.isJump = False
        self.jumpCount = 10
        self.left_side = left_side
        self.right_side = right_side
        self.neg = 2

    def toches_obstacle(self, directionx, dx, directiony, dy):
        equation = f'self.rect.{directionx}'
        equation1 = f'self.rect.{directiony}'
        for obc in self.obstacles_ver:
            pass

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
            left_side = True
            right_side = False
        if key[pygame.K_RIGHT]:
            for obc in self.obstacles_hor:
                if self.rect.x == obc[0] - 100 and self.rect.bottom > obc[1]:
                    return
            self.speed_x = 5
            left_side = False
            right_side = True
        self.rect.x += self.speed_x
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 5
                if pygame.sprite.collide_rect(player, pill):
                    neg = 5
                if self.jumpCount < 0:
                    neg = -5

                    if pygame.sprite.collide_rect(player, pill):
                        neg -= 5
                self.rect.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top + 50)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def shoot_right(self):
        bullet2 = BulletRight(self.rect.centerx, self.rect.top + 50)
        all_sprites.add(bullet2)
        bullets.add(bullet2)


class Reward(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = cake_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.speed_x = 0


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = mushroom_img2
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ra = x
        self.pa = self.rect.top
        self.ta = self.rect.right
        self.ya = self.rect.left
        self.random = random.randint(1300, 1800)


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

    def update(self):
        self.speed_x = 0


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1500, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.left_side = left_side
        self.right_side = right_side


class Knife(pygame.sprite.Sprite):
    def __init__(self, x, y, player_info):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.player_info = player_info
        self.left_side = left_side
        self.right_side = right_side


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.left_side = left_side
        self.right_side = right_side


class Key2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.left_side = left_side
        self.right_side = right_side


class Princess(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.left_side = left_side
        self.right_side = right_side


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()


class BulletRight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.x -= self.speedy

        if self.rect.bottom < 0:
            self.kill()


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


pill = Pills(1000, 800)
turtle = Turtle(1700, 800)
bomb = Bomb(1600, 800)
boss = Boss(50, 100)
mushroom_info = Mushroom(x=1500, y=800)
player = Player(x=0, y=800, obstacles_hor=[(1200, 750, 50, 150)],
                obstacles_ver=[(600, 680, 200, 50),
                               (300, 730, 200, 50), (950, 680, 200, 50)], mushroom_info=mushroom_info)
ball1 = Point(450, 830)
ball2 = Point(800, 830)
ball3 = Point(1000, 620)
ball4 = Point(400, 670)
ball5 = Point(650, 620)

reward = Reward(1600, 600)
ver_wall = VerticalWall(1200, 750, 50, 150)
hor_wall = HorizontalWall(600, 680, 200, 50)
hor_wall2 = HorizontalWall(300, 730, 200, 50)
hor_wall3 = HorizontalWall(950, 680, 200, 50)
key = Key(1500, 500)
all_sprites.add(key)
f6 = pygame.font.Font(None, 75)
text6 = f6.render('ОЧКИ:', True, 'White')
f7 = pygame.font.Font(None, 75)
text7 = f7.render('НУЖНО ОЧКОВ:', True, 'White')
f8 = pygame.font.Font(None, 75)
text8 = f8.render('МЯЧЕЙ:', True, 'White')

boss_group.add(boss)
weapon = pygame.sprite.Group()
weapon.add(ball1)
weapon.add(ball2)
weapon.add(ball3)
weapon.add(ball4)
weapon.add(ball5)
all_sprites.add(reward)
all_sprites.add(player)
all_sprites.add(mushroom_info)
all_sprites.add(turtle)
all_sprites.add(pill)
all_sprites.add(bomb)
all_sprites.add(boss)
obstacles = [hor_wall, hor_wall2, hor_wall3, ver_wall]
over = False


def main():
    ochko = 0
    balls = 0
    hp = 25
    a1 = 20
    a2 = 20
    a3 = 20
    a4 = 20
    a5 = 20

    f15 = pygame.font.Font(None, 150)
    text15 = f15.render('С Днем Рождение!', True, 'White')
    run = True
    while run:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.isJump = True
                if event.key == pygame.K_e:
                    balls += 1
                    player.shoot()
                if event.key == pygame.K_r:
                    balls += 1
                    player.shoot_right()
        if pygame.sprite.collide_rect(player, ball1):
            ochko += a1
            a1 = 0
            weapon.remove(ball1)
        if pygame.sprite.collide_rect(player, ball2):
            ochko += a2
            a2 = 0
            weapon.remove(ball2)
        if pygame.sprite.collide_rect(player, ball3):
            ochko += a3
            a3 = 0
            weapon.remove(ball3)
        if pygame.sprite.collide_rect(player, ball4):
            ochko += a4
            a4 = 0
            weapon.remove(ball4)
        if pygame.sprite.collide_rect(player, ball5):
            ochko += a5
            a5 = 0
            weapon.remove(ball5)

        sc.fill('Black')
        f9 = pygame.font.Font(None, 75)
        text9 = f9.render(str(balls), True, 'White')
        f10 = pygame.font.Font(None, 75)
        text10 = f10.render(str(ochko), True, 'White')

        sc.blit(text6, (00, 0))
        sc.blit(text8, (1300, 0))
        sc.blit(text9, (1550, 0))
        sc.blit(text10, (200, 0))
        if pygame.sprite.collide_rect(player, reward):
            all_sprites.remove(reward)
            sc.blit(text15, (700, 300))
        mushroom.add(mushroom_info)
        turtle_group.add(turtle)
        bomb_group.add(bomb)
        for item in obstacles:
            item.draw()
        all_sprites.update()
        all_sprites.draw(sc)
        weapon.update()
        weapon.draw(sc)
        pygame.display.flip()
        if pygame.sprite.collide_rect(player, pill):
            all_sprites.remove(pill)
            seconds_left = 15
            neg = 4
            used = True
        if pygame.sprite.collide_rect(player, mushroom_info):
            if not used:
                over = True
        if pygame.sprite.collide_rect(player, turtle):
            if not used:
                over = True
        if pygame.sprite.collide_rect(player, bomb):
            over = True
        if pygame.sprite.groupcollide(boss_group, bullets, False, True):
            hp -= 1
            ochko += 10
        if hp <= 0:
            all_sprites.remove(boss)
            pygame.init()
            return ochko, hp, balls
        player.jump()
    pygame.quit()
