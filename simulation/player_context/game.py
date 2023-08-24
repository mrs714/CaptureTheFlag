from simulation.player_context.actions import Actions
from simulation.player_context.functions import Functions

entity_keys = ["bots", "bullets", "drops_points", "drops_health", "drops_shield"]

class Game:
    def __init__(self, bot, entities, actions, tick, functions):
        self.entities = {key: {key_id: ent.get_info() for key_id, ent in value.items() if key_id != bot.id()} for key, value in entities.items() if key in entity_keys}
        self.entities["me"] = bot.get_info()
        self.actions = Actions(*actions)
        self.tick = tick
        self.functions = Functions(*functions) # get_data, save_data, print, vector_to, vector_from_to, unit_vector, vector_length, get_bots_in_range_melee, nearest_object, get_objects_in_range
    
    def debug(self, *args):
        print(*args)  
