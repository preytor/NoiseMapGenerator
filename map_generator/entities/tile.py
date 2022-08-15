import pygame as pg
from settings import *


class ImageTile(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, image) -> None:
        self.groups = game.image_tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.fromstring(image.tobytes(), image.size, image.mode).convert()
        self.rect = self.image.get_rect()
        self.x = w
        self.y = h
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def check_collisions(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                print(self.x, self.y, self.tile_type)


class Tile(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile_type):
        self.groups = game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.tile_type = tile_type
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(self.get_tile_sprite())
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_tile_sprite(self):
        return get_tile_sprite(self.tile_type)

    def check_collisions(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                print(self.x, self.y, self.tile_type)


# Get tile sprite but module-level to construct the ImageTile
def get_tile_sprite(tile_type):
    found_it = False
    for key, value in TERRAIN_COLOR.items():
        if tile_type == key:
            return value
    if not found_it:
        return tuple((0, 0, 0))