import game
from settings import *

if __name__ == '__main__':
    # create the game object
    g = game.Game()
    while True:
        g.new_generated_map(MAP_WIDTH, MAP_HEIGHT)
        g.run()