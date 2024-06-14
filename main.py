import pygame
import sys
from interface import draw_ui
from config import (
    screen,
    screen_height,
    screen_width,
    WHITE,
    LIGHT_BLUE,
)
from units import (
    Hero,
    Warrior,
    Enemy
)
from load_images import LANDSCAPE
from utils import ClickTimer
from objects import static_objects


pygame.init()

click_timer = ClickTimer()

all_sprites = pygame.sprite.Group()
player_units = pygame.sprite.Group()
enemy_units = pygame.sprite.Group()

hero = Hero(100, screen_height - 100, "Лорд", 4)
squad1 = Warrior(200, screen_height - 200, "Рыцарь 1", 1)
squad2 = Warrior(300, screen_height - 100, "Рыцарь 2", 2)

player_units.add(hero, squad1, squad2)
all_sprites.add(hero, squad1, squad2)

enemy_hero = Enemy(screen_width - 100, 100, "Главарь банды", 3)
enemy_squad = Enemy(screen_width - 200, 200, "Головорез 1", 1)

enemy_units.add(enemy_hero, enemy_squad)
all_sprites.add(enemy_hero, enemy_squad)


# Загружаем изображения объектов
all_sprites.add(static_objects)


selecting = False
start_pos = None
end_pos = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selecting = True
                start_pos = event.pos
                end_pos = event.pos
            elif event.button == 3:
                pos = pygame.mouse.get_pos()
                is_double_click = click_timer.is_double_click()
                for unit in player_units:
                    if unit.selected:
                        unit.target_pos = pos
                        unit.is_running = is_double_click  # Бег, если двойной клик
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selecting = False
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos
                select_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                if not pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    for unit in player_units:
                        unit.selected = False
                for unit in player_units:
                    if select_rect.colliderect(unit.rect):
                        unit.selected = True
        if event.type == pygame.MOUSEMOTION:
            if selecting:
                end_pos = event.pos

    # Обновление всех спрайтов
    all_sprites.update()
    player_units.update()
    enemy_units.update()

    # Обработка коллизий и боя
    for unit in player_units:
        unit.update()
        unit.handle_collisions(player_units, static_objects)
        unit.check_combat(enemy_units)

    for unit in enemy_units:
        unit.update()
        unit.handle_collisions(enemy_units, static_objects)
        unit.check_combat(player_units)

    # Удаление юнитов с нулевым здоровьем
    for unit in player_units.copy():
        if unit.hp <= 0:
            unit.update()  # Обновляем юнита для анимации смерти
    for unit in enemy_units.copy():
        if unit.hp <= 0:
            unit.update()  

    # Отрисовка на экране
    screen.blit(LANDSCAPE, (0, 0))
    all_sprites.draw(screen)

    for unit in player_units:
        if unit.selected:
            unit.draw()

    if selecting and start_pos and end_pos:
        x1, y1 = start_pos
        x2, y2 = end_pos
        select_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, LIGHT_BLUE, select_rect, 2)

    selected_units = [unit for unit in player_units if unit.selected]
    draw_ui(selected_units)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
