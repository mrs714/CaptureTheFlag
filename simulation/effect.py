from simulation.entity import Entity
from simulation.simulation_consts import *

class Effect(Entity):
    # Represents a visual effect, like a bullet explosion, player death, etc.

    def __init__(self, sim_id, x, y, type): # Type: "player_death", "drop_picked"
        super().__init__(sim_id, x, y)
        self.__type = type # points, health, shield
        self.__state = {"effect_step": 0}

    def type(self):
        return self.__type

    def get_state(self):
        return self.__state
    
    def set_state(self, state):
        self.__state = state
