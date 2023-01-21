import pygame
import os
import sys
import random

from design import fon_color

pygame.init()
screen_rect = (20, 50, 350, 700)
GRAVITY = 2


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pygame.display.set_caption('Tetris')
    size = 600, 800
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    intro_text = ["TETRIS",
                  "Правила:",
                  "Стрелка влево - Движение влево",
                  "Стрелка вправо - Движение вправо",
                  "Стрелка вверх - Вращение фигуры",
                  "Стрекла вниз - Ускоренное движение вниз",
                  "Фигуры выстраиваются друг на друга.",
                  "Если ряд заполняется, то он удаляется.",
                  "Игра завершается по достижении верхнего ряда.",
                  "Цель - набрать как можно больше очков.",
                  "Очки начисляются за удаленные линии.",
                  "",
                  "При побитии рекорды будет воспризведён звуковой эффект",
                  "с анимацией в виде звёдочек."]
    screen.fill(fon_color)
    font = pygame.font.SysFont('calibri', 82, bold=True)
    string_rendered = font.render(intro_text[0], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 180
    screen.blit(string_rendered, intro_rect)
    font = pygame.font.SysFont('calibri', 28)
    text_coord = 300
    for line in intro_text[1:]:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def end_screen(cur):
    pygame.display.set_caption('Tetris')
    size = 600, 800
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    screen.fill(fon_color)
    font = pygame.font.SysFont('calibri', 56)
    string_rendered = font.render('РЕКОРДЫ', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 190
    screen.blit(string_rendered, intro_rect)
    records = sorted([i[0] for i in cur.execute("""SELECT score FROM records""").fetchall()], reverse=True)
    font = pygame.font.SysFont('calibri', 32)
    text_coord = 200
    for i in range(len(records)):
        if i == 9:
            string_rendered = font.render(f'{i + 1}.   {records[i]}', True, pygame.Color('black'))
        else:
            string_rendered = font.render(f'{i + 1}.     {records[i]}', True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 190
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


def create_particles(sprites):
    particle_count = 50
    # возможные скорости
    numbers = list(range(-5, 6))
    numbers.pop(5)
    for _ in range(particle_count):
        Particle((195, 250), random.choice(numbers), random.choice(numbers), sprites)


class Particle(pygame.sprite.Sprite):

    def __init__(self, pos, dx, dy, sprites):
        self.fire = [load_image("star.png")]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        super().__init__(sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
