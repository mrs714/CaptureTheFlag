from simulation.simulation_consts import *
# Entities to spawn
from simulation.bot import Bot
from simulation.bullet import Bullet
from simulation.drop import Drop

import random as rnd

class Spawner():
    # Spawns different types of entity

    def __init__(self): # Type: "player_death", "drop_picked"
        self.__id_counter = 0

    def __get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def spawn_bot(self, bot, config):
        sim_id = self.__get_id()
        entity = Bot(sim_id, 
                bot["id"], 
                bot["username"], 
                rnd.randint(100, MAP_WIDTH - 100), # At least 50 inside the play-zone
                rnd.randint(100, MAP_HEIGHT - 100), 
                bot["code"], 
                config["health"], 
                config["shield"], 
                config["attack"])
        return sim_id, entity
    
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

    def spawn_effects(self, origin_entity, type):
        sim_id = self.__get_id()
        return sim_id, getattr(origin_entity, type)(sim_id)
        