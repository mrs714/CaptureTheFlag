from simulation.simulation_consts import *
# Entities to spawn
from simulation.objects.bot import Bot
from simulation.objects.bullet import Bullet
from simulation.objects.flag import Flag
from simulation.objects.drop import Drop
from simulation.objects.zone import Zone

import numpy as np

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
        self.__cells = np.empty((COLLISIONS_CELL_NUMBER, COLLISIONS_CELL_NUMBER), dtype=object)

        for i in range(COLLISIONS_CELL_NUMBER):
            for j in range(COLLISIONS_CELL_NUMBER):
                self.__cells[i, j] = self.__Cell(i, j)

        self.collision_size_bullet = BOT_RADIUS + BULLET_RADIUS
        self.collision_size_flag = BOT_RADIUS + FLAG_RADIUS
        self.collision_size_drop = BOT_RADIUS + DROP_RADIUS
        self.collision_size_zone = BOT_RADIUS + ZONE_RADIUS

    # Function used to populate the cells dictionaries
    def __populate_cells(self, bots, bullets, flags, drops, zones):
        self.__clear_cells()
        for entity_type, entities in zip(['bots', 'bullets', 'flags', 'drops', 'zones'], [bots, bullets, flags, drops, zones]):
            for entity in entities.values():
                cell = self.__get_cell(entity.relative_x(), entity.relative_y())
                getattr(cell, entity_type)[entity.id()] = entity

    # Function used to clear cells
    def __clear_cells(self):
        for cell in np.ravel(self.__cells):
            cell.bots.clear()
            cell.bullets.clear()
            cell.flags.clear()
            cell.drops.clear()
            cell.zones.clear()

    # Translates coordinates to a cell position, returns the cell
    def __get_cell(self, x, y):
        width = COLLISION_SQUARE_SIZE[0]
        height = COLLISION_SQUARE_SIZE[1]
        row = np.clip(np.ceil(y / height) - 1, 0, COLLISIONS_CELL_NUMBER - 1).astype(int)
        col = np.clip(np.ceil(x / width) - 1, 0, COLLISIONS_CELL_NUMBER - 1).astype(int)
        return self.__cells[row, col]

    # Checks for collisions between bots and other entities, saves them in a list of tuples (bot, entity)
    def __detect_collisions(self, bots, bullets, flags, drops, zones):

        collisions = []
        
        def __bot_is_colliding_bullet(bot, bullet):
           return (bot.x() - bullet.x()) ** 2 + (bot.y() - bullet.y()) ** 2 <= self.collision_size_bullet ** 2 if bot.id() != bullet.get_owner_id() else False
        
        def __bot_is_colliding_flag(bot, flag):
            return (bot.x() - flag.x()) ** 2 + (bot.y() - flag.y()) ** 2 <= self.collision_size_flag ** 2 if flag.get_holder() == None else False
        
        def __bot_is_colliding_drop(bot, drop):
            return (bot.x() - drop.x()) ** 2 + (bot.y() - drop.y()) ** 2 <= self.collision_size_drop ** 2
        
        def __bot_is_colliding_zone(bot, zone):
            return (bot.x() - zone.x()) ** 2 + (bot.y() - zone.y()) ** 2 <= self.collision_size_zone ** 2

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
                    # If a zone contains a flag, and the bot is not the owner, pick up the flag
                    if entity.get_owner() != bot and entity.get_contains_flag() is not None:
                        flag = entity.get_contains_flag()
                        entity.set_contains_flag(None) # Remove the flag from the zone
                        bot.carry_flag(entity.get_contains_flag()) # Pick up the flag
                        flag.set_zone(None) # Remove the flag from the zone
                        logger.info("Bot " + str(bot.id()) + " picked up a flag from zone " + str(entity.id()))
                    # If a zone is owned by the bot, and the bot is carrying a flag, drop the flag
                    elif entity.get_owner() == bot and bot.carrying_flag() is not None:
                        flag = bot.drop_flag()
                        entity.set_contains_flag(flag)
                        flag.set_zone(entity)
                        logger.info("Bot " + str(bot.id()) + " dropped a flag on zone " + str(entity.id()))
                   
                if type(entity) == Drop:
                    drops_to_remove.append((entity.id(), entity.type()))
                    bot.get_drop(entity.type())