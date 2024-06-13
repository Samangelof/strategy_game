import pygame

# отслеживания времени между нажатиями
class ClickTimer:
    def __init__(self, interval=500):  # Интервал в миллисекундах
        self.last_click = 0
        self.interval = interval

    def is_double_click(self):
        now = pygame.time.get_ticks()
        if now - self.last_click < self.interval:
            self.last_click = 0  # сбросить, чтобы не регистрировать тройные клики как два двойных
            return True
        self.last_click = now
        return False
