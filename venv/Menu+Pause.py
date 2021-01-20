import pygame
import Map
import Enemy
import Gui
import Core
import Tower
import time
import os
import pygame_menu

pygame.init()

surface = pygame.display.set_mode((1920, 1080))


def start_the_game():
    levels = ["levels/" + i for i in os.listdir("levels/")]
    current_level = 0

    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    running = True

    Map.create_map(levels[0], 100, 100)

    Gui.create_tower_buttons(100, 100, size)

    coin = pygame.transform.scale(Core.load_image("assets/coin.png"), (70, 70))
    heart = pygame.transform.scale(Core.load_image("assets/heart.png"), (50, 50))
    heart_empty = pygame.transform.scale(Core.load_image("assets/heart_empty.png"), (50, 50))

    SELECTED_TOWER = ''
    SELECTED_TILE = None

    next_level = False
    game_end = False
    start_new_game = False
    died = False

    Core.balance = 150
    update_timer = time.time()
    shoot_timer = time.time()
    enemy_timers = [time.time() for _ in range(len(list(Map.enemy_delays)))]
    current_wave = -1
    spawned_enemys = [0, 0]
    wavetimer = 0
    enemy_spawn_timer = time.time()

    def pause():
        paused = True
        Core.load_image('assets/pause.jpg')
        intro_text = ['', "Пауза", "",
                      "",
                      "Нажмите 'с' ", ''
                      "чтобы продолжить,",
                      '',
                      '',
                      "Нажмите 'q' ", ''
                      "чтобы выйти"]
        fon = pygame.transform.scale(Core.load_image('assets/pause.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 20
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color((200, 200, 200)))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 30
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            pygame.display.flip()

    while running:
        if Core.lives[0] == 0:
            died = True
        key_pr = pygame.key.get_pressed()
        if key_pr[pygame.K_ESCAPE]:
            pause()
        while died:
            screen.fill((0, 0, 0))
            Core.draw_text(screen, "YOU LOSE!",
                           size[0] / 2 - 100, size[1] / 2, 40, (255, 255, 255))
            Core.draw_text(screen, "To restart press any key",
                           size[0] / 2 - 230, size[1] / 2 + 50, 40, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    died = False
                elif event.type == pygame.KEYUP:
                    died = False
                    start_new_game = True
                    Core.lives[0] = Core.lives[1]
            pygame.display.flip()
        if start_new_game:
            Core.balance = 150
            Map.tiles_group.empty()
            Tower.tower_group.empty()
            Tower.bullet_group.empty()
            Enemy.enemy_group.empty()
            next_level = False
            update_timer = time.time()
            shoot_timer = time.time()
            enemy_timers = [time.time() for _ in range(len(list(Map.enemy_delays)))]
            Map.create_map(levels[current_level], 100, 100)
            current_wave = -1
            spawned_enemys = [0, 0]
            wavetimer = 0
            enemy_spawn_timer = time.time()
            start_new_game = False
        while game_end:
            screen.fill((0, 0, 0))
            Core.draw_text(screen, "THE END!",
                           size[0] / 2 - 59, size[1] / 2, 40, (255, 255, 255))
            Core.draw_text(screen, "To play again press any key",
                           size[0] / 2 - 230, size[1] / 2 + 50, 40, (255, 255, 255))
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                    game_end = False
                elif event.type == pygame.KEYUP:
                    game_end = False
                    current_level = 0
                    start_new_game = True
            pygame.display.flip()
        while next_level:
            screen.fill((0, 0, 0))
            Core.draw_text(screen, "You passed this level!",
                           size[0] / 2 - 200, size[1] / 2, 40, (255, 255, 255))
            Core.draw_text(screen, "To continue press any key",
                           size[0] / 2 - 230, size[1] / 2 + 50, 40, (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    next_level = False
                elif event.type == pygame.KEYUP:
                    current_level += 1
                    next_level = False
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in Gui.button_group.sprites():
                    if btn.rect.collidepoint(event.pos):
                        SELECTED_TOWER = btn.tower_type
                        break
            elif event.type == pygame.MOUSEBUTTONUP and SELECTED_TILE:
                if SELECTED_TILE.type == 'base':
                    if Core.balance >= Core.tower_costs[SELECTED_TOWER]:
                        Tower.create_tower(SELECTED_TILE, SELECTED_TOWER, 70, 70)
                        Core.balance -= Core.tower_costs[SELECTED_TOWER]
                SELECTED_TOWER = ''
                SELECTED_TILE = None
        delay = list(Map.instructions)[current_wave]
        if spawned_enemys[0] == spawned_enemys[1]:
            if not Enemy.enemy_group.sprites() and wavetimer == 0:
                print(current_wave, len(list(Map.instructions)))
                if current_wave >= len(list(Map.instructions)) - 1:
                    if current_level + 1 == len(levels):
                        game_end = True
                    else:
                        next_level = True
                else:
                    current_wave += 1
                wavetimer = time.time()
            elif time.time() - wavetimer >= delay and wavetimer != 0:
                spawned_enemys = [0, len(Map.instructions[delay])]
                wavetimer = 0

        screen.fill((255, 255, 255))
        Map.tiles_group.draw(screen)
        if SELECTED_TOWER:
            for tile in Map.tiles_group.sprites():
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    SELECTED_TILE = tile
                    if tile.type == 'base':
                        color = (0, 255, 0)
                    else:
                        color = (255, 0, 0)
                    pygame.draw.rect(screen, color, tile.rect, 4)
                    break
        Enemy.enemy_group.draw(screen)
        Tower.tower_group.draw(screen)
        Gui.button_group.draw(screen)
        Gui.draw_costs(screen)
        Tower.bullet_group.draw(screen)
        Core.draw_text(screen, Core.balance, coin.get_width() + 20, 20, 40, (250, 250, 250))
        screen.blit(coin, (10, 10))
        if wavetimer != 0:
            Core.draw_text(screen, delay - int(time.time() - wavetimer), size[0] / 2, 20, 40, (250, 250, 250))
        if spawned_enemys[0] != spawned_enemys[1] and time.time() - enemy_spawn_timer >= 2:
            Enemy.spawn_enemy(Map.instructions[delay][spawned_enemys[0]])
            spawned_enemys[0] += 1
            enemy_spawn_timer = time.time()
        lcounter = Core.lives[1] - Core.lives[0]
        for i in range(Core.lives[1]):
            if lcounter != 0:
                screen.blit(heart_empty, (size[0] - 30 * i - 60, 10))
                lcounter -= 1
            else:
                screen.blit(heart, (size[0] - 30 * i - 60, 10))
        # for i in Tower.bullet_group.sprites():
        #     pygame.draw.rect(screen, (255, 0, 0), i.image.get_rect().move(i.rect.x, i.rect.y), 3)
        #     pygame.draw.circle(screen, (0, 255, 0), (i.rect.x, i.rect.y), 5, 4)
        if time.time() - update_timer >= 0.02:
            for i in Tower.tower_group.sprites():
                i.update()
            for i in Tower.bullet_group.sprites():
                i.update()
            update_timer = time.time()
        for i, j in enumerate(list(Map.enemy_delays)):
            if time.time() - enemy_timers[i] >= Map.enemy_delays[j]:
                for k in Enemy.enemy_group.sprites():
                    k.update()
                enemy_timers[i] = time.time()
        if time.time() - shoot_timer >= 0.8:
            for i in Tower.tower_group.sprites():
                i.shoot()
            shoot_timer = time.time()
        pygame.display.flip()


menu = pygame_menu.Menu(1080, 1920, 'Добро пожаловать',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_button('Начать игру', start_the_game)
menu.add_button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(surface)
