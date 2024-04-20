from simulation.main_class.entity import Entity
from simulation.simulation_consts import *
from simulation.player_context.zone_info import ZoneInfo
from simulation.objects.flag import Flag

class Zone(Entity):

    def __init__(self, sim_id, x, y, bot):
        super().__init__(sim_id, x, y)
        self.__bot = bot
        self.__contains_flag = None # Flag entity

    def get_owner(self):
        return self.__bot

    def get_info(self):
        return ZoneInfo(self.id(), self.__x__, self.__y__, self.__contains_flag, self.__bot)
    
    def get_contains_flag(self):
        return self.__contains_flag
    
    def set_contains_flag(self, flag: Flag):
        self.__contains_flag = flag