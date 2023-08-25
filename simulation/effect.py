from simulation.entity import Entity
from simulation.simulation_consts import *

class Effect(Entity):
    # Represents a visual effect, like a bullet explosion, player death, etc.

    def __init__(self, sim_id, x, y, type): # Type: "player_death", "drop_picked"
        super().__init__(sim_id, x, y)
        self.__type = type # points, health, shield
        self.__step = 0
        self.__to_remove = False

    def type(self):
        return self.__type

    def get_step(self):
        self.__step += 1
        return self.__step
    
    def to_remove(self):
        return self.__to_remove
    
    def remove(self):
        self.__to_remove = True
