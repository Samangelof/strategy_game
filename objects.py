import pygame
import random
from load_images import (
    BUILDING_IMAGE,
    TREE_IMAGE,
    ROCK_IMAGE
)

class StaticObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, image_size):
        super().__init__()
        self.image = pygame.transform.scale(image, image_size)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def create_static_objects(object_images, predefined_coords, image_size=(64, 64)):
    objects_group = pygame.sprite.Group()
    for coord in predefined_coords:
        x, y = coord
        image = random.choice(object_images)
        obj = StaticObject(x, y, image, image_size)
        objects_group.add(obj)
    return objects_group


object_images = [BUILDING_IMAGE, TREE_IMAGE, ROCK_IMAGE]
predefined_coords = [
    (150, 150), 
    (200, 200), 
    (300, 300), 
    (450, 450),
    (500, 500)]
static_objects = create_static_objects(object_images, predefined_coords)
