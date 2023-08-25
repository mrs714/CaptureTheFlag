from simulation.entity import Entity
from simulation.simulation_consts import *
from simulation.player_context.drop_info import DropInfo

class Drop(Entity):

    def __init__(self, sim_id, x, y, type):
        super().__init__(sim_id, x, y)
        self.__type = type # points, health, shield
        self.__state = {"blinking": False, "color": None}

    def type(self):
        return self.__type
  
    def get_info(self):
        return DropInfo(self.id(), self.__x__, self.__y__, self.__type)
    
    def get_state(self):
        return self.__state
    
    def set_state(self, state):
        self.__state = state
