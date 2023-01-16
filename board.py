import pygame
import random

from config import figures, new_poses, new_poses_long, line_score, sound_delete_row
from design import cell_color


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        """
        0: Пустая клетка
        2: Мобильная клетка фигуры
        11-17: Статичная клетка фигуры
        """
        self.speed = 20
        self.level = 1
        self.score = 0
        self.lines = 0
        self.left = 20
        self.top = 50
        self.cell_size = 35
        self.last_index = None  # ИНДЕКС ПРЕДЫДУЩЕЙ ФИГУРЫ
        self.index = None  # ИНДЕКС ТЕКУЩЕЙ ФИГУРЫ
        self.next_index = self.next_index = random.randint(1, 7)  # ИНДЕКС СЛЕДУЮЩЕЙ ФИГУРЫ
        self.moving_indexes = None  # ИНДЕКСЫ ДВИГАЮЩИХСЯ КЛЕТОК
        self.current_color = None  # ЦВЕТ ТЕКУЩЕЙ ФИГУРЫ
        self.central_index = None  # ЦЕНТРАЛЬНЫЙ ИНДЕКС ТЕКУЩЕЙ ФИГУРЫ (ТОЧКА ВРАЩЕНИЯ)
        self.is_lost = False

    def render(self, scr):
        # БОЛЬШОЙ ПРЯМОУГОЛЬНИК
        pygame.draw.rect(scr, (150, 150, 150),
                         (self.left - 1, self.top - 1,
                          self.cell_size * self.width + 2, self.cell_size * self.height + 2), width=1)

        for x in range(self.width):
            for y in range(self.height):
                # ОТРИСОВКА ПОДВИЖНЫХ КЛЕТОК С ИНДЕКСОМ 2
                if self.board[y][x] == 2:
                    pygame.draw.rect(scr, self.current_color,
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))
                # ОТРИСОВКА НЕПОДВЖИНЫХ КЛЕТОК
                elif self.board[y][x] > 10:
                    pygame.draw.rect(scr, figures[self.board[y][x] - 10].get('color'),
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))
                # ОТРИСОВКА ФОНА ДЛЯ ПУСТЫХ КЛЕТОК
                else:
                    pygame.draw.rect(scr, cell_color,
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))

                # ГРАНИЦЫ ПОЛЯ
                pygame.draw.rect(scr, (185, 185, 185),
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

    def add_figure(self):
        #  ПОДБОР ИНДЕКСОВ ФИГУР
        self.last_index = self.index
        self.index = self.next_index
        while True:
            self.next_index = random.randint(1, 7)
            if self.next_index != self.index and self.next_index != self.last_index:
                break
        if self.can_move_to_coords(figures.get(self.index).get('indexes').copy()):
            self.moving_indexes = figures.get(self.index).get('indexes').copy()
            self.current_color = figures.get(self.index).get('color')
            self.central_index = figures.get(self.index).get('central_index')
            for mi in self.moving_indexes:
                self.board[mi[0]][mi[1]] = 2
        else:
            self.is_lost = True

    def update(self):
        if self.can_move_down():
            self.move_down()
        else:
            self.stop_move()
            self.check_full_rows()
            self.add_figure()

    def movement_down(self):
        if self.can_move_down():
            self.move_down()
            self.score += 1
        else:
            self.stop_move()

    def can_move_down(self):
        # ПРОВЕРКА КАЖДОЙ КЛЕТКИ НА СТОЛКНОВЕНИЕ
        for mi in self.moving_indexes:
            # ЕСЛИ ХОТЯ БЫ ОДНА КЛЕТКА НЕ ПРОШЛА ПРОВЕРКУ
            if not(mi[0] <= self.height - 2 and self.board[mi[0] + 1][mi[1]] < 11):
                return False
        return True

    def move_down(self):
        # СМЕЩЕНИЕ ИНДЕКСОВ НА 1 ВНИЗ
        self.central_index = [self.central_index[0] + 1, self.central_index[1]]
        for i in range(len(self.moving_indexes)):
            self.board[self.moving_indexes[i][0]][self.moving_indexes[i][1]] = 0
            self.moving_indexes[i] = [self.moving_indexes[i][0] + 1, self.moving_indexes[i][1]]
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 2

    def stop_move(self):
        # ОСТАНОВКА ДВЖИЕНИЯ
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 10 + self.index

    def movement_left(self):
        if self.can_move_left():
            self.move_left()

    def can_move_left(self):
        # ПРОВЕРКА КАЖДОЙ КЛЕТКИ НА СТОЛКНОВЕНИЕ
        for mi in self.moving_indexes:
            # ЕСЛИ ХОТЯ БЫ ОДНА КЛЕТКА НЕ ПРОШЛА ПРОВЕРКУ
            if not(mi[1] >= 1 and self.board[mi[0]][mi[1] - 1] < 11):
                return False
        return True

    def move_left(self):
        # СМЕЩЕНИЕ ИНДЕКСОВ НА 1 ВЛЕВО
        self.central_index = [self.central_index[0], self.central_index[1] - 1]
        for i in range(len(self.moving_indexes)):
            self.board[self.moving_indexes[i][0]][self.moving_indexes[i][1]] = 0
            self.moving_indexes[i] = [self.moving_indexes[i][0], self.moving_indexes[i][1] - 1]
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 2

    def movement_right(self):
        if self.can_move_right():
            self.move_right()

    def can_move_right(self):
        # ПРОВЕРКА КАЖДОЙ КЛЕТКИ НА СТОЛКНОВЕНИЕ
        for mi in self.moving_indexes:
            # ЕСЛИ ХОТЯ БЫ ОДНА КЛЕТКА НЕ ПРОШЛА ПРОВЕРКУ
            if not(mi[1] <= self.width - 2 and self.board[mi[0]][mi[1] + 1] < 11):
                return False
        return True

    def move_right(self):
        # СМЕЩЕНИЕ ИНДЕКСОВ НА 1 ВЛЕВО
        self.central_index = [self.central_index[0], self.central_index[1] + 1]
        for i in range(len(self.moving_indexes)):
            self.board[self.moving_indexes[i][0]][self.moving_indexes[i][1]] = 0
            self.moving_indexes[i] = [self.moving_indexes[i][0], self.moving_indexes[i][1] + 1]
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 2

    def rotate(self):
        new_coords, new_central_index = self.get_new_coords()
        if self.can_move_to_coords(new_coords):
            self.move_to_coords(new_coords, new_central_index)

    def get_new_coords(self):

        if self.index == 5:  # ЕСЛИ ДЛИННАЯ ФИГУРА
            return self.get_new_coords_long_figure()

        elif self.index == 3:  # ЕСЛИ КВАДРАТ
            return False, False

        else:  # ЕСЛИ ОСТАЛЬНЫЕ ФИГУРЫ
            return self.get_new_coords_other_figure()

    def get_new_coords_long_figure(self):
        if self.central_index[0] >= 18 or self.central_index[0] == 0:
            return False, False
        elif self.central_index[1] > 1 and self.central_index[1] != 9:  # ФИГУРА НЕ У КРАЁВ
            new_coords = self.moving_indexes.copy()
            new_central_index = self.central_index
        elif self.central_index[1] == 0:  # ФИГУРА У ЛЕВОГО КРАЯ
            new_coords = [[i[0], i[1] + 2] for i in self.moving_indexes]
            new_central_index = [self.central_index[0], self.central_index[1] + 2]
        elif self.central_index[1] == 1:  # ФИГУРА У ЛЕВОГО КРАЯ
            new_coords = [[i[0], i[1] + 1] for i in self.moving_indexes]
            new_central_index = [self.central_index[0], self.central_index[1] + 1]
        else:  # ФИУГРА У ПРАВОГО КРАЯ
            new_coords = [[i[0], i[1] - 1] for i in self.moving_indexes]
            new_central_index = [self.central_index[0], self.central_index[1] - 1]

        new_coords = [[i[0] - new_central_index[0], i[1] - new_central_index[1]] for i in new_coords]
        new_coords = [new_poses_long[str(i)] for i in new_coords]
        new_coords = [[i[0] + new_central_index[0], i[1] + new_central_index[1]] for i in new_coords]
        return new_coords, new_central_index

    def get_new_coords_other_figure(self):
        if self.central_index[0] == 19 or self.central_index[0] == 0 or self.central_index[0] > 100:
            return False, False
        elif self.central_index[1] != 0 and self.central_index[1] != 9:  # ФИГУРА НЕ У КРАЁВ
            new_coords = self.moving_indexes.copy()
            new_central_index = self.central_index
        elif self.central_index[1] == 0:  # ФИГУРА У ЛЕВОГО КРАЯ
            new_coords = [[i[0], i[1] + 1] for i in self.moving_indexes]
            new_central_index = [self.central_index[0], self.central_index[1] + 1]
        else:  # ФИУГРА У ПРАВОГО КРАЯ
            new_coords = [[i[0], i[1] - 1] for i in self.moving_indexes]
            new_central_index = [self.central_index[0], self.central_index[1] - 1]

        new_coords = [[i[0] - new_central_index[0], i[1] - new_central_index[1]] for i in new_coords]
        new_coords = [new_poses[str(i)] for i in new_coords]
        new_coords = [[i[0] + new_central_index[0], i[1] + new_central_index[1]] for i in new_coords]
        return new_coords, new_central_index

    def can_move_to_coords(self, coords):
        if not coords:
            return False
        for c in coords:
            if self.board[c[0]][c[1]] >= 11:
                return False
        return True

    def move_to_coords(self, coords, central_index):
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 0
        self.moving_indexes = coords
        self.central_index = central_index
        for i in self.moving_indexes:
            self.board[i[0]][i[1]] = 2

    def check_full_rows(self):
        # ПОЛУЧЕНИЯ ВСЕХ РЯДОВ ГДЕ СТОИТ ОСТАНОВИВШАЯСЯ ФИГУРА
        rows = sorted(list(set([i[0] for i in self.moving_indexes])))
        deleted_count = 0
        for row in rows:
            # ПРОВЕРКА ЗАПОЛНЕННОСТИ РЯДА
            for cell in self.board[row]:
                if cell == 0:
                    break
            # ЕСЛИ НЕТ ПУСТЫХ КЛЕТОК УДАЛЯЕТ РЯД
            else:
                self.delete_row(row)
                deleted_count += 1
                self.lines += 1
        if deleted_count != 0:
            self.score += self.level * line_score[deleted_count]
            sound_delete_row.play(0)

    def delete_row(self, row):
        # СДВИГ ВСЕХ РЯДОВ НАД УДАЛЯЕМЫМ НА 1 ВНИЗ
        for i in range(row, 0, -1):
            self.board[i] = self.board[i - 1].copy()

    def up_level(self):
        if self.speed > 2:
            self.speed -= 2
            self.level += 1


class NextFigureBoard:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 415
        self.top = 400
        self.cell_size = 35
        self.index = None  # ИНДЕКС ФИГУРЫ
        self.indexes = None  # ИНДЕКСЫ КЛЕТОК ФИГУРЫ
        self.color = None  # ЦВЕТ ФИГУРЫ

    def render(self, scr):
        # БОЛЬШОЙ ПРЯМОУГОЛЬНИК
        pygame.draw.rect(scr, (150, 150, 150),
                         (self.left - 1, self.top - 1,
                          self.cell_size * self.width + 2, self.cell_size * self.height + 2), width=1)

        for x in range(self.width):
            for y in range(self.height):
                # ОТРИСОВКА НЕПОДВЖИНЫХ КЛЕТОК
                if self.index and [y, x] in self.indexes:
                    pygame.draw.rect(scr, self.color,
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))
                # ОТРИСОВКА ФОНА ПУСТЫХ КЛЕТОК
                else:
                    pygame.draw.rect(scr, cell_color,
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))
                # ГРАНИЦЫ ПОЛЯ
                pygame.draw.rect(scr, (185, 185, 185),
                                 (self.left + x * self.cell_size, self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

    def update(self, index):
        if self.index != index:
            self.index = index
            self.color = figures[index].get('color')
            self.indexes = [[i[0], i[1] - 3] for i in figures[index].get('indexes').copy()]
