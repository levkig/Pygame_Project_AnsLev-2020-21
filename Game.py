from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import json
import time
import pygame
import random

pygame.init()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Mushrom(GameSprite):
    def __init__(self, x, y, image):
        GameSprite.__init__(self, x, y, image)
        self.move_cnt = 0
        self.dir = None


class Bomb(GameSprite):
    def __init__(self, x, y, image):
        GameSprite.__init__(self, x, y, image)
        self.move_cnt = 0
        self.dir = None


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width_rect, height_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width_rect, height_rect))
        self.image.fill('WHITE')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Key2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill('RED')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class GameImage:
    def __init__(self, height, width, background, image_path):
        self.height = height
        self.width = width
        self.background = background
        self.image_path = image_path

    def get_image(self):
        if hasattr(self, 'image') and self.image:
            return self.image

        self.image = pygame.image.load(self.image_path)
        self.image.set_colorkey(self.background)
        self.image = pygame.transform.scale(self.image, (self.height, self.width))
        return self.image


player_image = GameImage(110, 110, 'White', 'mario.png')
mushroom_image = GameImage(90, 90, 'White', 'mushroom.png')
turtle_image = GameImage(150, 90, 'White', 'turtle.png')
pill_image = GameImage(150, 100, 'White', 'pill.png')
boss_image = GameImage(1000, 500, 'WHITE', 'boss.jpg')
bomb_image = GameImage(90, 90, 'WHITE', 'bomb.jpg')
boss_group = pygame.sprite.Group()


class GameSettings:
    def __init__(self, height, width, speed, level):
        self.width = width
        self.height = height
        self.speed = speed
        self.level = level
        self.level_to_settings = {
            1: 'settings.json',
            2: 'settings2.json',
            3: 'settings3.json'
        }
        self.settings = eval(open(self.level_to_settings[self.level]).read())

    def increase_level(self):
        self.level += 1
        self.settings = eval(open(self.level_to_settings[self.level]).read())

    def add_to_sprite(self, sprite):
        for obs in self.obstacles:
            sprite.add(obs)
        for ball in self.balls:
            sprite.add(ball)
        for mushroom in self.mushrooms:
            sprite.add(mushroom)
        for bomb in self.bombs:
            sprite.add(bomb)
        for turtle in self.turtles:
            sprite.add(turtle)
        for boss in self.bosses:
            sprite.add(boss)

    def remove_from_sprite(self, sprite):
        for obs in self.obstacles:
            sprite.remove(obs)
        for ball in self.balls:
            sprite.remove(ball)
        for mushroom in self.mushrooms:
            sprite.remove(mushroom)
        for bomb in self.bombs:
            sprite.remove(bomb)
        for turtle in self.turtles:
            sprite.remove(turtle)
        for boss in self.bosses:
            sprite.remove(boss)

    def init_game(self):
        self.init_balls()
        self.init_obstacles()
        self.init_mushrooms()
        self.init_bombs()
        self.init_turtles()
        self.init_bosses()

    def init_bombs(self):
        bombs = []
        bombs_info = self.settings.get('bombs')
        for gi in bombs_info:
            bombs.append(GameSprite(gi[0], gi[1], bomb_image.get_image()))
        self.bombs = bombs

    def init_turtles(self):
        turtles = []
        turtles_info = self.settings.get('turtles')
        for ui in turtles_info:
            turtles.append(GameSprite(ui[0], ui[1], turtle_image.get_image()))
        self.turtles = turtles

    def init_balls(self):
        balls = []
        balls_info = self.settings.get('balls')
        for bi in balls_info:
            balls.append(Point(bi[0], bi[1]))
        self.balls = balls

    def init_obstacles(self):
        obstacles = []
        obstacles_info = self.settings.get('obstacles')
        for oi in obstacles_info:
            obstacles.append(Obstacle(oi[0], oi[1], oi[2], oi[3]))
        self.obstacles = obstacles

    def init_mushrooms(self):
        mushrooms = []
        mushrooms_info = self.settings.get('mushrooms')
        for di in mushrooms_info:
            mushrooms.append(Mushrom(di[0], di[1], mushroom_image.get_image()))
        self.mushrooms = mushrooms

    def init_bosses(self):
        bosses = []
        bosses_info = self.settings.get('bosses')
        for di in bosses_info:
            bosses.append(Mushrom(di[0], di[1], boss_image.get_image()))
        self.bosses = bosses


mushroom_group = pygame.sprite.Group()
turtle_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

