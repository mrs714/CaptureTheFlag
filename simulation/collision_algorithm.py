from simulation.simulation_consts import *

class CollisionAlgorithm():
    
    # The map is divided in a grid of cells.
    class __Cell():
        def __init__(self, row, column):
            self.__row = row
            self.__column = column
            self.__grid_position = (row, column)
            
            # Each cell has a dictionary for the bots, bullets and drops it contains, and their id's.
            # Those lists will be updated at each tick/frame.
            self.__bots = {}
            self.__bullets = {}
            self.__drops = {}

            def bots():
                return self.__bots
            
            def bullets():
                return self.__bullets
            
            def drops():
                return self.__drops

    def __init__(self):
        self.__cells = [[self.__Cell(i, j) for j in range(COLLISIONS_CELL_NUMBER)] for i in range(COLLISIONS_CELL_NUMBER)] # n*n cells, n = COLLISIONS_CELL_NUMBER
        # self.__cells[2][1] would be cell at the third row, second column

    # Function used to populate the cells dictionaries
    def __populate_cells(self, bots, bullets, drops):
        for bot in bots.values():
            self.__get_cell(bot.x, bot.y).__bots[bot.id()] = bot
        for bullet in bullets.values():
            self.__get_cell(bullet.x, bullet.y).__bullets[bullet.id()] = bullet
        for drop in drops.values():
            self.__get_cell(drop.x, drop.y).__drops[drop.id()] = drop

    # Translates coordinates to a cell position, returns the cell
    def __get_cell(self, x, y):
        return self.__cells[math.ceil(y/COLLISION_SQUARE_SIZE[1])][math.ceil(x/COLLISION_SQUARE_SIZE[0])]

    # Checks for collisions between bots and other entities
    def __check_collisions(self):
        pass

    # Function called from the main simulation loop.
    # It updates the cells and checks for collisions.
    def check_collisions(self, bots, bullets, drops):
        # First of all, we check the cell of each entity and update the cells dictionaries
        self.__populate_cells(bots, bullets, drops)

        for cell in self.__cells:
            # Then, on each cell we get all of its entities and those of the neighbouring cells
            bots = cell.__bots
            bullets = cell.__bullets
            drops = cell.__drops

            # Get the neighbouring cells if the neighbour cell exists
            neighbouring_cells = []
            for i in range(-1, 1):
                for j in range(-1, 1):
                    if cell.__row + i >= 0 and cell.__row + i < COLLISIONS_CELL_NUMBER and cell.__column + j >= 0 and cell.__column + j < COLLISIONS_CELL_NUMBER:
                        neighbouring_cells.append(self.__cells[cell.__row + i][cell.__column + j])

            # Get the entities in the neighbouring cells
            # We use the | operator to merge the dictionaries
            for neighbouring_cell in neighbouring_cells:
                bots = bots | neighbouring_cell.__bots
                bullets = bullets | neighbouring_cell.__bullets
                drops = drops | neighbouring_cell.__drops 

            # Finally we check for collisions between the bot and the other entities
            self.__check_collisions(bots, bullets, drops)

        