MAP_WIDTH, MAP_HEIGHT = 1000, 1000 # pixels
BULLET_RADIUS = 10 # pixels
BOT_RADIUS = 4 * BULLET_RADIUS # pixels
PLAYER_SPEED = 3 # pixels per frame
BULLET_SPEED = PLAYER_SPEED * 4 # pixels per frame
FPS = 20 # frames per second
DURATION = 10 * FPS # ticks (converts 60 seconds to ticks)
INTER_SIMULATION_TIME = 300 # seconds (5 minutes)
SIM_MP4_NAME = "simulation/simulation.mp4"
SIM_INFO_NAME = "simulation/simulation_info.txt"

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BOT_COLOR = BLUE
BACKGROUND_COLOR = BLACK
BULLET_COLOR = RED
