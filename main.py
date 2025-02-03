# import sys
# import pygame
# from pygame.locals import *
#
#
# pygame.init()
# display_info = pygame.display.Info()
# max_resolution = display_info.current_w, display_info.current_h
# SCREEN_WIDTH = max_resolution[0] - 100
# SCREEN_HEIGHT = max_resolution[1] - 100
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("ThunderStrike")
#
#
# class GameObject(pygame.sprite.Sprite):
#     def __init__(self, image_path, x, y):
#         super().__init__()
#         self.image = pygame.image.load(image_path)
#         self.rect = self.image.get_rect(topleft=(x, y))
#         self.mask = pygame.mask.from_surface(self.image)
#
#
# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.transform.scale(pygame.image.load('data/images/bullet.png'), (16, 32))# Замена на путь к вашему изображению пули
#         self.rect = self.image.get_rect(center=(x, y))
#         self.speed = 10
#
#     def update(self):
#         self.rect.y -= self.speed
#         if self.rect.bottom < 0:
#             self.kill()
#
#
# class Ship(GameObject):
#     def __init__(self, x, y):
#         super().__init__('data/images/resized_ship.png', x, y)
#         self.left_image = pygame.image.load('data/images/resized_ship_left.png')
#         self.right_image = pygame.image.load('data/images/resized_ship_right.png')
#         self.speed = 12
#
#     def update(self, keys):
#         dx = 0
#         dy = 0
#
#         if keys[K_LEFT] or keys[K_a]:
#             dx -= self.speed
#             self.image = self.left_image
#         if keys[K_RIGHT] or keys[K_d]:
#             dx += self.speed
#             self.image = self.right_image
#         if keys[K_UP] or keys[K_w]:
#             dy -= self.speed
#         if keys[K_DOWN] or keys[K_s]:
#             dy += self.speed
#
#         if not any([keys[K_LEFT], keys[K_RIGHT], keys[K_UP], keys[K_DOWN]]):
#             self.image = pygame.image.load('data/images/resized_ship.png')
#
#         self.rect.x += dx
#         self.rect.y += dy
#
#         if self.rect.left < 0:
#             self.rect.left = 0
#         elif self.rect.right > SCREEN_WIDTH:
#             self.rect.right = SCREEN_WIDTH
#         if self.rect.top < SCREEN_HEIGHT / 3:
#             self.rect.top = SCREEN_HEIGHT / 3
#         elif self.rect.bottom > SCREEN_HEIGHT:
#             self.rect.bottom = SCREEN_HEIGHT
#
#
# class MainGameScreen:
#     background_image = pygame.transform.scale(pygame.image.load('data/images/bg_play_image.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
#
#     def __init__(self, screen):
#         self.screen = screen
#         self.clock = pygame.time.Clock()
#         self.bullet_group = pygame.sprite.Group()  # Группа для хранения всех пуль
#         self.bg_color = (0, 0, 0)
#
#         # Загружаем фоновое изображение
#         self.background_image = MainGameScreen.background_image
#         self.copy_background_image = self.background_image.copy()
#
#         # Определяем начальные позиции двух экземпляров фона
#         self.background_rect = self.background_image.get_rect()
#         self.background_rect.y = 0
#         self.copy_rect = self.copy_background_image.get_rect()
#         self.copy_rect.y = -self.background_rect.height
#
#         self.ship = Ship(screen.get_width() // 2, screen.get_height() * 2 // 3)
#         self.hp_images = [pygame.transform.scale(pygame.image.load(f'time_images/hp_{i}.png'), (600, 300)) for i in range(15, -1, -1)]
#         self.hp_index = 0  # Индекс текущего изображения полоски прогресса
#         # self.progress_timer = 0
#
#     def run(self):
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     running = False
#                     pygame.quit()
#                     sys.exit()
#                 elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Правая кнопка мыши
#                     bullet = Bullet(self.ship.rect.centerx - 20, self.ship.rect.centery - 5)  # Создаем новую пулю
#                     self.bullet_group.add(bullet)
#                     bullet = Bullet(self.ship.rect.centerx + 20, self.ship.rect.centery - 5)  # Создаем новую пулю
#                     self.bullet_group.add(bullet)
#
#             keys = pygame.key.get_pressed()
#             self.ship.update(keys)
#             self.bullet_group.update()
#             # current_time = pygame.time.get_ticks()
#             # if current_time - self.progress_timer >= 10000:  # Каждые 10 секунд
#             #     self.progress_timer = current_time
#             #     self.hp_index = (self.hp_index + 1) % len(self.hp_images)
#
#             # Обновляем положение фонового изображения
#             if self.background_rect.y >= SCREEN_HEIGHT:
#                 self.background_rect.y = self.copy_rect.y - self.background_rect.height
#             elif self.copy_rect.y >= SCREEN_HEIGHT:
#                 self.copy_rect.y = self.background_rect.y - self.copy_rect.height
#
#             self.background_rect.y += self.clock.get_time() * 0.2
#             self.copy_rect.y += self.clock.get_time() * 0.2
#
#             # Очищаем экран
#             self.screen.fill(self.bg_color)
#
#             # Рисуем фоны
#             self.screen.blit(self.background_image, self.background_rect)
#             self.screen.blit(self.copy_background_image, self.copy_rect)
#
#             # Рисуем корабль и сердца
#             self.screen.blit(self.hp_images[self.hp_index], ((SCREEN_WIDTH - self.hp_images[self.hp_index].get_width()) // 2, -200))
#             self.bullet_group.draw(self.screen)
#             self.screen.blit(self.ship.image, self.ship.rect)
#             pygame.display.flip()
#             self.clock.tick(60)
#
#
# def main_menu(screen):
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 running = False
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == MOUSEBUTTONDOWN and event.button == 1:
#                 mouse_pos = pygame.mouse.get_pos()
#                 if resume_x <= mouse_pos[0] <= resume_x + 640 and \
#                         resume_y <= mouse_pos[1] <= resume_y + 360:
#                     # screen.blit(resume_button, (0, 0))
#                     game_screen = MainGameScreen(screen)
#                     game_screen.run()
#                     break
#         mouse_pos = pygame.mouse.get_pos()
#         # if start_x <= mouse_pos[0] <= start_x + 640 and \
#         #         start_y <= mouse_pos[1] <= start_y + 360:
#         #     screen.blit(start_button, (0, 0))
#         # if resume_x <= mouse_pos[0] <= resume_x + 640 and \
#         #         resume_y <= mouse_pos[1] <= resume_y + 360:
#         #     screen.blit(resume_button, (0, 0))
#         # elif settings_x <= mouse_pos[0] <= settings_x + 640 and \
#         #         settings_y <= mouse_pos[1] <= settings_y + 360:
#         #     screen.blit(settings_button, (0, 0))
#         # else:
#         screen.blit(background, (0, 0))
#         pygame.display.update()
#
#
# if __name__ == "__main__":
#     start_x = 640
#     start_y = SCREEN_HEIGHT // 3
#     resume_x = 640
#     resume_y = SCREEN_HEIGHT // 3 + 170
#     settings_x = 640
#     settings_y = SCREEN_HEIGHT // 3 + 400
#     background = pygame.image.load('data/images/menu_2.png').convert()
#     # start_button = pygame.image.load('data/images/menu_1_start.png').convert_alpha()
#     # resume_button = pygame.image.load('data/images/menu_1_resume.png').convert_alpha()
#     # settings_button = pygame.image.load('data/images/menu_1_settings.png').convert_alpha()
#     main_menu(screen)
import sys
import pygame
from pygame.locals import *
import math

