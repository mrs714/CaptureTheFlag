from simulation.main_class.entity import Entity
from simulation.simulation_consts import *
from simulation.player_context.flag_info import FlagInfo

class Flag(Entity):
    def __init__(self, sim_id, x, y):
        super().__init__(sim_id, x, y)
        self.__held_by = None # Bot entity that holds the flag
        self.__in_zone = None # Zone entity that contains the flag
    
    def get_holder(self):
        return self.__held_by
    
    def set_holder(self, bot):
        self.__held_by = bot

    def get_zone(self):
        return self.__in_zone
    
    def set_zone(self, zone):
        self.__in_zone = zone

    def move(self):   
        # If the flag is held by a bot, move with it
        assert not (self.__held_by and self.__in_zone)
        if self.__held_by:
            self.__x__ = self.__held_by.x()
            self.__y__ = self.__held_by.y()
        if self.__in_zone:
            self.__x__ = self.__in_zone.x()
            self.__y__ = self.__in_zone.y()
    
    def get_info(self):
        return FlagInfo(self.id(), self.x(), self.y(), self.__held_by.id() if self.__held_by else None, self.__in_zone.id() if self.__in_zone else None)