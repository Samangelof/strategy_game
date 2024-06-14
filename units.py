import pygame
from load_images import (
    HERO_IDLE_RIGHT_IMAGES,
    HERO_IDLE_LEFT_IMAGES,
    HERO_RUN_RIGHT_IMAGES,
    HERO_RUN_LEFT_IMAGES,
    HERO_WALK_RIGHT_IMAGES,
    HERO_WALK_LEFT_IMAGES,
    HERO_DEAD_RIGHT_IMAGES,
    HERO_DEAD_LEFT_IMAGES,
    HERO_ATTACK_RIGHT_IMAGES,
    HERO_ATTACK_LEFT_IMAGES,
    ENEMY_IMAGE,
    KNIGHT_IDLE_RIGHT_IMAGES,
    KNIGHT_IDLE_LEFT_IMAGES,
    KNIGHT_RUN_RIGHT_IMAGES,
    KNIGHT_RUN_LEFT_IMAGES,
    KNIGHT_WALK_RIGHT_IMAGES,
    KNIGHT_WALK_LEFT_IMAGES,
    KNIGHT_DEAD_RIGHT_IMAGES,
    KNIGHT_DEAD_LEFT_IMAGES,
    KNIGHT_ATTACK_RIGHT_IMAGES,
    KNIGHT_ATTACK_LEFT_IMAGES
    
)
from combat import (
    handle_collisions, 
    resolve_collision, 
    attack, 
    check_combat
)
from config import screen, BLUE


class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, name, idle_images, walk_images, run_images, attack_images, image_size, battle_spirit=50):
        super().__init__()
        self.idle_images = [pygame.transform.scale(image, image_size) for image in idle_images]
        self.walk_images = [pygame.transform.scale(image, image_size) for image in walk_images]
        self.run_images = [pygame.transform.scale(image, image_size) for image in run_images]
        self.attack_images = [pygame.transform.scale(image, image_size) for image in attack_images]
        self.images = self.idle_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.selected = False
        self.target_pos = None
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.battle_spirit = battle_spirit
        self.attack_cooldown = 0
        self.animation_counter = 0
        self.direction = 'right'  # 'left' or 'right'
        self.selected_color = BLUE
        self.walking_speed = 1
        self.running_speed = 1.2
        self.is_running = False
        self.is_walking = False
        self.is_attacking = False
        self.collision_resolved = False 
        self.hp_bar_length = 50  # Длина полоски здоровья
        self.hp_bar_height = 5   # Высота полоски здоровья
        self.hp_bar_color = (0, 255, 0)       # Цвет полоски здоровья
        self.hp_bar_bg_color = (255, 0, 0)  # Цвет фона полоски здоровья
        self.dead_animation_counter = 0
        self.dead_animation_speed = 50  # Скорость анимации смерти

    def update(self):
        if self.hp <= 0:
            self.dead_animation()
            return
        
        if self.is_attacking:
            self.attack_animation()
            return

        self.animate()
        if self.target_pos:
            self.move_towards_target()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def dead_animation(self):
        self.dead_animation_counter += 1
        if self.dead_animation_counter >= len(self.dead_images) * self.dead_animation_speed:
            self.kill()
            return
        
        self.images = self.dead_images
        self.image_index = self.dead_animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]

    def attack_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= len(self.attack_images) * self.dead_animation_speed:
            self.is_attacking = False
            return
        
        self.images = self.attack_images
        self.image_index = self.animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]

    def handle_collisions(self, all_units, static_objects):
        handle_collisions(self, all_units, static_objects)

    def check_combat(self, all_units):
        check_combat(self, all_units)

    def attack(self, other_unit):
        attack(self, other_unit)

    def resolve_collision(self, other_unit):
        resolve_collision(self, other_unit)

    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= 30:  # значение скорости анимации
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

    def draw(self):
        if self.selected:
            pygame.draw.rect(screen, self.selected_color, self.rect, 3)
        
        # полоска здоровья
        hp_bar_width = int(self.hp / self.max_hp * self.hp_bar_length)
        pygame.draw.rect(screen, self.hp_bar_bg_color, (self.rect.centerx - self.hp_bar_length // 2, self.rect.y - 10, self.hp_bar_length, self.hp_bar_height))
        pygame.draw.rect(screen, self.hp_bar_color, (self.rect.centerx - self.hp_bar_length // 2, self.rect.y - 10, hp_bar_width, self.hp_bar_height))

        screen.blit(self.image, self.rect)

    
class Hero(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, HERO_IDLE_RIGHT_IMAGES, HERO_WALK_RIGHT_IMAGES, HERO_RUN_RIGHT_IMAGES, HERO_ATTACK_RIGHT_IMAGES, image_size)  # анимация стояния вправо по умолчанию
        self.level = level
        self.walk_images_right = [pygame.transform.scale(image, image_size) for image in HERO_WALK_RIGHT_IMAGES]
        self.walk_images_left = [pygame.transform.scale(image, image_size) for image in HERO_WALK_LEFT_IMAGES]
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in HERO_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in HERO_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in HERO_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in HERO_IDLE_RIGHT_IMAGES]
        self.dead_images_left = [pygame.transform.scale(image, image_size) for image in HERO_DEAD_LEFT_IMAGES]
        self.dead_images_right = [pygame.transform.scale(image, image_size) for image in HERO_DEAD_RIGHT_IMAGES]
        self.attack_images_left = [pygame.transform.scale(image, image_size) for image in HERO_ATTACK_LEFT_IMAGES]
        self.attack_images_right = [pygame.transform.scale(image, image_size) for image in HERO_ATTACK_RIGHT_IMAGES]

    def update(self):
        if self.hp <= 0:
            self.dead_animation()
            return
        
        if self.is_running:
            self.images = self.run_images_left if self.direction == 'left' else self.run_images_right
        elif self.target_pos:
            self.images = self.walk_images_left if self.direction == 'left' else self.walk_images_right
        elif self.is_attacking:
            self.images = self.attack_images_left if self.direction == 'left' else self.attack_images_right
        else:
            self.images = self.idle_images_left if self.direction == 'left' else self.idle_images_right
            
        super().update()
    
    def dead_animation(self):
        self.dead_animation_counter += 1
        if self.dead_animation_counter >= len(self.dead_images_left) * self.dead_animation_speed:
            self.kill()
            return
        
        self.images = self.dead_images_left if self.direction == 'left' else self.dead_images_right
        self.image_index = self.dead_animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]
    
    def dead_animation(self):
        self.dead_animation_counter += 1
        if self.dead_animation_counter >= len(self.dead_images_left) * self.dead_animation_speed:
            self.kill()
            return
        
        self.images = self.dead_images_left if self.direction == 'left' else self.dead_images_right
        self.image_index = self.dead_animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]


class Warrior(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, KNIGHT_IDLE_RIGHT_IMAGES, KNIGHT_WALK_RIGHT_IMAGES, KNIGHT_RUN_RIGHT_IMAGES, KNIGHT_ATTACK_RIGHT_IMAGES, image_size)  # анимация стояния вправо по умолчанию
        self.level = level
        self.walk_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_WALK_RIGHT_IMAGES]
        self.walk_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_WALK_LEFT_IMAGES]
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_RIGHT_IMAGES]
        self.dead_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_DEAD_LEFT_IMAGES]
        self.dead_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_DEAD_RIGHT_IMAGES]
        self.attack_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_ATTACK_LEFT_IMAGES]
        self.attack_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_ATTACK_RIGHT_IMAGES]

    def update(self):
        if self.hp <= 0:
            self.dead_animation()
            return
        
        if self.is_running:
            self.images = self.run_images_left if self.direction == 'left' else self.run_images_right
        elif self.target_pos:
            self.images = self.walk_images_left if self.direction == 'left' else self.walk_images_right
        elif self.is_attacking:
            self.images = self.attack_images_left if self.direction == 'left' else self.attack_images_right
        else:
            self.images = self.idle_images_left if self.direction == 'left' else self.idle_images_right
            
        super().update()
    
    def dead_animation(self):
        self.dead_animation_counter += 1
        if self.dead_animation_counter >= len(self.dead_images_left) * self.dead_animation_speed:
            self.kill()
            return
        
        self.images = self.dead_images_left if self.direction == 'left' else self.dead_images_right
        self.image_index = self.dead_animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]