pygame.init()
display_info = pygame.display.Info()
max_resolution = display_info.current_w, display_info.current_h
SCREEN_WIDTH = max_resolution[0] - 100
SCREEN_HEIGHT = max_resolution[1] - 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ThunderStrike")


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/images/bullet.png'), (16, 32))  # Замена на путь к вашему изображению пули
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy_Hight(GameObject):
    def __init__(self, x, y):
        super().__init__('data/images/resized_ship.png', x, y)
        self.left_image = pygame.transform.scale(pygame.image.load('data/images/enemy_left_1.png'), (256, 144))
        self.right_image = pygame.transform.scale(pygame.image.load('data/images/enemy_right_1.png'), (256, 144))
        self.speed = 5
        self.direction = 'center'

    def update(self, keys, x_p, y_p):
        if x_p < self.rect.x:
            self.rect.x -= self.speed
            self.image = self.left_image
            self.direction = 'left'
        elif x_p > self.rect.x:
            self.rect.x += self.speed
            self.image = self.right_image
            self.direction = 'right'
        else:
            self.image = pygame.transform.scale(pygame.image.load('data/images/enemy_1.png'), (256, 144))
            self.direction = 'center'

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT * -0.2:
            self.rect.top = SCREEN_HEIGHT * -0.2
        elif self.rect.bottom > SCREEN_HEIGHT // 4:
            self.rect.bottom = SCREEN_HEIGHT // 4


class Ship(GameObject):
    def __init__(self, x, y):
        super().__init__('data/images/resized_ship.png', x, y)
        self.left_image = pygame.transform.scale(pygame.image.load('data/images/resized_ship_left.png'), (256, 144))
        self.right_image = pygame.transform.scale(pygame.image.load('data/images/resized_ship_right.png'), (256, 144))
        self.shield_left_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield_left.png'), (256, 144))
        self.shield_right_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield_right.png'), (256, 144))
        self.shield_image = pygame.transform.scale(pygame.image.load('data/images/ship_shield.png'), (256, 144))
        self.normal_speed = 10
        self.double_speed = 2 * self.normal_speed
        self.speed = self.normal_speed
        self.shield_active = False
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
                self.image = pygame.image.load('data/images/resized_ship.png')
            else:
                self.image = self.shield_image

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT / 3:
            self.rect.top = SCREEN_HEIGHT / 3
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.shield_active:
            self.shield_duration -= dt
            if self.shield_duration <= 0:
                self.shield_active = False
                self.image = pygame.image.load('data/images/resized_ship.png')  # Возвращаемся к обычному изображению корабля

    def activate_double_speed(self, duration=5000):
        self.speed = self.double_speed
        pygame.time.set_timer(USEREVENT+1, duration, loops=1)

    def activate_shield(self, duration=10000):
        self.shield_active = True
        self.shield_duration = duration
        self.image = self.shield_image


