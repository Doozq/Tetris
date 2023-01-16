import pygame
import sys
import sqlite3

from board import Board, NextFigureBoard
from config import PREGAME, GAME, PAUSE, LOSTGAME, RECORDS, rects, texts, sound_melody, sound_game_over
from design import buttons_color, fon_color, s

# ИНИЦИАЛИЗАЦИЯ PYGAME
pygame.init()

# ПОДКЛЮЧЕНИЕ БД
con = sqlite3.connect("database/records.sqlite")
cur = con.cursor()


def terminate():
    con.close()
    pygame.quit()
    sys.exit()


def render_static_text():
    menu_text = ['Новая игра', 'Пауза', 'Рекорды']

    font = pygame.font.SysFont('calibri', 34)
    text_coord = 85
    for line in menu_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 16
        intro_rect.top = text_coord
        intro_rect.x = 405
        text_coord += intro_rect.height
        texts.append((string_rendered, intro_rect))
        rec = intro_rect.copy()
        rec.top -= 8
        rec.height += 16
        rec.x -= 12
        rec.width = 185
        rects.append(rec)

    font = pygame.font.SysFont('calibri', 20)
    string_rendered = font.render('Следующая фигура:', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 350
    intro_rect.x = 405
    texts.append((string_rendered, intro_rect))

    font = pygame.font.SysFont('calibri', 48)
    string_rendered = font.render('ПАУЗА', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 150
    intro_rect.x = 130
    texts.append((string_rendered, intro_rect))

    string_rendered = font.render('РЕКОРДЫ', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 100
    texts.append((string_rendered, intro_rect))

    font = pygame.font.SysFont('calibri', 48, bold=True)
    string_rendered = font.render('ВЫ ПРОИГРАЛИ', True, pygame.Color(213, 40, 37))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 150
    intro_rect.x = 30
    texts.append((string_rendered, intro_rect))

    font = pygame.font.SysFont('calibri', 34)
    string_rendered = font.render('СЧЁТ', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 350
    intro_rect.x = 160
    texts.append((string_rendered, intro_rect))

    texts.append(0)


def render_score(score):
    font = pygame.font.SysFont('calibri', 38, bold=True)
    string_rendered = font.render(str(score), True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 400
    intro_rect.x = (350 - intro_rect.width) // 2 + 20
    texts[8] = (string_rendered, intro_rect)


def render_text():
    font = pygame.font.SysFont('calibri', 24)
    text_coord = 635
    for line in [f'Очки: {board.score}', f'Линии: {board.lines}', f'Уровень: {board.level}']:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 405
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def update_text():
    render_text()
    for rect in rects:
        pygame.draw.rect(screen, buttons_color, rect)
        pygame.draw.rect(screen, (142, 142, 142), rect, width=3)
    for text in texts[:4]:
        screen.blit(text[0], text[1])


def is_clicked_new_game(pos):
    rect = rects[0]
    if rect.x <= pos[0] <= rect.x + rect.width and rect.top <= pos[1] <= rect.top + rect.height:
        return True


def is_clicked_pause(pos):
    rect = rects[1]
    if rect.x <= pos[0] <= rect.x + rect.width and rect.top <= pos[1] <= rect.top + rect.height:
        return True


def is_clicked_records(pos):
    rect = rects[2]
    if rect.x <= pos[0] <= rect.x + rect.width and rect.top <= pos[1] <= rect.top + rect.height:
        return True


def pause_mode():
    screen.blit(s, (20, 50))
    screen.blit(texts[4][0], texts[4][1])


def lostgame_mode():
    screen.blit(s, (20, 50))
    screen.blit(texts[6][0], texts[6][1])
    screen.blit(texts[7][0], texts[7][1])
    screen.blit(texts[8][0], texts[8][1])


def records_mode():
    screen.blit(s, (20, 50))
    screen.blit(texts[5][0], texts[5][1])
    records = sorted([i[0] for i in cur.execute("""SELECT score FROM records""").fetchall()], reverse=True)
    font = pygame.font.SysFont('calibri', 32)
    text_coord = 180
    for i in range(len(records)):
        if i == 9:
            string_rendered = font.render(f'{i + 1}.   {records[i]}', True, pygame.Color('black'))
        else:
            string_rendered = font.render(f'{i + 1}.     {records[i]}', True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


if __name__ == '__main__':
    # НАСТРОЙКИ ОКНА
    pygame.display.set_caption('Tetris')
    size = width, height = 600, 800
    screen = pygame.display.set_mode(size)
    render_static_text()
    FPS = 60
    fps_counter = 0
    clock = pygame.time.Clock()
    board = Board(10, 20)
    next_figure_board = NextFigureBoard(4, 2)
    mode = PREGAME
    last_mode = PREGAME
    sound_melody.play(-1)
    running = True

    # ОСНОВНОЙ ЦИКЛ
    while running:
        # ПРОВЕРКА НА ПРОИГРЫШ
        if board.is_lost and mode == GAME:
            mode = LOSTGAME
            render_score(board.score)
            # ДОБАВЛЕНИЕ РЕЗУЛЬТАТА В БАЗУ ДАННЫХ
            lst = sorted(list(cur.execute("""SELECT * FROM records""").fetchall()), key=lambda x: x[0], reverse=True)
            if len(lst) == 10 and lst[9][0] < board.score:
                cur.execute(f"""UPDATE records SET 
                    score = {board.score} 
                        WHERE id = {lst[9][1]}""")
            con.commit()
            sound_game_over.play()

        # ОБРАБОТКА СОБЫТИЙ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # СОБЫТИЯ КЛАВИАТУРЫ
            if event.type == pygame.KEYDOWN and mode == GAME:
                if event.key == pygame.K_LEFT:
                    board.movement_left()
                if event.key == pygame.K_RIGHT:
                    board.movement_right()
                if event.key == pygame.K_UP:
                    board.rotate()
                if event.key == pygame.K_DOWN:
                    board.movement_down()

            # СОБЫИТЯ МЫШИ
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_clicked_new_game(event.pos):
                    if mode == PREGAME:
                        board.add_figure()
                    else:
                        board = Board(10, 20)
                        board.add_figure()
                        next_figure_board = NextFigureBoard(4, 2)
                        fps_counter = 0
                    mode = 'game'
                elif is_clicked_pause(event.pos):
                    if mode == GAME:
                        mode = PAUSE
                    elif mode == PAUSE:
                        mode = GAME
                elif is_clicked_records(event.pos):
                    if mode == PREGAME or mode == LOSTGAME:
                        last_mode = mode
                        mode = RECORDS
                    elif mode == RECORDS:
                        mode = last_mode

        screen.fill(fon_color)

        if mode == GAME:
            # СЧЁТ ФПС И ОБНОВЛЕНИЕ КООРДИНАТ ДЛЯ ИГРОВОГО МОДА
            fps_counter += 1
            if fps_counter % board.speed == 0:
                board.update()
                next_figure_board.update(board.next_index)

        if fps_counter == 1800:
            board.up_level()
            fps_counter = 0

        update_text()
        board.render(screen)
        next_figure_board.render(screen)
        if mode == PAUSE:
            pause_mode()
        elif mode == LOSTGAME:
            lostgame_mode()
        elif mode == RECORDS:
            records_mode()
        pygame.display.flip()
        clock.tick(FPS)
    terminate()
