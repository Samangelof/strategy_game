from objects import StaticObject


def handle_collisions(unit, all_units, static_objects):
    for other_unit in all_units:
        if other_unit is not unit and unit.rect.colliderect(other_unit.rect):
            resolve_collision(unit, other_unit)
    for obj in static_objects:
        if unit.rect.colliderect(obj.rect):
            resolve_collision(unit, obj)

def resolve_collision(unit, other):
    if isinstance(other, StaticObject):
        overlap_x = unit.rect.right - other.rect.left if unit.rect.centerx < other.rect.centerx else other.rect.right - unit.rect.left
        overlap_y = unit.rect.bottom - other.rect.top if unit.rect.centery < other.rect.centery else other.rect.bottom - unit.rect.top
    else:
        overlap_x = unit.rect.right - other.rect.left if unit.rect.centerx < other.rect.centerx else other.rect.right - unit.rect.left
        overlap_y = unit.rect.bottom - other.rect.top if unit.rect.centery < other.rect.centery else other.rect.bottom - unit.rect.top

    if abs(overlap_x) < abs(overlap_y):
        if unit.rect.centerx < other.rect.centerx:
            unit.rect.right = other.rect.left
        else:
            unit.rect.left = other.rect.right
    else:
        if unit.rect.centery < other.rect.centery:
            unit.rect.bottom = other.rect.top
        else:
            unit.rect.top = other.rect.bottom

    # Изменение цели для обхода препятствия
    if isinstance(other, StaticObject):
        if abs(overlap_x) > abs(overlap_y):
            unit.target_pos = (unit.rect.centerx, unit.rect.centery + (-20 if unit.rect.centery < other.rect.centery else 20))
        else:
            unit.target_pos = (unit.rect.centerx + (-20 if unit.rect.centerx < other.rect.centerx else 20), unit.rect.centery)
    else:
        if abs(overlap_x) > abs(overlap_y):
            unit.target_pos = (unit.rect.centerx, unit.rect.centery + (-20 if unit.rect.centery < other.rect.centery else 20))
        else:
            unit.target_pos = (unit.rect.centerx + (-20 if unit.rect.centerx < other.rect.centerx else 20), unit.rect.centery)

def attack(unit, other_unit):
    if unit.attack_cooldown <= 0:
        unit.is_attacking = True
        other_unit.hp -= 10  # 10 единиц урона
        unit.attack_cooldown = 30  # время до следующей атаки

def check_combat(unit, all_units):
    for other_unit in all_units:
        if other_unit is not unit and unit.rect.colliderect(other_unit.rect):
            attack(unit, other_unit)