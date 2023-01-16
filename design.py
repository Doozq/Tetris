import pygame

# ЦВЕТ ФОНА
fon_color = (229, 228, 226)

# ЦВЕТ ФОНА КНОПОК
buttons_color = (213, 212, 210)

# ЦВЕТ ФОНА КЛЕТОК
cell_color = (30, 30, 30)

# ЦВЕТА ФИГУР
colors = {
    'красный': pygame.Color(192, 19, 2),
    'оранжевый': pygame.Color(238, 129, 0),
    'желтый': pygame.Color(251, 208, 32),
    'зеленый': pygame.Color(39, 144, 0),
    'голубой': pygame.Color(0, 205, 223),
    'синий': pygame.Color(0, 0, 205),
    'фиолетовый': pygame.Color(145, 2, 172),
}

# ПОЛУПРОЗРАЧНЫЙ ХОЛСТ
s = pygame.Surface((350, 700), pygame.SRCALPHA)
s.fill((237, 237, 237, 200))
