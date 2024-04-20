from simulation.simulation_consts import *
# Entities to spawn
from simulation.objects.bot import Bot
from simulation.objects.bullet import Bullet
from simulation.objects.flag import Flag
from simulation.objects.drop import Drop
from simulation.objects.zone import Zone

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
            self.flags = {}
            self.drops = {}
            self.zones = {}

    def __init__(self):
        self.__cells = [[self.__Cell(i, j) for j in range(COLLISIONS_CELL_NUMBER)] for i in range(COLLISIONS_CELL_NUMBER)] # n*n cells, n = COLLISIONS_CELL_NUMBER
        # self.__cells[2][1] would be cell at the third row, second column

    # Function used to populate the cells dictionaries
    def __populate_cells(self, bots, bullets, flags, drops, zones):
        self.__clear_cells()
        for bot in bots.values():
            self.__get_cell(bot.relative_x(), bot.relative_y()).bots[bot.id()] = bot
        for bullet in bullets.values():
            self.__get_cell(bullet.relative_x(), bullet.relative_y()).bullets[bullet.id()] = bullet
        for flag in flags.values():
            self.__get_cell(flag.relative_x(), flag.relative_y()).flags[flag.id()] = flag
        for drop in drops.values():
            self.__get_cell(drop.relative_x(), drop.relative_y()).drops[drop.id()] = drop
        for zone in zones.values():
            self.__get_cell(zone.relative_x(), zone.relative_y()).zones[zone.id()] = zone

    # Function used to clear cells
    def __clear_cells(self):
        for row in self.__cells:
            for cell in row:
                cell.bots.clear()
                cell.bullets.clear()
                cell.flags.clear()
                cell.drops.clear()
                cell.zones.clear()

    # Translates coordinates to a cell position, returns the cell
    def __get_cell(self, x, y):
        width = COLLISION_SQUARE_SIZE[0]
        height = COLLISION_SQUARE_SIZE[1]
        return self.__cells[math.ceil(y/height)-1][math.ceil(x/width)-1]

    # Checks for collisions between bots and other entities, saves them in a list of tuples (bot, entity)
    def __detect_collisions(self, bots, bullets, flags, drops, zones):

        collisions = []
        
        def __bot_is_colliding_bullet(bot, bullet):
           return (bot.x() - bullet.x()) ** 2 + (bot.y() - bullet.y()) ** 2 <= (BOT_RADIUS + BULLET_RADIUS) ** 2 if bot.id() != bullet.get_owner_id() else False
        
        def __bot_is_colliding_flag(bot, flag):
            return (bot.x() - flag.x()) ** 2 + (bot.y() - flag.y()) ** 2 <= (BOT_RADIUS + FLAG_RADIUS) ** 2 if flag.get_holder() == None else False
        
        def __bot_is_colliding_drop(bot, drop):
            return (bot.x() - drop.x()) ** 2 + (bot.y() - drop.y()) ** 2 <= (BOT_RADIUS + DROP_RADIUS) ** 2
        
        def __bot_is_colliding_zone(bot, zone):
            return (bot.x() - zone.x()) ** 2 + (bot.y() - zone.y()) ** 2 <= (BOT_RADIUS + ZONE_RADIUS) ** 2

        for bot in bots.values():
            for bullet in bullets.values():
                if __bot_is_colliding_bullet(bot, bullet):
                    collisions.append((bot, bullet))

            for flag in flags.values():
                if __bot_is_colliding_flag(bot, flag):
                    collisions.append((bot, flag))
                    
            for drop in drops.values():
                if __bot_is_colliding_drop(bot, drop):
                    collisions.append((bot, drop))

            for zone in zones.values():
                if __bot_is_colliding_zone(bot, zone):
                    collisions.append((bot, zone))

        return collisions

    # Function called from the main simulation loop.
    # It updates the cells and checks for collisions.
    def detect_collisions(self, bots, bullets, flags, drops, zones):
        # First of all, we check the cell of each entity and update the cells dictionaries
        self.__populate_cells(bots, bullets, flags, drops, zones)

        # Store the collisions detected in each cell:
        collisions = []

        for row in self.__cells:
            for cell in row:
                # Then, on each cell we get all of its entities and those of the neighbouring cells
                bots = cell.bots
                bullets = cell.bullets
                flags = cell.flags
                drops = cell.drops
                zones = cell.zones

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
                    flags = flags | neighbouring_cell.flags
                    drops = drops | neighbouring_cell.drops 
                    zones = zones | neighbouring_cell.zones

                # Finally we check for collisions between the bot and the other entities, and save them
                collisions += self.__detect_collisions(bots, bullets, flags, drops, zones)

        # Merge all collisions that are the same
        collisions = list(set(collisions))
        return collisions if len(collisions) > 0 else None
    
    # Gets a list of the bots and the entities they are colliding with
    def handle_collisions(self, collisions, bots_to_remove, bullets_to_remove, drops_to_remove, entities, kill_bot, tick, logger):
        if collisions:
            for bot, entity in collisions:
                if type(entity) == Bullet:
                    bot.hit(tick)
                    bullets_to_remove.append(entity.id())
                    bullet_owner_id = entity.get_owner_id()
                    if entity.get_type() == "normal":
                        if (bot.receive_shield_damage(BULLET_DAMAGE)):
                            kill_bot(bot.id(), bots_to_remove, bullet_owner_id)
                    else: 
                        if (bot.receive_life_damage(MELEE_DAMAGE)):
                            kill_bot(bot.id(), bots_to_remove, bullet_owner_id)

                if type(entity) == Flag:
                    if bot.carrying_flag() == None:
                        bot.carry_flag(entity)
                    else:
                        logger.error("Bot " + str(bot.id()) + " tried to pick up a flag while carrying one")

                if type(entity) == Zone:
                    if entity.get_owner() != bot and entity.get_contains_flag() is not None:
                        entity.set_contains_flag(None)
                        bot.carry_flag(entity.get_contains_flag())
                        logger.info("Bot " + str(bot.id()) + " picked up a flag from zone " + str(entity.id()))
                    elif entity.get_owner() == bot and bot.carrying_flag() is not None:
                        entity.set_contains_flag(bot.drop_flag())
                        logger.info("Bot " + str(bot.id()) + " dropped a flag on zone " + str(entity.id()))
                   
                if type(entity) == Drop:
                    drops_to_remove.append((entity.id(), entity.type()))
                    bot.get_drop(entity.type())