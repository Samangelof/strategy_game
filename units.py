import pygame
from load_images import (
    HERO_IDLE_RIGHT_IMAGES,
    HERO_IDLE_LEFT_IMAGES,
    HERO_RUN_RIGHT_IMAGES,
    HERO_RUN_LEFT_IMAGES,
    HERO_WALK_RIGHT_IMAGES,
    HERO_WALK_LEFT_IMAGES,
    ENEMY_IMAGE,
    KNIGHT_IDLE_RIGHT_IMAGES,
    KNIGHT_IDLE_LEFT_IMAGES,
    KNIGHT_RUN_RIGHT_IMAGES,
    KNIGHT_RUN_LEFT_IMAGES
)
from config import (screen, BLUE)


class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, name, idle_images, walk_images, run_images, image_size, battle_spirit=50):
        super().__init__()
        self.idle_images = [pygame.transform.scale(image, image_size) for image in idle_images]
        self.walk_images = [pygame.transform.scale(image, image_size) for image in walk_images]
        self.run_images = [pygame.transform.scale(image, image_size) for image in run_images]
        self.images = self.idle_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.selected = False
        self.target_pos = None
        self.name = name
        self.hp = 100
        self.battle_spirit = battle_spirit
        self.attack_cooldown = 0
        self.animation_counter = 0
        self.direction = 'right'  # 'left' or 'right'
        self.selected_color = BLUE
        self.walking_speed = 1.5
        self.running_speed = 2.4
        self.is_running = False
        self.is_walking = False

    def update(self):
        self.animate()
        if self.target_pos:
            self.move_towards_target()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= 10:  # можно изменять это значение для регулировки скорости анимации
            self.animation_counter = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        # обновляет изображения в зависимости от направления и состояния
        if self.is_running:
            self.images = self.run_images
        elif self.is_walking:
            self.images = self.walk_images
        else:
            self.images = self.idle_images

        if self.direction == 'left':
            self.images = [pygame.transform.flip(image, True, False) for image in self.images]

    def move_towards_target(self):
        if self.target_pos:
            target_x, target_y = self.target_pos
            dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance < 5:
                self.target_pos = None
                self.is_walking = False
                self.is_running = False
            else:
                dx, dy = dx / distance, dy / distance
                speed = self.running_speed if self.is_running else self.walking_speed
                self.rect.x += dx * speed
                self.rect.y += dy * speed
                self.direction = 'left' if dx < 0 else 'right'

    def handle_collisions(self, all_units):
        for unit in all_units:
            if unit is not self and self.rect.colliderect(unit.rect):
                self.resolve_collision(unit)

    def resolve_collision(self, other_unit):
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
            other_unit.hp -= 10
            self.attack_cooldown = 30

    def check_combat(self, all_units):
        for unit in all_units:
            if unit is not self and self.rect.colliderect(unit.rect):
                self.attack(unit)
    
    def draw(self):
        if self.selected:
            pygame.draw.rect(screen, self.selected_color, self.rect, 3)
        screen.blit(self.image, self.rect)


class Hero(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, HERO_IDLE_RIGHT_IMAGES, HERO_WALK_RIGHT_IMAGES, HERO_RUN_RIGHT_IMAGES, image_size)  # анимация стояния вправо по умолчанию
        self.level = level
        self.walk_images_right = [pygame.transform.scale(image, image_size) for image in HERO_WALK_RIGHT_IMAGES]
        self.walk_images_left = [pygame.transform.scale(image, image_size) for image in HERO_WALK_LEFT_IMAGES]
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in HERO_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in HERO_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in HERO_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in HERO_IDLE_RIGHT_IMAGES]
        self.is_running = False

    def update(self):
        # Устанавливаем соответствующие изображения в зависимости от состояния и направления
        if self.is_running:
            self.images = self.run_images_left if self.direction == 'left' else self.run_images_right
        elif self.target_pos:
            self.images = self.walk_images_left if self.direction == 'left' else self.walk_images_right
        else:
            self.images = self.idle_images_left if self.direction == 'left' else self.idle_images_right
            
        super().update()


class Warrior(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, KNIGHT_IDLE_RIGHT_IMAGES, HERO_WALK_RIGHT_IMAGES, KNIGHT_RUN_RIGHT_IMAGES, image_size)  # анимация стояния вправо по умолчанию
        self.level = level
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_RIGHT_IMAGES]
        self.is_running = False

    def update(self):
        if self.target_pos:
            self.images = self.run_images_left if self.direction == 'left' else self.run_images_right
        else:
            self.images = self.idle_images_left if self.direction == 'left' else self.idle_images_right

        super().update()


class Enemy(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, KNIGHT_IDLE_RIGHT_IMAGES, HERO_WALK_RIGHT_IMAGES, KNIGHT_RUN_RIGHT_IMAGES, image_size)  # анимация стояния вправо по умолчанию
        self.level = level
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_RIGHT_IMAGES]
        self.is_running = False

    def update(self):
        pass
    