run = True
game_settings = GameSettings(height=900, width=1800, speed=60, level=1)
game_settings.init_game()

sc = pygame.display.set_mode((game_settings.width, game_settings.height))
pygame.display.set_caption("Aario")

clock = pygame.time.Clock()
used = False
right_side = False
left_side = False


def check_position(player_rect, obstacles):
    for obs in obstacles:
        if player_rect.colliderect(obs):
            return False
    return True


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, game_settings, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.game_settings = game_settings
        self.image = image
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

        self.isJump = False
        self.jumpCount = 10
        self.jump_height = 500


    def update(self):
        key = pygame.key.get_pressed()
        new_pos_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if key[pygame.K_UP]:
            new_pos_rect.bottom -= self.speed
            if not check_position(new_pos_rect, self.game_settings.obstacles):
                return
            new_pos_rect.bottom += self.speed
            self.rect.bottom -= self.speed

        if key[pygame.K_DOWN]:
            new_pos_rect.bottom += self.speed
            if not check_position(new_pos_rect, self.game_settings.obstacles):
                return
            self.rect.bottom += self.speed

        if key[pygame.K_LEFT]:
            new_pos_rect.left -= self.speed
            if not check_position(new_pos_rect, self.game_settings.obstacles):
                return
            self.rect.left -= self.speed

        if key[pygame.K_RIGHT]:
            new_pos_rect.right += self.speed
            if not check_position(new_pos_rect, self.game_settings.obstacles):
                return
            self.rect.right += self.speed

        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0

    def remove_killed_mushrooms(self):
        for mushroom in self.game_settings.mushrooms:
            if self.rect.bottom == mushroom.rect.top and abs(self.rect.centerx - mushroom.rect.centerx) < self.rect.width:
                self.game_settings.mushrooms.remove(mushroom)
                all_sprites.remove(mushroom)

    def jump(self):
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 5
                if self.jumpCount < 0:
                    neg = -5
                bad = False
                new_pos_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
                new_pos_rect.y -= self.jumpCount ** 2 * 0.1 * neg
                for obs in self.game_settings.obstacles:
                    if new_pos_rect.colliderect(obs):
                        self.isJump = False
                        self.jumpCount = 10
                        bad = True
                        break
                if bad:
                    return
                self.rect.y -= self.jumpCount ** 2 * 0.1 * neg
                self.remove_killed_mushrooms()
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def jump_task(self):
        for i in range(self.jump_height):
            self.remove_killed_mushrooms()
            new_y = self.rect.y - 1 if i <= self.jump_height // 2 else self.rect.y + 1
            new_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
            for obs in self.game_settings.obstacles:
                if new_rect.colliderect(obs.rect):
                    return
            if i <= self.jump_height // 2:
                self.rect.y -= 1
                time.sleep(0.001)
            else:
                self.rect.y += 1
                time.sleep(0.001)

    def shoot(self):
        bullet = BulletRight(self.rect.centerx, self.rect.top + 50, -1, 10)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def shoot_right(self):
        bullet = Bullet(self.rect.centerx, self.rect.top + 50, 1, 10)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 10))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.direction = direction

    def update(self):
        self.rect.x += (self.speedy * self.direction)

        if self.rect.bottom < 0:
            self.kill()


