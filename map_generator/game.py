import pygame as pg
import sys

from settings import *
from utils.sprites import *
from entities.player import *
from entities.tile import *
from utils.camera import *
from utils.button import *
from utils.inputbox import *
from worldgen.world_generator import *
from utils.label import *



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.font = pygame.font.SysFont('Calibri', 30)

        self.menu_hidden = False
        
        self.zoom_label = Label("Noise Scale:", WHITE, 800, 0, self.font)
        self.noise_scale_input = InputBox(800, 25, 140, 32, self.screen, self.font, text='10')
        self.octaves_label = Label("Octaves:", WHITE, 800, 60, self.font)
        self.octaves_input = InputBox(800, 85, 140, 32, self.screen, self.font, text='16')
        self.persistance_label = Label("Persistance:", WHITE, 800, 120, self.font)
        self.persistance_input = InputBox(800, 145, 140, 32, self.screen, self.font, text='0.6')
        self.lacunarity_label = Label("Lacunarity:", WHITE, 800, 180, self.font)
        self.lacunarity_input = InputBox(800, 205, 140, 32, self.screen, self.font, text='2')
        self.offset_x_label = Label("Offset X:", WHITE, 800, 240, self.font)
        self.offset_x_input = InputBox(800, 265, 140, 32, self.screen, self.font)
        self.offset_y_label = Label("Offset Y:", WHITE, 800, 300, self.font)
        self.offset_y_input = InputBox(800, 325, 140, 32, self.screen, self.font)

        
        self.fps_counter = Fps("", WHITE, 0, 0, self.font)
   
        self.labels = [self.zoom_label, self.octaves_label, self.persistance_label,
                        self.lacunarity_label, self.offset_x_label, self.offset_y_label]
        self.input_boxes = [self.noise_scale_input, self.octaves_input, self.persistance_input,
                        self.lacunarity_input, self.offset_x_input, self.offset_y_input,]
        self.generate_button = Button(800, 380, self.screen, self.font, "Generate")


    def game_keys(self):
        keys = pg.key.get_pressed()

        # Hidding Menu
        if keys[pg.K_h]:
            self.menu_hidden = True if not self.menu_hidden else False


    def new_generated_map(self, map_width, map_height):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.player_layer = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.image_tiles = pg.sprite.Group()

        self.width = map_width * TILESIZE
        self.height = map_height * TILESIZE

        self.map = WorldGenerator(self, map_width, map_height, isTiles=True)
        self.mini_map = WorldGenerator(self, map_width, map_height)
        
        self.player = Player(self, 0, 1* TILESIZE)
        self.camera = Camera(self.width, self.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.player_layer.update()
        self.camera.update(self.player)
        for box in self.input_boxes:
            box.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()

        for sprite in self.player_layer:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # Maps
        for sprite in self.tiles:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.image_tiles:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if not self.menu_hidden:
            if self.generate_button.draw():
                self.map.apply_parameters(
                    self.noise_scale_input.text, 
                    self.octaves_input.text, 
                    self.persistance_input.text, 
                    self.lacunarity_input.text, 
                    self.offset_x_input.text, 
                    self.offset_y_input.text
                )
                self.map.generate_world()

                self.mini_map.apply_parameters(
                    self.noise_scale_input.text, 
                    self.octaves_input.text, 
                    self.persistance_input.text, 
                    self.lacunarity_input.text, 
                    self.offset_x_input.text, 
                    self.offset_y_input.text
                )
                self.mini_map.generate_world()

        if hasattr(self, 'map'):
            self.map.draw()

        if hasattr(self, 'mini_map'):
            self.mini_map.draw()
        
        if not self.menu_hidden:
            for box in self.input_boxes:
                box.draw(self.screen)

            for label in self.labels:
                label.draw(self.screen)

        self.fps_counter.draw(self.clock.get_fps(), self.screen)

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                
                self.game_keys()
                self.map.get_keys()
                self.mini_map.get_keys(False)

                if event.key == pg.K_ESCAPE:
                    self.quit()
            
            for box in self.input_boxes:
                box.handle_event(event)

            for tile in self.map.tiles:
                tile.check_collisions(event)
