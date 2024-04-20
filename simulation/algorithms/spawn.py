from simulation.simulation_consts import *
# Entities to spawn
from simulation.objects.bot import Bot
from simulation.objects.bullet import Bullet
from simulation.objects.drop import Drop
from simulation.objects.flag import Flag
from simulation.objects.zone import Zone

import random as rnd

class Spawner():
    # Spawns different types of entity

    def __init__(self): # Type: "player_death", "drop_picked"
        self.__id_counter = 0

    def __get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def spawn_bot(self, bot, config, x, y):
        sim_id = self.__get_id()
        entity = Bot(sim_id, 
                bot["id"], 
                bot["username"], 
                x, # At least 50 inside the play-zone
                y, 
                bot["code"], 
                config["health"], 
                config["shield"], 
                config["attack"])
        return sim_id, entity
    
    def spawn_zone(self, x, y, bot):
        sim_id = self.__get_id()
        return sim_id, Zone(sim_id, x, y, bot)
    
    def spawn_bullet(self, bot, dx, dy, type):
        sim_id = self.__get_id()
        entity = Bullet(sim_id, 
                            bot.x(), 
                            bot.y(), 
                            dx, 
                            dy, 
                            BULLET_DAMAGE if type == "normal" else SUPER_BULLET_DAMAGE,
                            type,
                            bot.id())
        return sim_id, entity
        
    def spawn_drops(self, entities, tick):
        def spawn(drop):
            sim_id = self.__get_id()
            entities["drops_" + drop][sim_id] = Drop(sim_id, 
                                                            rnd.randint(MAP_PADDING + DROP_RADIUS, MAP_WIDTH + MAP_PADDING - DROP_RADIUS), 
                                                            rnd.randint(MAP_PADDING + DROP_RADIUS, MAP_HEIGHT + MAP_PADDING - DROP_RADIUS), 
                                                            drop)

        # If empty, replenish health and shield drops:
        if len(entities["drops_health"]) < NUMBER_OF_HEALTH_DROPS:
            spawn("health")
        
        if len(entities["drops_shield"]) < NUMBER_OF_SHIELD_DROPS:
            spawn("shield")
        
        # Point drops: Minimum ammount: ceil(players/4); Maximum ammount: max((players-1), 1);
        if (len(entities["drops_points"]) < math.ceil(len(entities["bots"]))) or (tick % TIME_BETWEEN_DROPS == 0):
            if len(entities["drops_points"]) < max((len(entities["bots"]) - 1), 1):
                spawn("points")

    def spawn_flag(self, x, y):
        sim_id = self.__get_id()
        return sim_id, Flag(sim_id, x, y)
    
    def spawn_effects(self, origin_entity, type):
        sim_id = self.__get_id()
        return sim_id, getattr(origin_entity, type)(sim_id)
        