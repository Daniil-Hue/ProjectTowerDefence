import pygame
import os

tower_costs = {
    "laser": 100,
    "fire": 150
}

tower_types = [  # type, damage, radius, image_path, bullet_path
    ["laser", 50, 200, "assets/laserGun.png", "assets/laserBullet.png"],
    ["fire", 100, 150, "assets/fireGun.png", "assets/fire.png"]
]

codes = [  # code, type, image_path
    ['#', 'field', 'assets/field.png'],
    ['%', 'road', 'assets/road.png'],
    ['$', 'base', 'assets/base.png'],
    ['@', 'spawn', 'assets/road.png'],
    ['*', 'end', 'assets/road.png']
]

enemy_type = [  # type, health, speed, path, reward
    ["soldier", 100, 0.02, "assets/soldier.png", 10],
    ["warrior", 200, 0.025, "assets/warrior.png", 20],
    ["cyborg", 300, 0.03, "assets/cyborg.png", 30],
    ["robot", 400, 0.035, "assets/robot.png", 40]
]

balance = 0
lives = [5, 5]  # current, max


def load_image(path, color_key=None):
    if not os.path.isfile(path):
        raise Exception(f"Изображение не найдено. {path}")
    image = pygame.image.load(path)
    if color_key:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def draw_text(screen, text, x, y, size, color, font_type='assets/FredokaOne-Regular.ttf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