class MainGameScreen:
    background_image = pygame.transform.scale(pygame.image.load('data/images/bg_play_image.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bullet_group = pygame.sprite.Group()  # Группа для хранения всех пуль
        self.bg_color = (0, 0, 0)
        self.rocket = Enemy_Hight(screen.get_width() // 2, 20)
        self.background_image = MainGameScreen.background_image
        self.copy_background_image = self.background_image.copy()
        self.background_rect = self.background_image.get_rect()
        self.background_rect.y = 0
        self.copy_rect = self.copy_background_image.get_rect()
        self.copy_rect.y = -self.background_rect.height
        self.ship = Ship(screen.get_width() // 2, screen.get_height() * 2 // 3)
        self.hp_images = [pygame.transform.scale(pygame.image.load(f'data/images/hp_{i}.png'), (600, 300)) for i in range(15, -1, -1)]
        self.hp_index = 0
        self.arrow_icon = pygame.transform.scale(pygame.image.load('data/images/arrow.png'), (200, 100))
        self.heart_icon = pygame.transform.scale(pygame.image.load('data/images/heart.png'), (300, 200))
        self.arrow_rect = self.arrow_icon.get_rect(bottomleft=(25, SCREEN_HEIGHT - 50))
        self.heart_rect = self.heart_icon.get_rect(bottomright=(450, SCREEN_HEIGHT - 15))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.arrow_rect.collidepoint(pos):
                        self.ship.activate_double_speed(duration=5000)
                    elif self.heart_rect.collidepoint(pos):
                        self.ship.activate_shield(duration=10000)
                    else:  # Правая кнопка мыши
                        bullet = Bullet(self.ship.rect.centerx - 20, self.ship.rect.centery - 5)
                        self.bullet_group.add(bullet)
                        bullet = Bullet(self.ship.rect.centerx + 20, self.ship.rect.centery - 5)
                        self.bullet_group.add(bullet)
                elif event.type == USEREVENT+1:
                    self.ship.speed = self.ship.normal_speed
            keys = pygame.key.get_pressed()
            self.ship.update(keys, dt)
            self.bullet_group.update()
            self.rocket.update(keys, self.ship.rect.x, self.ship.rect.x)
            if self.background_rect.y >= SCREEN_HEIGHT:
                self.background_rect.y = self.copy_rect.y - self.background_rect.height
            elif self.copy_rect.y >= SCREEN_HEIGHT:
                self.copy_rect.y = self.background_rect.y - self.copy_rect.height
            self.background_rect.y += self.clock.get_time() * 0.2
            self.copy_rect.y += self.clock.get_time() * 0.2
            self.screen.fill(self.bg_color)
            self.screen.blit(self.background_image, self.background_rect)
            self.screen.blit(self.copy_background_image, self.copy_rect)
            self.screen.blit(self.arrow_icon, self.arrow_rect)
            self.screen.blit(self.heart_icon, self.heart_rect)
            self.screen.blit(self.rocket.image, self.rocket.rect)
            self.screen.blit(self.hp_images[self.hp_index], (5, 500))
            self.bullet_group.draw(self.screen)
            self.screen.blit(self.ship.image, self.ship.rect)
            pygame.display.flip()


def main_menu(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if resume_x <= mouse_pos[0] <= resume_x + 640 and \
                        resume_y <= mouse_pos[1] <= resume_y + 360:
                    # screen.blit(resume_button, (0, 0))
                    game_screen = MainGameScreen(screen)
                    game_screen.run()
                    break
        mouse_pos = pygame.mouse.get_pos()
        # if start_x <= mouse_pos[0] <= start_x + 640 and \
        #         start_y <= mouse_pos[1] <= start_y + 360:
        #     screen.blit(start_button, (0, 0))
        # if resume_x <= mouse_pos[0] <= resume_x + 640 and \
        #         resume_y <= mouse_pos[1] <= resume_y + 360:
        #     screen.blit(resume_button, (0, 0))
        # elif settings_x <= mouse_pos[0] <= settings_x + 640 and \
        #         settings_y <= mouse_pos[1] <= settings_y + 360:
        #     screen.blit(settings_button, (0, 0))
        # else:
        screen.blit(background, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    start_x = 640
    start_y = SCREEN_HEIGHT // 3
    resume_x = 640
    resume_y = SCREEN_HEIGHT // 3 + 170
    settings_x = 640
    settings_y = SCREEN_HEIGHT // 3 + 400
    background = pygame.image.load('data/images/menu_2.png').convert()
    # start_button = pygame.image.load('data/images/menu_1_start.png').convert_alpha()
    # resume_button = pygame.image.load('data/images/menu_1_resume.png').convert_alpha()
    # settings_button = pygame.image.load('data/images/menu_1_settings.png').convert_alpha()
    main_menu(screen)