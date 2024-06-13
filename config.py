import pygame

# 1 - Гастаты
# 2 - Принципы
# 3 - Триарии
# 4 - Центурионы
# 5 - Рекс

# настройки экрана
screen_width = 1200
screen_height = 600
ui_height = 100  # высота интерфейса в нижней части экрана
screen = pygame.display.set_mode((screen_width, screen_height + ui_height))
pygame.display.set_caption("Стратегия на Pygame")

# цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (173, 216, 230)  # цвет выделения
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
# шрифт
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)