import pygame
import Core
import Map

enemy_group = pygame.sprite.Group()
spawn_delays = dict()


def spawn_enemy(type):
    spawn_x, spawn_y = 0, 0
    for i in Map.tiles_group.sprites():
        if i.type == 'spawn':
            spawn_x = i.rect.x + i.rect.width // 2
            spawn_y = i.rect.y + i.rect.height // 2
    if not spawn_x and not spawn_y:
        raise Exception("Не найдена точка спавна врагов")
    for i in Core.enemy_type:
        if i[0] == type:
            health = i[1]
            reward = i[4]
            enemy_type = i[0]
            spawn_delays[i[0]] = i[2]
            image = pygame.transform.scale(Core.load_image(i[3]), (80, 80))
    Enemy(image, spawn_x, spawn_y, health, reward, enemy_type)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, health, reward, enemy_type):
        super().__init__(enemy_group)
        self.type = enemy_type
        self.image = image
        self.rect = self.image.get_rect().move(x - image.get_width() // 2, y - image.get_height() // 2)
        self.speed = 1
        self.health = health
        self.direction = ''
        self.passedRoads = []
        self.reward = reward
        self.angle = 0
        self.update()

    def update(self):
        x, y = self.getRoad()
        width, height = len(Map.MAP_DATA[0]), len(Map.MAP_DATA)
        if self.health <= 0:
            enemy_group.remove(self)
            Core.balance += self.reward
            return
        if (x, y) in self.passedRoads:
            self.move()
            return
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.last_angle = self.angle
        self.angle = 0
        if x != 0 and Map.MAP_DATA[y][x - 1] == 'road' and (x - 1, y) not in self.passedRoads:
            self.direction = 'left'
            self.angle += 180
        elif x != width and Map.MAP_DATA[y][x + 1] == 'road' and (x + 1, y) not in self.passedRoads:
            self.direction = 'right'
        elif y != 0 and Map.MAP_DATA[y - 1][x] == 'road' and (x, y - 1) not in self.passedRoads:
            self.direction = 'up'
            self.angle += 90
        elif y != height and Map.MAP_DATA[y + 1][x] == 'road' and (x, y + 1) not in self.passedRoads:
            self.direction = 'down'
            self.angle += -90
        else:
            self.angle = self.last_angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.passedRoads.append((x, y))
        self.move()

    def move(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed

    def getRoad(self):
        road_id = None
        for tile in Map.tiles_group.sprites():
            if tile.rect.x + tile.rect.width // 2 == self.rect.x + self.image.get_width() // 2 \
                    and tile.rect.y + tile.rect.height // 2 == self.rect.y + self.image.get_height() // 2:
                road_id = Map.tiles_group.sprites().index(tile)
                if tile.type == "end":
                    enemy_group.remove(self)
                    Core.lives[0] -= 1
                break
        map_width = len(Map.MAP_DATA[0])
        if road_id is None:
            return 0, 0
        return road_id % map_width, road_id // map_width
