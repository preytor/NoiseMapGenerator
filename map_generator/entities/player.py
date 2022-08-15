import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.player_layer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()

        # Left
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vx = -PLAYER_SPEED*2
        # Right
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vx = PLAYER_SPEED*2
        # Up
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vy = -PLAYER_SPEED*2
        # Down
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
            if pg.key.get_mods() & pg.KMOD_SHIFT:
                self.vy = PLAYER_SPEED*2

        # Zooms
        if keys[pg.K_PAGEDOWN]:
            TILESIZE += 1

        if keys[pg.K_PAGEUP]:
            TILESIZE -= 1
        
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.topleft = (self.x, self.y)