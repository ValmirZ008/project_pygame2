import sys
import pygame
from pygame.locals import *
import math
import random

def load_background(image_path, width, height):
    background = pygame.image.load(image_path).convert()
    return pygame.transform.scale(background, (width, height))

pygame.init()
display_info = pygame.display.Info()
max_resolution = display_info.current_w, display_info.current_h
SCREEN_WIDTH = max_resolution[0] - 100
SCREEN_HEIGHT = max_resolution[1] - 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ThunderStrike")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)


class Application:
    def __init__(self, screen):
        info_object = pygame.display.Info()
        max_resolution = (info_object.current_w, info_object.current_h)
        global SLIDER_WIDTH, SLIDER_HEIGHT, SLIDER_X, KNOB_SIZE, sliders
        self.screen = screen
        self.background = load_background('data/images/bg.jpg', SCREEN_WIDTH, SCREEN_HEIGHT)
        SLIDER_WIDTH = int(SCREEN_WIDTH * 0.7)
        SLIDER_HEIGHT = 20
        SLIDER_X = SCREEN_WIDTH // 2 - SLIDER_WIDTH // 2
        KNOB_SIZE = 10
        one_third_screen_height = SCREEN_HEIGHT // 3
        one_fifth_screen_height = SCREEN_HEIGHT // 5
        self.sliders = sliders
        self.back_button = Button("Back", SCREEN_WIDTH - 190, 20, 80, 40, GREY)
        self.save_button = Button("Save", SCREEN_WIDTH - 90, 20, 80, 40, GREY)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    for slider in self.sliders:
                        slider.handle_event(event)
                    self.back_button.handle_event(event, self.sliders)
                    self.save_button.handle_event(event, self.sliders)
            self.screen.blit(self.background, (0, 0))
            for slider in self.sliders:
                slider.draw(self.screen)
            self.back_button.draw(self.screen)
            self.save_button.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        sys.exit()


class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, sliders=[]):
        self.sliders = sliders
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.clicked()

    def clicked(self):
        if self.text == "Back":
            main_menu(screen)
        elif self.text == "Save":
            self.save()

    def save(self):
        for slider in self.sliders:
            print(f"{slider.title}: {slider.get_current_value()}")
            # тут вместо вывода должна быть запись в бд


