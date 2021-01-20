import pygame
import Core

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

MAP_DATA = list()

instructions = dict()
enemy_delays = dict()


def create_map(path, *tile_size): #создаём карту
    with open(path, 'r') as file:
        global MAP_DATA
        data = file.read().split('\n')
        MAP_DATA = [list() for _ in range(len(data))]
        inst = data[data.index(''):]#автоматическое заполнение пропусков карты
        data = data[:data.index('')]
        max_width = max(map(len, data))
        data = list(map(lambda a: a.ljust(max_width, ' '), data))
        for y in range(len(data)):
            for x in range(max_width):
                for i in Core.codes:
                    if data[y][x] in i:
                        image = pygame.transform.scale(Core.load_image(i[2]), tile_size)#загрузка изображения с соотвествующим размеров
                        MAP_DATA[y].append(i[1])
                        Tile(i[1], image, x, y, tile_size)
        for i in range(1, len(inst), 2):
            enemys = inst[i + 1].split(' ')
            instructions[int(inst[i])] = enemys
            for j in enemys:
                for k in Core.enemy_type:
                    if k[0] == j:
                        enemy_delays[j] = k[2]
