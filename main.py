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
from utils import ClickTimer

pygame.init()


click_timer = ClickTimer()


all_sprites = pygame.sprite.Group()
player_units = pygame.sprite.Group()
enemy_units = pygame.sprite.Group()

hero = Hero(100, screen_height - 100, "Лорд", 4)
squad1 = Warrior(200, screen_height - 200, "Рыцарь 1", 1)
squad2 = Warrior(300, screen_height - 100, "Рыцарь 2", 2)

player_units.add(hero, squad1, squad2)
all_sprites.add(player_units)

enemy_hero = Enemy(screen_width - 100, 100, "Главарь банды", 3)
enemy_squad = Enemy(screen_width - 200, 200, "Головорез 1", 1)

enemy_units.add(enemy_hero, enemy_squad)
all_sprites.add(enemy_units)


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

    all_sprites.update()

    for unit in player_units:
        unit.handle_collisions(player_units)
        unit.check_combat(enemy_units)
    for unit in enemy_units:
        unit.handle_collisions(enemy_units)
        unit.check_combat(player_units)

    for unit in player_units.copy():
        if unit.hp <= 0:
            unit.kill()
    for unit in enemy_units.copy():
        if unit.hp <= 0:
            unit.kill()

    screen.fill(WHITE)
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