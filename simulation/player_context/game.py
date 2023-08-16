from simulation.player_context.actions import Actions

entity_keys = ["bots", "bullets"]

class Game:
    def __init__(self, bot, entities, actions, tick):
        self.entities = {key: {key_id: ent.get_info() for key_id, ent in value.items() if key_id != bot.id()} for key, value in entities.items() if key in entity_keys}
        self.entities["me"] = bot.get_info()
        self.actions = Actions(*actions)
        self.tick = tick
    
    def debug(self, *args):
        print(*args)
