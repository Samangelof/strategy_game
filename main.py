import pygame
import sys
from interface import draw_ui
from config import (
    screen,
    screen_height,
    screen_width,
    WHITE,
    RED,
    GREEN,
    BLUE,
    LIGHT_BLUE
)

pygame.init()

HERO_IMAGE = pygame.image.load('images/hero.png')
WARRIOR_IMAGE = pygame.image.load('images/soldier.png')
ENEMY_IMAGE = pygame.image.load('images/enemy_soldier.png')

# главный класс для юнита
class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, image_size, battle_spirit=50):
        super().__init__()
        self.original_image = pygame.transform.scale(image, image_size)  # исходное изображение
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.selected = False
        self.target_pos = None
        self.name = name
        self.hp = 100  # начальное значение здоровья
        self.battle_spirit = battle_spirit  # начальное значение боевого духа
        self.attack_cooldown = 0  # Время до следующей атаки

    def update(self):
        if self.selected:
            self.image = self.original_image.copy()
            pygame.draw.rect(self.image, GREEN, self.image.get_rect(), 3)  # рамка вокруг юнита
        else:
            self.image = self.original_image.copy()  # восстанавливаем исходное изображение

        if self.target_pos:
            self.move_towards_target()

        # уменьшаем время до следующей атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def move_towards_target(self):
        if self.target_pos:
            target_x, target_y = self.target_pos
            dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5

            if distance < 5:
                self.target_pos = None
            else:
                dx, dy = dx / distance, dy / distance
                self.rect.x += dx * 3  # скорость перемещения юнита
                self.rect.y += dy * 3

    def handle_collisions(self, all_units):
        for unit in all_units:
            if unit is not self and self.rect.colliderect(unit.rect):
                self.resolve_collision(unit)

    def resolve_collision(self, other_unit):
        # метод для разрешения столкновений, чтобы юниты не перекрывали друг друга
        overlap_x = self.rect.right - other_unit.rect.left if self.rect.centerx < other_unit.rect.centerx else other_unit.rect.right - self.rect.left
        overlap_y = self.rect.bottom - other_unit.rect.top if self.rect.centery < other_unit.rect.centery else other_unit.rect.bottom - self.rect.top

        if abs(overlap_x) < abs(overlap_y):
            if self.rect.centerx < other_unit.rect.centerx:
                self.rect.right = other_unit.rect.left
            else:
                self.rect.left = other_unit.rect.right
        else:
            if self.rect.centery < other_unit.rect.centery:
                self.rect.bottom = other_unit.rect.top
            else:
                self.rect.top = other_unit.rect.bottom

    def attack(self, other_unit):
        if self.attack_cooldown <= 0:
            other_unit.hp -= 10  # наносим 10 единиц урона
            self.attack_cooldown = 30  # время до следующей атаки

    def check_combat(self, all_units):
        for unit in all_units:
            if unit is not self and self.rect.colliderect(unit.rect):
                self.attack(unit)


class Hero(Unit):
    def __init__(self, x, y, name, level, image_size=(27, 43)):
        super().__init__(x, y, name, HERO_IMAGE, image_size)
        self.level = level

class Warrior(Unit):
    def __init__(self, x, y, name, level, image_size=(25, 38)):
        super().__init__(x, y, name, WARRIOR_IMAGE, image_size)
        self.level = level

class Enemy(Unit):
    def __init__(self, x, y, name, battle_spirit=70, image_size=(24, 38)):
        # повернуть изображение в другу сторону по горизонтали
        flipped_image = pygame.transform.flip(ENEMY_IMAGE, True, False)
        super().__init__(x, y, name, flipped_image, image_size, battle_spirit)


# создание групп спрайтов
all_sprites = pygame.sprite.Group()
player_units = pygame.sprite.Group()
enemy_units = pygame.sprite.Group()

# создание героя игрока и двух отрядов пехоты
hero = Hero(100, screen_height - 100, "Центурион", 4)
squad1 = Warrior(200, screen_height - 200, "Гастат 1", 1)
squad2 = Warrior(300, screen_height - 100, "Гастат 2", 2)

player_units.add(hero, squad1, squad2)
all_sprites.add(player_units)

# создание главного героя противников и одного отряда пехоты
enemy_hero = Enemy(screen_width - 100, 100, "Главарь банды")
enemy_squad = Enemy(screen_width - 200, 200, "Головорез 1")

enemy_units.add(enemy_hero, enemy_squad)
all_sprites.add(enemy_units)

# переменные для прямоугольника выделения
selecting = False
start_pos = None
end_pos = None

# основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                selecting = True
                start_pos = event.pos
                end_pos = event.pos
            elif event.button == 3:  # правая кнопка мыши
                pos = pygame.mouse.get_pos()
                for unit in player_units:
                    if unit.selected:
                        unit.target_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # левая кнопка мыши
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

    # обновление спрайтов
    all_sprites.update()

    # обработка столкновений
    for unit in player_units:
        unit.handle_collisions(player_units)
        unit.check_combat(enemy_units)
    for unit in enemy_units:
        unit.handle_collisions(enemy_units)
        unit.check_combat(player_units)

    # удаление юнитов с нулевым здоровьем
    for unit in player_units.copy():
        if unit.hp <= 0:
            unit.kill()
    for unit in enemy_units.copy():
        if unit.hp <= 0:
            unit.kill()

    # отрисовка
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # отрисовка прямоугольника выделения
    if selecting and start_pos and end_pos:
        x1, y1 = start_pos
        x2, y2 = end_pos
        select_rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, LIGHT_BLUE, select_rect, 2)

    # отрисовка интерфейса
    selected_units = [unit for unit in player_units if unit.selected]
    draw_ui(selected_units)

    # обновление экрана
    pygame.display.flip()

    # ограничение FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
