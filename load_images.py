import pygame
import os

# стояние
HERO_IDLE_RIGHT_IMAGES = [pygame.image.load(f'assets/Knight_1/Idle/Idle_{i}.png') for i in range(1, 5)]
HERO_IDLE_LEFT_IMAGES = [pygame.image.load(f'assets/Knight_1/Idle/Idle_left_{i}.png') for i in range(1, 5)]

# бег
HERO_RUN_RIGHT_IMAGES = [pygame.image.load(f'assets/Knight_1/Run/Run_{i}.png') for i in range(1, 7)]
HERO_RUN_LEFT_IMAGES = [pygame.image.load(f'assets/Knight_1/Run/Run_left_{i}.png') for i in range(1, 7)]

# пешком
HERO_WALK_RIGHT_IMAGES = [pygame.image.load(f'assets/Knight_1/Walk/Walk_{i}.png') for i in range(1, 8)]
HERO_WALK_LEFT_IMAGES = [pygame.image.load(f'assets/Knight_1/Walk/Walk_left_{i}.png') for i in range(1, 8)]







KNIGHT_IDLE_RIGHT_IMAGES = [pygame.image.load(f'assets/Knight_1/Idle/Idle_{i}.png') for i in range(1, 5)]
KNIGHT_IDLE_LEFT_IMAGES = [pygame.image.load(f'assets/Knight_1/Idle/Idle_left_{i}.png') for i in range(1, 5)]



KNIGHT_RUN_RIGHT_IMAGES = [
    pygame.image.load(f'assets/Knight_1/Run/Run_{i}.png') for i in range(1, 7)
]
KNIGHT_RUN_LEFT_IMAGES = [
    pygame.image.load(f'assets/Knight_1/Run/Run_left_{i}.png') for i in range(1, 7)
]

# WARRIOR_IMAGE = pygame.image.load('images/soldier.png')
ENEMY_IMAGE = pygame.image.load('images/enemy_soldier.png')