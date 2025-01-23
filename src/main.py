import sys
import pygame
from pygame.locals import *


class MainGameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bg_color = (0, 0, 0)
        self.ship = Ship(screen.get_width() // 2, screen.get_height() * 2 // 3)
        self.hearts = [
            GameObject('data/images/resized_heart.png', screen.get_width() - 350, 10),
            GameObject('data/images/resized_heart.png', screen.get_width() - 250, 10),
            GameObject('data/images/resized_heart.png', screen.get_width() - 150, 10)
        ]
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            self.ship.update(keys)
            self.screen.fill(self.bg_color)
            self.screen.blit(self.ship.image, self.ship.rect)
            for heart in self.hearts:
                self.screen.blit(heart.image, heart.rect)
            pygame.display.flip()
            self.clock.tick(60)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Ship(GameObject):
    def __init__(self, x, y):
        super().__init__('data/images/resized_ship.png', x, y)
        self.left_image = pygame.image.load('data/images/resized_ship_left.png')
        self.right_image = pygame.image.load('data/images/resized_ship_right.png')
        self.speed = 10
        self.direction = 'center'
    def update(self, keys):
        if keys[K_LEFT] or keys[K_a]:
            self.rect.x -= self.speed
            self.image = self.left_image
            self.direction = 'left'
        elif keys[K_RIGHT] or keys[K_d]:
            self.rect.x += self.speed
            self.image = self.right_image
            self.direction = 'right'
        elif keys[K_UP] or keys[K_w]:
            self.rect.y -= self.speed
            self.image = self.image
            self.direction = 'up'
        elif keys[K_DOWN] or keys[K_s]:
            self.rect.y += self.speed
            self.image = self.image
            self.direction = 'down'
        else:
            self.image = pygame.image.load('data/images/resized_ship.png')
            self.direction = 'center'
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT / 3:
            self.rect.top = SCREEN_HEIGHT / 3
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


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
                if start_x <= mouse_pos[0] <= start_x + 640 and \
                   start_y <= mouse_pos[1] <= start_y + 360:
                       game_screen = MainGameScreen(screen)
                       game_screen.run()
                       break
        mouse_pos = pygame.mouse.get_pos()
        if start_x <= mouse_pos[0] <= start_x + 640 and \
           start_y <= mouse_pos[1] <= start_y + 360:
               screen.blit(start_button, (0, 0))
        elif resume_x <= mouse_pos[0] <= resume_x + 640 and \
              resume_y <= mouse_pos[1] <= resume_y + 360:
               screen.blit(resume_button, (0, 0))
        elif settings_x <= mouse_pos[0] <= settings_x + 640 and \
              settings_y <= mouse_pos[1] <= settings_y + 360:
               screen.blit(settings_button, (0, 0))
        else:
            screen.blit(background, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    display_info = pygame.display.Info()
    max_resolution = display_info.current_w, display_info.current_h
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = max_resolution[0] - 100
    SCREEN_HEIGHT = max_resolution[1] - 100
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ThunderStrike")
    start_x = 640
    start_y = SCREEN_HEIGHT // 3
    resume_x = 640
    resume_y = SCREEN_HEIGHT // 3 + 170
    settings_x = 640
    settings_y = SCREEN_HEIGHT // 3 + 400
    background = pygame.image.load('data/images/menu_1.png').convert()
    start_button = pygame.image.load('data/images/menu_1_start.png').convert_alpha()
    resume_button = pygame.image.load('data/images/menu_1_resume.png').convert_alpha()
    settings_button = pygame.image.load('data/images/menu_1_settings.png').convert_alpha()
    main_menu(screen)
