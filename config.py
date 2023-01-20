import pygame

from design import colors

pygame.init()

# СПИСОК С ТЕКСТАМИ
texts = []

# СПИСОК С ПРЯМОУГОЛЬНИКАМИ ДЛЯ КНОПОК
rects = []


# КОНСТАНТЫ МОДОВ
PREGAME = 'pregame'  # МОД ПЕРЕД САМОЙ ПЕРВОЙ ИГРОЙ (ПУСТОЕ ПОЛЕ BOARD)
GAME = 'game'  # МОД ИГРЫ (ПАДАЮТ ФИУГРЫ)
PAUSE = 'pause'  # МОД ПАУЗЫ ВО ВРЕМЯ ИГРЫ (ФИГУРЫ НЕ ПАДАЮТ, ПОЛЕ БЛЕКЛОЕ)
LOSTGAME = 'lostgame'  # МОД ЗАКОНЧЕННОЙ ИГРЫ (ФИГУРЫ НЕ ПАДАЮТ ПОЛЕ БЛЕКЛОЕ, НАПИСАН СЧЕТ)

# ЗАГРУЗКА ЗВУКА
sound_delete_row = pygame.mixer.Sound("sounds/sound_delete_row.mp3")
sound_delete_row.set_volume(0.2)

sound_game_over = pygame.mixer.Sound("sounds/sound_game_over.mp3")
sound_game_over.set_volume(0.5)

sound_new_record = pygame.mixer.Sound("sounds/sound_new_record.mp3")
sound_new_record.set_volume(0.2)

sound_melody = pygame.mixer.Sound("sounds/sound_melody.mp3")
sound_melody.set_volume(0.04)

# СЛОВАРЬ С НОВЫМИ ПОЗИЦИЯМИ КЛЕТОК ПОСЛЕ ПОВОРОТА
new_poses = {
    '[-1, -1]': [-1, 1],
    '[-1, 1]': [1, 1],
    '[1, 1]': [1, -1],
    '[1, -1]': [-1, -1],
    '[-1, 0]': [0, 1],
    '[0, 1]': [1, 0],
    '[1, 0]': [0, -1],
    '[0, -1]': [-1, 0],
    '[0, 0]': [0, 0]
}


# СЛОВАРЬ С НОВЫМИ ПОЗИЦИЯМИ КЛЕТОК ПОСЛЕ ПОВОРОТА (ДЛИННАЯ ФИГУРА)
new_poses_long = {
    '[0, -2]': [2, 0],
    '[0, -1]': [1, 0],
    '[0, 0]': [0, 0],
    '[0, 1]': [-1, 0],
    '[2, 0]': [0, -2],
    '[1, 0]': [0, -1],
    '[-1, 0]': [0, 1]
}


# CЛОВАРЬ С НАЧАЛЬНЫМИ ИНДЕКСАМИ ВСЕХ ФИГУР НА ПОЛЕ BOARD
figures = {
    1: {'color': colors['красный'], 'indexes': [[1, 5], [1, 4], [0, 4], [0, 3]], 'central_index': [0, 4]},
    2: {'color': colors['оранжевый'], 'indexes': [[1, 5], [1, 4], [1, 3], [0, 5]], 'central_index': [1, 4]},
    3: {'color': colors['желтый'], 'indexes': [[1, 5], [1, 4], [0, 5], [0, 4]], 'central_index': [500, 20]},
    4: {'color': colors['зеленый'], 'indexes': [[1, 4], [1, 3], [0, 5], [0, 4]], 'central_index': [0, 4]},
    5: {'color': colors['голубой'], 'indexes': [[0, 6], [0, 5], [0, 4], [0, 3]], 'central_index': [0, 5]},
    6: {'color': colors['синий'], 'indexes': [[1, 5], [1, 4], [1, 3], [0, 3]], 'central_index': [1, 4]},
    7: {'color': colors['фиолетовый'], 'indexes': [[1, 5], [1, 4], [1, 3], [0, 4]], 'central_index': [1, 4]}
}


# СКОЛЬКО ОЧКОВ ДАЁТСЯ ЗА УДАЛЕНИЕ ЛИНИЙ ЗА РАЗ
line_score = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}
