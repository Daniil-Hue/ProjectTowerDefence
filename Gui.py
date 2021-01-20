import pygame
import Core

button_group = pygame.sprite.Group()


def create_tower_buttons(height, width, *screen_size):
    screen_size = screen_size[0]
    for i in range(len(Core.tower_types)):
        x = (30 + width) * i
        y = screen_size[1] - 30
        image = Core.load_image(Core.tower_types[i][3])
        Button(image, Core.tower_types[i][0], x, y, width, height)


def draw_costs(screen):
    for i in button_group.sprites():
        Core.draw_text(screen, Core.tower_costs[i.tower_type], i.rect.centerx - 23,
                       i.rect.centery - 10, 30, (250, 250, 250))


class Button(pygame.sprite.Sprite):
    def __init__(self, image, tower_type, x, y, *size):
        super().__init__(button_group)
        self.tower_type = tower_type
        self.image = image
        self.rect = self.image.get_rect().move(x, y - size[1])
