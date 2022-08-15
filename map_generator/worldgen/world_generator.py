import pygame as pg
from noise import pnoise2
import numpy as np
from PIL import Image, ImageDraw

import sys
sys.path.append('../')
from entities.tile import Tile, ImageTile, get_tile_sprite
from settings import TILESIZE, MAP_WIDTH, MAP_SEED, HEIGHT_TERRAIN

class WorldGenerator:
    def __init__(self, game, x, y, isTiles=False) -> None:
        self.game = game
        self.x = x
        self.y = y
        self.isTiles = isTiles
        self.tiles = []
        print(self.tiles)


    def apply_parameters(self, scale, octaves, persistence, lacunarity, offset_x, offset_y):
        self.scale = float(scale)
        self.octaves = int(octaves)
        self.persistence = float(persistence)
        self.lacunarity = float(lacunarity)
        self.offset_x = float(offset_x)
        self.offset_y = float(offset_y)

        
    def generate_world(self) -> None:
        shape = np.zeros((self.x, self.y), dtype=float)
        # We delete all of these values and restart them to avoid memory leaks
        if self.isTiles:
            self.game.tiles.empty()
        else:
            self.game.image_tiles.empty()
        del self.tiles  
        self.tiles = []
        if not self.isTiles:
            img = Image.new('RGB', (self.x*TILESIZE, self.y*TILESIZE))
            map_image = ImageDraw.Draw(img)

        for i in range(len(shape[0])):
            for j in range(len(shape[1])):
                p = pnoise2(
                    (i/self.scale)+self.offset_x,
                    (j/self.scale)+self.offset_y,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=self.x,
                    repeaty=self.y,
                    base=MAP_SEED
                )

                height = self.terrain_from_height(p)
                if self.isTiles:
                    tile = Tile(self.game, i, j, height)
                    self.tiles.append(tile)
                else:
                    map_image.rectangle([(i*TILESIZE,j*TILESIZE),((i*TILESIZE)+TILESIZE-1,(j*TILESIZE)+TILESIZE-1)], fill=get_tile_sprite(height))

        if not self.isTiles:            
            map_image.rectangle([(0, 0),(
                (self.x*TILESIZE)/(self.game.map.scale/10)-1, 
                (self.y*TILESIZE)/(self.game.map.scale/10)-1
                )], outline="red", width=1)
            self.tiles.append(ImageTile(self.game, MAP_WIDTH+10, 0, self.x, self.y, img))

    def update_map_image_with_rect(self):
        shape = np.zeros((self.x, self.y), dtype=float)
        self.game.image_tiles.empty()
        img = Image.new('RGB', (self.x*TILESIZE, self.y*TILESIZE))
        map_image = ImageDraw.Draw(img)
        for i in range(len(shape[0])):
            for j in range(len(shape[1])):
                p = pnoise2(
                    (i/self.scale)+self.offset_x,
                    (j/self.scale)+self.offset_y,
                    octaves=self.octaves,
                    persistence=self.persistence,
                    lacunarity=self.lacunarity,
                    repeatx=self.x,
                    repeaty=self.y,
                    base=MAP_SEED
                )

                height = self.terrain_from_height(p)
                
                map_image.rectangle([(i*TILESIZE,j*TILESIZE),((i*TILESIZE)+TILESIZE-1,(j*TILESIZE)+TILESIZE-1)], fill=get_tile_sprite(height))
        map_image.rectangle([(0, 0),(
                (self.x*TILESIZE)/(self.game.map.scale/10)-1, 
                (self.y*TILESIZE)/(self.game.map.scale/10)-1
                )], outline="red", width=1)
        self.tiles.append(ImageTile(self.game, 110, 0, self.x, self.y, img))


    def draw(self):
        pass


    def get_keys(self, zoomable=True):
        keys = pg.key.get_pressed()

        # Left
        if keys[pg.K_KP4]:
            self.offset_x = self.offset_x - 0.1
            self.generate_world()

        # Right
        if keys[pg.K_KP6]:
            self.offset_x = self.offset_x + 0.1
            self.generate_world()

        # Up
        if keys[pg.K_KP8]:
            self.offset_y = self.offset_y - 0.1
            self.generate_world()
        # Down
        if keys[pg.K_KP2]:
            self.offset_y = self.offset_y + 0.1
            self.generate_world()

        if zoomable:
            # Zoom in
            if keys[pg.K_KP_PLUS]:
                self.scale = self.scale + 1
                if pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.scale = self.scale + 9
                self.generate_world()
            # Zoom out
            if keys[pg.K_KP_MINUS]:
                self.scale = self.scale - 1
                if pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.scale = self.scale - 9
                self.generate_world()
        else:
            self.update_map_image_with_rect()


        # Debug
        if hasattr(self, 'offset_x'):
            print("----------------")
            print("offset_x:", self.game.map.offset_x)
            print("offset_y:", self.game.map.offset_y)
            print("scale:", self.game.map.scale)



    def terrain_from_height(self, height):
        for key, value in HEIGHT_TERRAIN.items():
            if height <= value:
                return key