class Slider:
    def __init__(self, title, y_position, initial_value=50):
        self.title = title
        self.y_position = y_position
        self.value = initial_value
        SLIDER_WIDTH = int(SCREEN_WIDTH * 0.7)
        self.knob_pos = initial_value / 100 * SLIDER_WIDTH

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.title, True, WHITE)
        text_rect = text_surface.get_rect(midtop=(SCREEN_WIDTH // 2, self.y_position - 40))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, GREY, (SLIDER_X, self.y_position, SLIDER_WIDTH, SLIDER_HEIGHT), border_radius=3)
        knob_x = SLIDER_X + self.knob_pos - KNOB_SIZE // 2
        pygame.draw.circle(screen, RED, (knob_x, self.y_position + SLIDER_HEIGHT // 2), KNOB_SIZE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._process_click(event.pos)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self._process_drag(event.pos)

    def _process_click(self, mouse_pos):
        knob_x = SLIDER_X + self.knob_pos - KNOB_SIZE // 2
        knob_y = self.y_position + SLIDER_HEIGHT // 2
        if ((mouse_pos[0] >= knob_x - KNOB_SIZE and mouse_pos[0] <= knob_x + KNOB_SIZE and
             mouse_pos[1] >= knob_y - KNOB_SIZE and mouse_pos[1] <= knob_y + KNOB_SIZE) or
                (SLIDER_X <= mouse_pos[0] <= SLIDER_X + SLIDER_WIDTH and
                 self.y_position <= mouse_pos[1] <= self.y_position + SLIDER_HEIGHT)):
            self.knob_pos = mouse_pos[0] - SLIDER_X
            if self.knob_pos < 0:
                self.knob_pos = 0
            elif self.knob_pos > SLIDER_WIDTH:
                self.knob_pos = SLIDER_WIDTH
            self.value = int(self.knob_pos / SLIDER_WIDTH * 100)

    def _process_drag(self, mouse_pos):
        knob_x = SLIDER_X + self.knob_pos - KNOB_SIZE // 2
        knob_y = self.y_position + SLIDER_HEIGHT // 2
        if ((mouse_pos[0] >= knob_x - KNOB_SIZE and mouse_pos[0] <= knob_x + KNOB_SIZE and
             mouse_pos[1] >= knob_y - KNOB_SIZE and mouse_pos[1] <= knob_y + KNOB_SIZE) or
                (SLIDER_X <= mouse_pos[0] <= SLIDER_X + SLIDER_WIDTH and
                 self.y_position <= mouse_pos[1] <= self.y_position + SLIDER_HEIGHT)):
            self.knob_pos = mouse_pos[0] - SLIDER_X
            if self.knob_pos < 0:
                self.knob_pos = 0
            elif self.knob_pos > SLIDER_WIDTH:
                self.knob_pos = SLIDER_WIDTH
            self.value = int(self.knob_pos / SLIDER_WIDTH * 100)

    def get_current_value(self):
        return self.value


class Scores:
    def __init__(self, screen, sp):
        self.screen = screen
        self.sp = sp
        self.start_x = SCREEN_WIDTH * 0.59
        self.start_y = SCREEN_HEIGHT * 0.37
        self.step_x = SCREEN_WIDTH * 0.22 / len(sp)
        self.step_y = SCREEN_HEIGHT * 0.098
        self.images = [pygame.transform.scale(pygame.image.load(f'data/images/{str(i)}.png'), (self.step_x, self.step_y)) for i in sp]

    def draw(self):
        for i in range(len(self.sp)):
            rect = pygame.Rect(self.start_x + self.step_x * i, self.start_y, self.step_x, self.step_y)
            self.screen.blit(self.images[i], rect)



class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Bufs(pygame.sprite.Sprite):
    arrow_icon = pygame.transform.scale(pygame.image.load('data/images/arrow.png'), (100, 50))
    heart_icon = pygame.transform.scale(pygame.image.load('data/images/heart.png'), (150, 100))

    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if type:
            self.image = Bufs.heart_icon
        else:
            self.image = Bufs.arrow_icon
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/images/bullet.png'), (16, 32))

    def __init__(self, x, y):
        super().__init__()
        self.image = Bullet.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 20

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy_bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(pygame.image.load('data/images/enemy_bullet.png'), (16, 32))

    def __init__(self, x, y):
        super().__init__()
        self.image = Bullet.image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


class Enemy_2(GameObject):
    left_image = pygame.transform.scale(pygame.image.load('data/images/enemy_2_left.png'), (128, 72))
    right_image = pygame.transform.scale(pygame.image.load('data/images/enemy_2_right.png'), (128, 72))
    image = pygame.transform.scale(pygame.image.load('data/images/enemy_2.png'), (128, 72))

    def __init__(self, x, y):
        super().__init__('data/images/enemy_2.png', x, y)
        self.left_image = Enemy_2.left_image
        self.right_image = Enemy_2.right_image
        self.last_shot_time = 0
        self.speed = 6
        self.side = 0
        self.hit_count = 0

    def update(self, x_p):
        if self.side == 0:
            if random.randint(0, 1):
                self.rect.x -= self.speed
                self.image = self.left_image
                self.side = -10
            else:
                self.rect.x += self.speed
                self.image = self.right_image
                self.side = 10
        else:
            if self.side > 0:
                self.rect.x += self.speed
                self.side -= 1
            else:
                self.rect.x -= self.speed
                self.side += 1
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT * -0.2:
            self.rect.top = SCREEN_HEIGHT * -0.2
        elif self.rect.bottom > SCREEN_HEIGHT // 4:
            self.rect.bottom = SCREEN_HEIGHT // 4

    def go(self):
        self.rect.x = -1000


class Enemy_Hight(GameObject):
    left_image = pygame.transform.scale(pygame.image.load('data/images/enemy_left_1.png'), (128, 72))
    right_image = pygame.transform.scale(pygame.image.load('data/images/enemy_right_1.png'), (128, 72))
    image = pygame.image.load('data/images/enemy_1.png')

    def __init__(self, x, y):
        super().__init__('data/images/enemy_1.png', x, y)
        self.left_image = Enemy_Hight.left_image
        self.right_image = Enemy_Hight.right_image
        self.last_shot_time = 0
        self.speed = 4
        self.hit_count = 0

    def update(self, x_p):
        if abs(self.rect.centerx - x_p) <= 5:
            self.image = Enemy_Hight.image
        elif x_p < self.rect.centerx:
            self.rect.x -= self.speed
            self.image = self.left_image
        elif x_p > self.rect.centerx:
            self.rect.x += self.speed
            self.image = self.right_image
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT * -0.2:
            self.rect.top = SCREEN_HEIGHT * -0.2
        elif self.rect.bottom > SCREEN_HEIGHT // 4:
            self.rect.bottom = SCREEN_HEIGHT // 4

    def go(self):
        self.rect.x = -1000


class Ship(GameObject):
    left_image = pygame.transform.scale(pygame.image.load('data/images/resized_ship_left.png'), (256, 144))
    right_image = pygame.transform.scale(pygame.image.load('data/images/resized_ship_right.png'), (256, 144))
    shield_left_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield_left.png'), (256, 144))
    shield_right_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield_right.png'), (256, 144))
    shield_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield.png'), (256, 144))
    image = pygame.image.load('data/images/resized_ship.png')

    def __init__(self, x, y):
        super().__init__('data/images/resized_ship.png', x, y)
        self.left_image = Ship.left_image
        self.right_image = Ship.right_image
        self.shield_left_image = Ship.shield_left_image
        self.shield_right_image = Ship.shield_right_image
        self.shield_image = Ship.shield_image
        self.count_shield = 0
        self.count_speed = 0
        self.normal_speed = 10
        self.double_speed = 2 * self.normal_speed
        self.speed = self.normal_speed
        self.shield_active = 0
        self.shield_duration = 0
        self.shield_timer = 0

    def update(self, keys, dt):
        dx = 0
        dy = 0

        if keys[K_LEFT] or keys[K_a]:
            dx -= self.speed
            if not self.shield_active:
                self.image = self.left_image
            else:
                self.image = self.shield_left_image
        if keys[K_RIGHT] or keys[K_d]:
            dx += self.speed
            if not self.shield_active:
                self.image = self.right_image
            else:
                self.image = self.shield_right_image
        if keys[K_UP] or keys[K_w]:
            dy -= self.speed
        if keys[K_DOWN] or keys[K_s]:
            dy += self.speed

        if not any([keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN]]):
            if not self.shield_active:
                self.image = Ship.image
            else:
                self.image = self.shield_image

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT / 2:
            self.rect.top = SCREEN_HEIGHT / 2
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.shield_active:
            self.shield_duration -= dt
            if self.shield_duration <= 0:
                self.shield_active = 0
                self.image = Ship.image

    def activate_double_speed(self, duration=5000):
        self.speed = self.double_speed
        pygame.time.set_timer(USEREVENT+1, duration, loops=1)

    def activate_shield(self, duration=10000):
        self.shield_active = 3
        self.shield_duration = duration
        self.image = self.shield_image


class MainGameScreen:
    background_image = pygame.transform.scale(pygame.image.load('data/images/bg_play_image.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    hp = [pygame.transform.scale(pygame.image.load(f'data/images/hp_{i}.png'), (600, 300)) for i in range(15, -1, -1)]
    arrow_icon = pygame.transform.scale(pygame.image.load('data/images/arrow.png'), (200, 100))
    heart_icon = pygame.transform.scale(pygame.image.load('data/images/heart.png'), (300, 200))
    arrow_icon_gray = pygame.transform.scale(pygame.image.load('data/images/arrow_gray.png'), (200, 100))
    heart_icon_gray = pygame.transform.scale(pygame.image.load('data/images/heart_gray.png'), (300, 200))

    def __init__(self, screen):
        pygame.mixer.music.load('data/sounds/фон на уровень.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2 * sliders[1].get_current_value() / 100)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.bg_color = (0, 0, 0)
        self.background_image = MainGameScreen.background_image
        self.copy_background_image = self.background_image.copy()
        self.background_rect = self.background_image.get_rect()
        self.background_rect.y = 0
        self.copy_rect = self.copy_background_image.get_rect()
        self.copy_rect.y = -self.background_rect.height
        self.ship = Ship(SCREEN_WIDTH // 2, screen.get_height() * 2 // 3)
        self.bufs_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.shut = pygame.mixer.Sound('data/sounds/выстрел.mp3')
        self.minus_hp = [pygame.mixer.Sound('data/sounds/отнимание_жизни.mp3'), pygame.mixer.Sound('data/sounds/отнимание_жизни_2.mp3')]
        self.shut.set_volume(0.05 * sliders[2].get_current_value() / 100)
        self.minus_hp[0].set_volume(0.3 * sliders[2].get_current_value() / 100)
        self.minus_hp[1].set_volume(0.3 * sliders[2].get_current_value() / 100)
        self.hp_images = MainGameScreen.hp
        self.hp_index = 0
        self.arrow_icon = MainGameScreen.arrow_icon
        self.heart_icon = MainGameScreen.heart_icon
        self.arrow_icon_gray = MainGameScreen.arrow_icon_gray
        self.heart_icon_gray = MainGameScreen.heart_icon_gray
        self.arrow_rect = self.arrow_icon.get_rect(bottomleft=(25, SCREEN_HEIGHT - 50))
        self.heart_rect = self.heart_icon.get_rect(bottomright=(450, SCREEN_HEIGHT - 15))
        self.scores = 0
        self.count_wawe = 0
        self.wawe_timer = 0
        self.new_wawe = True
        self.message_alpha = 255
        self.message_start_time = 0
        self.message_lifetime = 3000

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            current_time = pygame.time.get_ticks()
            if len(self.enemy_group) == 0:
                self.message_start_time = current_time
                self.new_wawe = False
                self.count_wawe += 1
                for _ in range(int(self.count_wawe // 3)):
                    enemy = Enemy_Hight(random.randint(0, SCREEN_WIDTH), random.randint(0, 100))
                    self.enemy_group.add(enemy)
                for _ in range(self.count_wawe - int(self.count_wawe // 3)):
                    enemy = Enemy_2(random.randint(0, SCREEN_WIDTH), random.randint(0, 100))
                    self.enemy_group.add(enemy)
            elapsed_time = current_time - self.message_start_time
            if elapsed_time < self.message_lifetime:
                self.message_alpha = int(255 - (elapsed_time / self.message_lifetime) * 255)
            else:
                self.message_alpha = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.arrow_rect.collidepoint(pos) and self.ship.count_speed > 0:
                        self.ship.activate_double_speed(duration=5000)
                        self.ship.count_speed -= 1
                    elif self.heart_rect.collidepoint(pos) and self.ship.count_shield > 0:
                        self.ship.activate_shield(duration=10000)
                        self.ship.count_shield -= 1
                    else:
                        bullet = Bullet(self.ship.rect.centerx - 20, self.ship.rect.centery - 5)
                        self.bullet_group.add(bullet)
                        bullet = Bullet(self.ship.rect.centerx + 20, self.ship.rect.centery - 5)
                        self.bullet_group.add(bullet)
                        self.shut.play()
                elif event.type == USEREVENT+1:
                    self.ship.speed = self.ship.normal_speed
            for bullet in self.bullet_group:
                for enemy in self.enemy_group:
                    if pygame.sprite.collide_mask(enemy, bullet):
                        bullet.kill()
                        enemy.hit_count += 1
                        if isinstance(enemy, Enemy_Hight):
                            if enemy.hit_count >= 6:
                                enemy.kill()
                                self.scores += 15
                                if random.randint(0, 10) > 7:
                                    if random.randint(0, 1) == 0:
                                        self.bufs_group.add(Bufs(enemy.rect.centerx, enemy.rect.centery, 1))
                                    else:
                                        self.bufs_group.add(Bufs(enemy.rect.centerx, enemy.rect.centery, 0))
                                enemy.go()
                        else:
                            if enemy.hit_count >= 3:
                                enemy.kill()
                                self.scores += 10
                                if random.randint(0, 10) > 7:
                                    if random.randint(0, 1) == 0:
                                        self.bufs_group.add(Bufs(enemy.rect.centerx, enemy.rect.centery, 1))
                                    else:
                                        self.bufs_group.add(Bufs(enemy.rect.centerx, enemy.rect.centery, 0))
                                enemy.go()
            for bullet in self.enemy_bullet_group:
                if pygame.sprite.collide_mask(self.ship, bullet):
                    bullet.kill()
                    if self.ship.shield_active:
                        self.minus_hp[1].play()
                    else:
                        self.hp_index += 0.5
                        if int(self.hp_index) == int(self.hp_index + 0.5):
                            self.minus_hp[0].play()
                        if self.hp_index > 15:
                            running = False
                            self.hp_index = 15
            for buf in self.bufs_group:
                if pygame.sprite.collide_mask(self.ship, buf):
                    buf.kill()
                    if buf.type:
                        self.ship.count_shield += 1
                    else:
                        self.ship.count_speed += 1
                    buf.rect.x = -1000
            for enemy in self.enemy_group:
                if abs(enemy.rect.centerx - self.ship.rect.centerx) <= 30 and (pygame.time.get_ticks() - enemy.last_shot_time) > 500:
                    self.enemy_bullet_group.add(Enemy_bullet(enemy.rect.centerx - 5, enemy.rect.centery))
                    self.enemy_bullet_group.add(Enemy_bullet(enemy.rect.centerx + 5, enemy.rect.centery))
                    enemy.last_shot_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            self.ship.update(keys, dt)
            self.bullet_group.update()
            self.enemy_bullet_group.update()
            self.bufs_group.update()
            for enemy in self.enemy_group:
                if enemy.alive():
                    enemy.update(self.ship.rect.centerx)
            if self.background_rect.y >= SCREEN_HEIGHT:
                self.background_rect.y = self.copy_rect.y - self.background_rect.height
            elif self.copy_rect.y >= SCREEN_HEIGHT:
                self.copy_rect.y = self.background_rect.y - self.copy_rect.height
            self.background_rect.y += self.clock.get_time() * 0.2
            self.copy_rect.y += self.clock.get_time() * 0.2
            self.screen.fill(self.bg_color)
            self.screen.blit(self.background_image, self.background_rect)
            self.screen.blit(self.copy_background_image, self.copy_rect)
            if self.ship.count_speed:
                self.screen.blit(self.arrow_icon, self.arrow_rect)
            else:
                self.screen.blit(self.arrow_icon_gray, self.arrow_rect)
            if self.ship.count_shield:
                self.screen.blit(self.heart_icon, self.heart_rect)
            else:
                self.screen.blit(self.heart_icon_gray, self.heart_rect)
            msg = message(f"Your score: {self.scores}", "Red")
            screen.blit(msg, (0, 0))
            if self.message_alpha > 0:
                msg = message(f"{self.count_wawe} WAWE!!!", "Red", self.message_alpha)
                self.screen.blit(msg, (SCREEN_WIDTH // 2, 0))
            self.enemy_group.draw(self.screen)
            self.bufs_group.draw(self.screen)
            self.screen.blit(self.hp_images[int(self.hp_index)], (5, 500))
            self.enemy_bullet_group.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.screen.blit(self.ship.image, self.ship.rect)
            pygame.display.flip()

    def get_scores(self):
        return self.scores


class Finish:
    def __init__(self, screen, scores):
        self.screen = screen
        self.scores = scores
        self.back_button = Button("Back", SCREEN_WIDTH - 190, 20, 80, 40, GREY)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                else:
                    self.back_button.handle_event(event)
            best_scores = 1 # тут должно быть значение из бд
            if self.scores > best_scores:
                self.screen.fill((0, 0, 0))
                msg = message(f"GAME OVER!", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.1, 10))
                msg = message(f"Your scores: {str(self.scores)}", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.1, 410))
                msg = message(f"It's a record! Comgratulations!!!", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.1, 210))
                msg = message(f"Good luck captain)", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.1, 610))
                self.back_button.draw(self.screen)
                pygame.display.flip()
                #тут должна быть перезапись значения в бд
            else:
                self.screen.fill((0, 0, 0))
                msg = message(f"GAME OVER!", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.2, 10))
                msg = message(f"Your scores: {str(self.scores)}", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.2, 210))
                msg = message(f"Best scores: {str(best_scores)}", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.2, 410))
                msg = message(f"Good luck captain)", "Red", n=150)
                self.screen.blit(msg, (SCREEN_WIDTH * 0.2, 610))
                self.back_button.draw(self.screen)
                pygame.display.flip()



def message(msg, color, alpha=255, n=60):
    font_style = pygame.font.SysFont(None, n)
    surface = font_style.render(msg, True, color)
    surface.set_alpha(alpha)
    return surface


def main_menu(screen):
    global background, start_button, settings_button, sliders
    pygame.mixer.music.load('data/sounds/фон меню.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(sliders[0].get_current_value() / 100)
    click = pygame.mixer.Sound('data/sounds/звук_нажатия_на_кнопку.mp3')
    running = True
    scores = Scores(screen, [9, 7, 8])
    start = False
    settings = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start:
                    pygame.mixer.music.stop()
                    click.play()
                    game_screen = MainGameScreen(screen)
                    game_screen.run()
                    f = Finish(screen, game_screen.get_scores())
                    f.run()
                    break
                elif settings:
                    pygame.mixer.music.stop()
                    click.play()
                    app = Application(screen)
                    app.run()
                    break
        mouse_pos = pygame.mouse.get_pos()
        if start_x <= mouse_pos[0] <= start_x + 640 and \
                start_y <= mouse_pos[1] <= start_y + 310:
            start = True
            settings = False
            screen.blit(start_button, (0, 0))
            scores.draw()
        elif settings_x <= mouse_pos[0] <= settings_x + 640 and \
                settings_y <= mouse_pos[1] <= settings_y + 310:
            start = False
            settings = True
            screen.blit(settings_button, (0, 0))
            scores.draw()
        else:
            start, settings = False, False
            screen.blit(background, (0, 0))
            scores.draw()
        pygame.display.update()


if __name__ == "__main__":
    one_third_screen_height = SCREEN_HEIGHT // 3
    one_fifth_screen_height = SCREEN_HEIGHT // 5
    sliders = [
        Slider('Звук меню', one_third_screen_height, initial_value=50),  # в initial_value должны быть значения из бд
        Slider('Музыка уровня', one_third_screen_height + one_fifth_screen_height, initial_value=50),
        Slider('Эффекты', one_third_screen_height + 2 * one_fifth_screen_height, initial_value=50)
    ]
    start_x = 640
    start_y = SCREEN_HEIGHT // 3 + 170
    settings_x = 640
    settings_y = SCREEN_HEIGHT // 3 + 400
    background = pygame.transform.scale(pygame.image.load('data/images/menu_2.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    start_button = pygame.transform.scale(pygame.image.load('data/images/menu_2_start.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    settings_button = pygame.transform.scale(pygame.image.load('data/images/menu_2_settings.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    main_menu(screen)