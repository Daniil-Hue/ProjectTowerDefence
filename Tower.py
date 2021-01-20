import pygame
import Core
import Enemy
import math

tower_group = pygame.sprite.Group()


def create_tower(spawn_base, tower_type, width, height):
    x = spawn_base.rect.x + (spawn_base.rect.width - width) / 2
    y = spawn_base.rect.y + (spawn_base.rect.height - height) / 2
    for i in Core.tower_types:
        if i[0] == tower_type:
            image = pygame.transform.scale(Core.load_image(i[3]), (width, height))
            damage = i[1]
            radius = i[2]
            bullet = i[4]
            break
    spawn_base.type = 'field'
    Tower(image, tower_type, damage, radius, x, y, bullet)


class Tower(pygame.sprite.Sprite):
    def __init__(self, image, tower_type, damage, radius, x, y, bullet_image):
        super().__init__(tower_group)
        self.bullet_image = bullet_image
        self.damage = damage
        self.radius = radius
        self.tower_type = tower_type
        self.image = image.copy()
        self.original_image = image
        self.rect = self.image.get_rect().move(x, y)
        self.position = x, y
        self.angle = 0
        self.nearest_enemy = None

    def update(self):
        for enemy in Enemy.enemy_group.sprites():
            x = enemy.rect.x + enemy.rect.width / 2
            y = enemy.rect.y + enemy.rect.height / 2
            if (x - self.rect.x) ** 2 + (y - self.rect.y) ** 2 <= self.radius ** 2:
                self.nearest_enemy = enemy
                self.rect.x = self.position[0]
                self.rect.y = self.position[1]
                self.angle = math.atan2(self.rect.x - x, self.rect.y - y) * (180 / math.pi)
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect.x = self.rect.x - (self.image.get_width() - self.rect.width) / 2
                self.rect.y = self.rect.y - (self.image.get_height() - self.rect.height) / 2
                break

    def shoot(self):
        if self.nearest_enemy not in Enemy.enemy_group.sprites():
            self.nearest_enemy = None
            return
        x, y = self.nearest_enemy.rect.x, self.nearest_enemy.rect.y
        if (x - self.rect.x) ** 2 + (y - self.rect.y) ** 2 <= self.radius ** 2:
            angle_rad = math.radians(self.angle)
            bullet_x = math.cos(angle_rad)
            bullet_y = math.sin(angle_rad)
            image = pygame.transform.rotate(Core.load_image(self.bullet_image), self.angle + 180)
            # bx = self.rect.centerx - bullet_x * self.original_image.get_width() // 2
            # by = self.rect.centery - bullet_y * self.original_image.get_height() // 2
            # bx = self.position[0] - self.image.get_width() / 2 - bullet_x * self.image.get_width() // 2
            # by = self.position[1] - self.image.get_height() / 2 - bullet_y * self.image.get_height() // 2
            Bullet(image,
                   self.rect.centerx,
                   self.rect.centery,
                   -bullet_x * 10,
                   -bullet_y * 10,
                   self.radius,
                   self.damage
                   )


bullet_group = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, shift_x, shift_y, max_distance, damage):
        super().__init__(bullet_group)
        self.type = type
        self.image = image
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.damage = damage
        self.max_distance = max_distance
        self.distance_per_step = math.sqrt(self.shift_x ** 2 + self.shift_y ** 2)
        self.rect = self.image.get_rect().move(x - image.get_width() / 2, y - image.get_height() / 2)

    def update(self):
        self.rect.x += self.shift_y
        self.rect.y += self.shift_x
        self.max_distance -= self.distance_per_step
        if self.max_distance <= 0:
            bullet_group.remove(self)
            return
        for i in Enemy.enemy_group.sprites():
            if self.rect.collidepoint(i.rect.center):
                i.health -= self.damage
                bullet_group.remove(self)
