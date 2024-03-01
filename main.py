import pygame
import sys
from upload_image import load_image

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')
tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя", '',
                  "Герой двигается",
                  "Карта на месте"]
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.position = (pos_x, pos_y)

    def move(self, x, y):
        self.position = x, y
        self.rect.x = tile_width * self.position[0] + 15
        self.rect.y = tile_height * self.position[1] + 5


def move(player, move):
    x, y = player.position
    if move == 'left' and level_map[y][x - 1] == '.' and x > 0:
        player.move(x - 1, y)
    if move == 'right' and level_map[y][x + 1] == '.' and x < level_x - 1:
        player.move(x + 1, y)
    if move == 'up' and level_map[y - 1][x] == '.' and y > 0:
        player.move(x, y - 1)
    if move == 'down' and level_map[y + 1][x] == '.' and y < level_y - 1:
        player.move(x, y + 1)


if __name__ == '__main__':
    start_screen()
    try:
        level_map = load_level(input())
    except FileNotFoundError:
        print("Такой карты не существует")
        sys.exit()
    player, level_x, level_y = generate_level(level_map)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(player, 'up')
                if event.key == pygame.K_DOWN:
                    move(player, 'down')
                if event.key == pygame.K_RIGHT:
                    move(player, 'right')
                if event.key == pygame.K_LEFT:
                    move(player, 'left')
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()