class Enemy(Unit):
    def __init__(self, x, y, name, level, image_size=(43, 64)):
        super().__init__(x, y, name, KNIGHT_IDLE_RIGHT_IMAGES, KNIGHT_WALK_RIGHT_IMAGES, KNIGHT_RUN_RIGHT_IMAGES, KNIGHT_ATTACK_RIGHT_IMAGES, image_size)  
        self.level = level
        self.run_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_LEFT_IMAGES]
        self.run_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_RUN_RIGHT_IMAGES]
        self.idle_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_LEFT_IMAGES]
        self.idle_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_IDLE_RIGHT_IMAGES]
        self.dead_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_DEAD_LEFT_IMAGES]
        self.dead_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_DEAD_RIGHT_IMAGES]
        self.attack_images_left = [pygame.transform.scale(image, image_size) for image in KNIGHT_ATTACK_LEFT_IMAGES]
        self.attack_images_right = [pygame.transform.scale(image, image_size) for image in KNIGHT_ATTACK_RIGHT_IMAGES]
        self.is_running = False
        self.attack_cooldown = 0

    def update(self):
        if self.hp <= 0:
            self.dead_animation()
            return

        super().update()

    def dead_animation(self):
        self.dead_animation_counter += 1
        if self.dead_animation_counter >= len(self.dead_images_left) * self.dead_animation_speed:
            self.kill()
            return
        
        self.images = self.dead_images_left if self.direction == 'left' else self.dead_images_right
        self.image_index = self.dead_animation_counter // self.dead_animation_speed
        self.image = self.images[min(self.image_index, len(self.images) - 1)]