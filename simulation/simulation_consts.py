import math

MAP_WIDTH, MAP_HEIGHT = 500, 500 # pixels, actual playing zone
MAP_PADDING = 50 # padding at each side of the map
BULLET_RADIUS = 4 # pixels
BOT_RADIUS = 4 * BULLET_RADIUS # pixels
DROP_RADIUS = 2 * BULLET_RADIUS # pixels
BOT_SPEED = 3 # pixels per frame
BULLET_SPEED = BOT_SPEED * 4 # pixels per frame
FPS = 20 # frames per second
DURATION = 10 * FPS # In seconds (x FPS = 1 second)
INTER_SIMULATION_TIME = 300 # seconds (5 minutes)
SIM_MP4_NAME = "replays/simulation.mp4"
SIM_INFO_NAME = "replays/simulation_info.txt"

BLUE = (0, 0, 255) # Players
BLACK = (0, 0, 0) # Background
RED = (255, 0, 0) # Bullets
GREEN = (0, 255, 0) # Drops
ORANGE = (255, 165, 0) # Drops
CYAN = (0, 255, 255) # Drops
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40) # Playground
BOT_COLOR = BLUE
BACKGROUND_COLOR = BLACK
BULLET_COLOR = RED
DROP_COLOR_POINTS = GREEN
DROP_COLOR_HEALTH = ORANGE
DROP_COLOR_SHIELD = CYAN

BULLET_DAMAGE = 10 # change this in the future
MELEE_DAMAGE = 30
BOT_SHOOT_COOLDOWN = 10 # ticks
BOT_MOVE_COOLDOWN = 1 
BOT_MELEE_COOLDOWN = 20 
BOT_DASH_COOLDOWN = 100
BOT_SUPER_SHOT_COOLDOWN = 100
BOT_SUPER_MELEE_COOLDOWN = 100
BOT_MELEE_RADIUS = 2 * BOT_RADIUS

TIME_BETWEEN_DROPS = 10 # ticks 
NUMBER_OF_HEALTH_DROPS = 10
NUMBER_OF_SHIELD_DROPS = 2
POINTS_PER_DROP = 10

# Collisions grid
COLLISIONS_CELL_NUMBER = 10 # >= 3, cells per row/column
# Ceil is used to make sure that the grid is big enough to contain the whole map/overlaps rather than being too small.
# It doesn't have much importance, but the best results will be obtained using a grid with a number of cells that is a multiple of the map size.
COLLISION_SQUARE_SIZE = (math.ceil(MAP_WIDTH/COLLISIONS_CELL_NUMBER), math.ceil(MAP_HEIGHT/COLLISIONS_CELL_NUMBER))       
