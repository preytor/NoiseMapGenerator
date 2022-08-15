
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Map viewer"
BGCOLOR = DARKGREY

TILESIZE = 4
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 500

# Map settings
MAP_WIDTH = 100
MAP_HEIGHT = 100

MAP_SEED = 1

# MAP TERRAINS
# The key is the name of the terrain 
# and the value is the height the terrain needs to have to be that terrain
# example of workflow:
# WATER = 0, PLAINS 0.5, MOUNTAINS 1.5
# if height < 0: terrain = WATER
# elif height < 0.5: terrain = PLAINS
# ETC..
# Values usually go from -0.5 to 0.5
HEIGHT_TERRAIN = {
    "DEEP_WATER": -0.1,
    "PLAINS": 0.1,
    "MOUNTAIN": 0.3,
    "MOUNTAIN_2": 0.4,
    "MOUNTAIN_PEAK": 100
}

# The key is the name of the terrain
# and the value is the color of the terrain in RGB
TERRAIN_COLOR = {
    "DEEP_WATER": tuple((0, 51, 204)),
    "PLAINS": tuple((0, 102, 0)),
    "MOUNTAIN": tuple((102, 51, 0)),
    "MOUNTAIN_2": tuple((153, 153, 102)),
    "MOUNTAIN_PEAK": tuple((228, 221, 220))
}
