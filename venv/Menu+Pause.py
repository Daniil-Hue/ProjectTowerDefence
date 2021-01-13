import pygame
import pygame_menu
import os
import sys

pygame.init()

surface = pygame.display.set_mode((1920, 1080))


def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def start_the_game():
    import pygame

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    sprites = pygame.sprite.Group()
    hero_im = load_image('hero.png')
    hero = pygame.sprite.Sprite(sprites)
    hero.image = hero_im
    hero.rect = hero.image.get_rect()
    clock = pygame.time.Clock()
    col = []
    coord = []
    rad = 10
    fps = 300
    colour = pygame.Color(255, 255, 255)

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            key_pr = pygame.key.get_pressed()
            if key_pr[pygame.K_ESCAPE]:
                pygame.quit()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    screen.fill((255, 255, 255))
            if event.type == pygame.MOUSEBUTTONDOWN:
                s = event.pos
                col.append(list(s))
                coord.append([-1, -1])
        for i in range(len(col)):
            for j in (0, 1):
                if col[i][j] >= size[j] - rad or col[i][j] <= rad:
                    coord[i][j] = -coord[i][j]
                col[i][j] += coord[i][j]
            pygame.draw.circle(screen, colour, col[i], rad, 0)
        pygame.display.flip()
        clock.tick(fps)


menu = pygame_menu.Menu(1080, 1920, 'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Normal', 2), ('Hard', 3), ('Easy', 1)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
