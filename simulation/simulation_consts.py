import math

MAP_WIDTH, MAP_HEIGHT = 600, 600 # pixels, actual playing zone
MAP_PADDING = 50 # padding at each side of the map
BULLET_RADIUS = 4 # pixels
SUPER_BULLET_RADIUS = int(BULLET_RADIUS * 1.5)
BOT_RADIUS = 4 * BULLET_RADIUS # pixels
DROP_RADIUS = 2 * BULLET_RADIUS # pixels
BOT_SPEED = 3 # pixels per frame
BULLET_SPEED = BOT_SPEED * 4 # pixels per frame
FPS = 20 # frames per second
DURATION = 100 * FPS # In seconds (x FPS = 1 second)
INTER_SIMULATION_TIME = 60 # seconds
MAX_FRAMES_ON_RAM = 100000000 / (MAP_HEIGHT * MAP_WIDTH) # Maximum ammount of frames on RAM. e.g.: 350x350pixels = 81 frames stored, 1000*1000pixels = 10 frames stored
SIM_FOLDER = "replays/"
SIM_MP4_NAME = "replays/simulation.mp4"
SIM_INFO_NAME = "replays/simulation_info.txt"
SIM_FRAMES_PATH = "replays/frames/"
SIM_PLACEHOLDER_FOLDER = "replays/placeholder/"
SIM_VIDEO_PLACEHOLDER_PATH = "replays/placeholder/simulation.mp4" # Used to save the video without users getting errors trying to access it while it's being written
SIM_INFO_PLACEHOLDER_PATH = "replays/placeholder/simulation_info.txt" # Used to save the video without users getting errors trying to access it while it's being written

BLUE = (0, 0, 255) # Players
BLACK = (0, 0, 0) # Background
RED = (255, 0, 0) # Bullets
GREEN = (0, 255, 0) 
DARK_GREEN = (0, 100, 0) # Point drops
ORANGE = (255, 165, 0) # Drops
DARK_ORANGE = (200, 100, 0) # Drops
CYAN = (0, 255, 255) # Drops
DARK_CYAN = (0, 100, 100) # Drops
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40) # Playground
BOT_COLOR = BLUE
BACKGROUND_COLOR = BLACK
BULLET_COLOR = RED
DROP_COLOR_POINTS_MIN = DARK_GREEN
DROP_COLOR_HEALTH_MIN = DARK_ORANGE
DROP_COLOR_SHIELD_MIN = DARK_CYAN
DROP_COLOR_POINTS_MAX = GREEN
DROP_COLOR_HEALTH_MAX = ORANGE
DROP_COLOR_SHIELD_MAX = CYAN

BULLET_DAMAGE = 10 # change this in the future
SUPER_BULLET_DAMAGE = int(BULLET_DAMAGE * 2)
MELEE_DAMAGE = 30
BOT_SHOOT_COOLDOWN = 15 # ticks
BOT_MOVE_COOLDOWN = 1 
BOT_MELEE_COOLDOWN = 20 
BOT_DASH_COOLDOWN = 100
BOT_SUPER_SHOT_COOLDOWN = 100
BOT_SUPER_MELEE_COOLDOWN = 100
BOT_MELEE_RADIUS = 2 * BOT_RADIUS
SECONDS_TO_REGAIN_SHIELD = 1 # seconds

TIME_BETWEEN_DROPS = 20 # ticks 
NUMBER_OF_HEALTH_DROPS = 2
NUMBER_OF_SHIELD_DROPS = 2
POINTS_PER_DROP = 10
HEALTH_PER_DROP = 50
SHIELD_PER_DROP = 50
POINTS_ON_DEATH = 50 / 100 # % of points given to the killer player

# Collisions grid
COLLISIONS_CELL_NUMBER = 10 # >= 3, cells per row/column
# Ceil is used to make sure that the grid is big enough to contain the whole map/overlaps rather than being too small.
# It doesn't have much importance, but the best results will be obtained using a grid with a number of cells that is a multiple of the map size.
COLLISION_SQUARE_SIZE = (math.ceil(MAP_WIDTH/COLLISIONS_CELL_NUMBER), math.ceil(MAP_HEIGHT/COLLISIONS_CELL_NUMBER))       
