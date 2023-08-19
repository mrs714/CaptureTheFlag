from simulation.simulation_consts import *

class CollisionAlgorithm():
    
    # The map is divided in a grid of cells.
    class __Cell():
        def __init__(self, row, column):
            self.row = row
            self.column = column
            self.grid_position = (row, column)
            
            # Each cell has a dictionary for the bots, bullets and drops it contains, and their id's.
            # Those lists will be updated at each tick/frame.
            self.bots = {}
            self.bullets = {}
            self.drops = {}

    def __init__(self):
        self.__cells = [[self.__Cell(i, j) for j in range(COLLISIONS_CELL_NUMBER)] for i in range(COLLISIONS_CELL_NUMBER)] # n*n cells, n = COLLISIONS_CELL_NUMBER
        # self.__cells[2][1] would be cell at the third row, second column

    # Function used to populate the cells dictionaries
    def __populate_cells(self, bots, bullets, drops):
        self.__clear_cells()
        for bot in bots.values():
            self.__get_cell(bot.relative_x(), bot.relative_y()).bots[bot.id()] = bot
        for bullet in bullets.values():
            self.__get_cell(bullet.relative_x(), bullet.relative_y()).bullets[bullet.id()] = bullet
        for drop in drops.values():
            self.__get_cell(drop.relative_x(), drop.relative_y()).drops[drop.id()] = drop

    # Function used to clear cells
    def __clear_cells(self):
        for row in self.__cells:
            for cell in row:
                cell.bots.clear()
                cell.bullets.clear()
                cell.drops.clear()

    # Translates coordinates to a cell position, returns the cell
    def __get_cell(self, x, y):
        width = COLLISION_SQUARE_SIZE[0]
        height = COLLISION_SQUARE_SIZE[1]
        return self.__cells[math.ceil(y/height)-1][math.ceil(x/width)-1]

    # Checks for collisions between bots and other entities, saves them in a list of tuples (bot, entity)
    def __check_collisions(self, bots, bullets, drops):

        collisions = []
        
        def __bot_is_colliding_bullet(bot, bullet):
           return (bot.x() - bullet.x()) ** 2 + (bot.y() - bullet.y()) ** 2 <= (BOT_RADIUS + BULLET_RADIUS) ** 2 if bot.id() != bullet.get_owner_id() else False
        
        def __bot_is_colliding_drop(bot, drop):
            return (bot.x() - drop.x()) ** 2 + (bot.y() - drop.y()) ** 2 <= (BOT_RADIUS + DROP_RADIUS) ** 2

        for bot in bots.values():
            for bullet in bullets.values():
                if __bot_is_colliding_bullet(bot, bullet):
                    collisions.append((bot, bullet))
                    
            for drop in drops.values():
                if __bot_is_colliding_drop(bot, drop):
                    collisions.append((bot, drop))

        print(collisions) if len(collisions) > 0 else ""
        return collisions if len(collisions) > 0 else None

    # Function called from the main simulation loop.
    # It updates the cells and checks for collisions.
    def check_collisions(self, bots, bullets, drops):
        # First of all, we check the cell of each entity and update the cells dictionaries
        self.__populate_cells(bots, bullets, drops)

        for row in self.__cells:
            for cell in row:
                # Then, on each cell we get all of its entities and those of the neighbouring cells
                bots = cell.bots
                bullets = cell.bullets
                drops = cell.drops

                # Get the neighbouring cells if the neighbour cell exists
                neighbouring_cells = []
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        if cell.row + i >= 0 and cell.row + i < COLLISIONS_CELL_NUMBER and cell.column + j >= 0 and cell.column + j < COLLISIONS_CELL_NUMBER:
                            neighbouring_cells.append(self.__cells[cell.row + i][cell.column + j])

                # Get the entities in the neighbouring cells
                # We use the | operator to merge the dictionaries
                for neighbouring_cell in neighbouring_cells:
                    bots = bots | neighbouring_cell.bots
                    bullets = bullets | neighbouring_cell.bullets
                    drops = drops | neighbouring_cell.drops 

                # Finally we check for collisions between the bot and the other entities
                self.__check_collisions(bots, bullets, drops)