class BulletRight(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill('YELLOW')
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy
        self.direction = direction

    def update(self):
        self.rect.y += (self.speedy * self.direction)

        if self.rect.bottom < 0:
            self.kill()


pill = GameSprite(1000, 800, pill_image.get_image())
key1 = Key(500, 800)
key2 = Key2(1200, 800)

player = Player(0, 800, player_image.get_image(), game_settings=game_settings, width=1800, height=900)

f6 = pygame.font.Font(None, 75)
text6 = f6.render('ОЧКИ:', True, 'White')
f7 = pygame.font.Font(None, 75)
text7 = f7.render('НУЖНО ОЧКОВ:', True, 'White')
f8 = pygame.font.Font(None, 75)
text8 = f8.render('МЯЧЕЙ:', True, 'White')

weapon = pygame.sprite.Group()

all_sprites.add(player, mushroom_group, turtle_group, pill)
all_sprites.add(key1, key2)
over = False

dy = None
cnt = 0


def move_mushroom(mushroom, obstacle, n, m):
    if mushroom.move_cnt == 0 or not mushroom.dir:
        mushroom.dir = random.choice([-1, 1])
        mushroom.move_cnt = random.randint(30, 50)
    ny = mushroom.rect.left + mushroom.dir if mushroom.dir == -1 else mushroom.rect.right + mushroom.dir
    if mushroom.dir == -1 and ny < 0 or mushroom.dir == 1 and ny > 1800:
        mushroom.move_cnt = 0
        move_mushroom(mushroom, obstacle, 1800, 900)
    for obs in obstacle:
        if mushroom.dir == -1 and ny == obs.rect.right or mushroom.dir == 1 and ny == obs.rect.left:
            mushroom.move_cnt = 0
            move_mushroom(mushroom, obstacle, 1800, 900)
    mushroom.move_cnt -= 1
    mushroom.rect.left += mushroom.dir
    return mushroom


def increase_level():
    game_settings.remove_from_sprite(all_sprites)
    game_settings.increase_level()
    game_settings.init_game()
    game_settings.add_to_sprite(all_sprites)


game_settings.add_to_sprite(all_sprites)


def main():
    ochko = 0
    over = False
    balls = 0
    hp = 25
    a1 = 1
    a2 = 1
    a3 = 1

    f15 = pygame.font.Font(None, 150)
    run = True

    while run:
        clock.tick(game_settings.speed)
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

        for ball in game_settings.balls:
            if pygame.sprite.collide_rect(player, ball):
                print(1)
                ochko += 20
                all_sprites.remove(ball)
                game_settings.balls.remove(ball)

        sc.fill('black')
        f9 = pygame.font.Font(None, 75)
        text9 = f9.render(str(balls), True, 'White')
        f10 = pygame.font.Font(None, 75)
        text10 = f10.render(str(ochko), True, 'White')

        sc.blit(text6, (00, 0))
        sc.blit(text8, (1300, 0))
        sc.blit(text9, (1550, 0))
        sc.blit(text10, (200, 0))

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

        for mushroom in game_settings.mushrooms:
            if player.rect.bottom == mushroom.rect.top and \
                abs(player.rect.centerx - mushroom.rect.centerx) < 110:
                mushroom = None
                break
            new_rect = pygame.Rect(player.rect.x, player.rect.y, player.rect.width, player.rect.height)
            if mushroom.rect.y >= player.rect.y:
                new_rect.y -= 5
            else:
                new_rect.y += 5
            if new_rect.colliderect(mushroom.rect):
                over = True
                break
            move_mushroom(mushroom, game_settings.obstacles, game_settings.height, game_settings.width)

        if pygame.sprite.groupcollide(boss_group, bullets, False, True):
            hp -= 1
            ochko += 10
        if pygame.sprite.collide_rect(player, key1):
            if a1 == 1:
                increase_level()
                all_sprites.remove(key1)
                a1 = 0
            else:
                pass
        if pygame.sprite.collide_rect(player, key2):
            if a3 == 1:
                increase_level()
                all_sprites.remove(key2)
                a3 = 0
            else:
                pass
        if pygame.sprite.groupcollide(bullets, boss_group, True, False):
            hp -= 1
        if pygame.sprite.groupcollide(turtle_group, bullets, False, True):
            pass

        if hp <= 0:
            pygame.init()
            return ochko, hp, balls
        if over:
            scr = pygame.display.set_mode((1800, 900))

            f1 = pygame.font.Font(None, 100)
            text1 = f1.render('ВЫ ПРОИГРАЛИ', True, 'White')
            f2 = pygame.font.Font(None, 70)
            text2 = f2.render('КОЛИЧЕСТВО МЯЧЕЙ:', True, 'WHITE')
            f3 = pygame.font.Font(None, 50)
            text3 = f3.render('ВЫЙТИ', True, 'White')
            f4 = pygame.font.Font(None, 50)
            text4 = f4.render('Escape', True, 'White')
            f5 = pygame.font.Font(None, 70)
            text5 = f5.render('КОЛИЧЕСТВО ОЧКОВ:', True, 'WHITE')
            f20 =pygame.font.Font(None, 90)
            text20 = f20.render(str(ochko), True, 'White')
            f21 = pygame.font.Font(None, 90)
            text21 = f21.render(str(balls), True, 'WHITE')

            no = pygame.draw.rect(scr, 'RED', (750, 550, 300, 100))

            scr.blit(text1, (630, 50))
            scr.blit(text2, (50, 200))
            scr.blit(text3, (820, 560))
            scr.blit(text4, (830, 600))
            scr.blit(text5, (50, 300))
            scr.blit(text20, (700, 300))
            scr.blit(text21, (700, 200))
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
        player.jump()
    pygame.quit()
