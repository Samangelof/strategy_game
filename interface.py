import pygame
from config import (
    screen,
    screen_height,
    screen_width,
    WHITE,
    BLACK,
    font,
    ui_height
)

# загрузка изображения для представления здоровья
hp_icon = pygame.transform.scale(pygame.image.load('images/hp_icon.png'), (40, 40))
bs_icon = pygame.transform.scale(pygame.image.load('images/battle_spirit.png'), (30, 30))

def draw_ui(selected_units):
    # рисуем прямоугольник для интерфейса с границами
    pygame.draw.rect(screen, BLACK, (0, screen_height, screen_width, ui_height), 2)
    pygame.draw.rect(screen, WHITE, (2, screen_height + 2, screen_width - 4, ui_height - 4))

    if selected_units:
        # задаем начальную позицию для первой строки таблицы
        x_pos = 10
        y_pos = screen_height + 10

        # увеличиваем y_pos на высоту строки, чтобы начать рисовать следующие строки ниже
        y_pos += 30

        # рисуем данные о выбранных юнитах
        for unit in selected_units:
            # имя юнита
            text_surface = font.render(unit.name, True, BLACK)
            screen.blit(text_surface, (x_pos, y_pos))
            
            #здоровье юнита
            text_surface = font.render(str(unit.hp), True, BLACK)
            screen.blit(text_surface, (x_pos + 180, y_pos + 10))
            
            # боевой дух юнита
            text_surface = font.render(str(unit.battle_spirit), True, BLACK)
            screen.blit(text_surface, (x_pos + 300, y_pos + 10))
            
            # увеличивает y_pos на высоту строки, чтобы перейти к следующей строке
            y_pos += 30

        # отображаем иконку здоровья
        screen.blit(hp_icon, (x_pos + 180, screen_height + 10))
        # отображаем иконку боевого духа
        screen.blit(bs_icon, (x_pos + 300, screen_height + 10))
    else:
        pass    # не выбран ни один юнит