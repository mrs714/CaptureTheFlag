from simulation.entity import Entity
from math import sqrt
from simulation.simulation_consts import *
from simulation.player_context.bullet_info import BulletInfo

class Bullet(Entity):
    def __init__(self, sim_id, x, y, dx, dy, damage, owner_id):
        super().__init__(sim_id, x, y)
        self.__damage = damage
        self.__owner_id = owner_id

        #Normalize the vector
        vec_norm = sqrt(dx**2 + dy**2)
        dx /= vec_norm
        dy /= vec_norm

        #Normalized direction
        self.__dx = dx
        self.__dy = dy
    
    def get_owner_id(self):
        return self.__owner_id

    def move(self):        
        #Escalate the vector with the speed
        dx = self.__dx * BULLET_SPEED
        dy = self.__dy * BULLET_SPEED

        #Move the bullet
        self.__x__ += dx
        self.__y__ += dy

    def check_map_bounds(self):
        if self.__x__ < MAP_PADDING or self.__x__ > MAP_WIDTH + MAP_PADDING:
            return True
        if self.__y__ < MAP_PADDING or self.__y__ > MAP_HEIGHT + MAP_PADDING:
            return True
        return False
    
    def get_info(self):
        return BulletInfo(self.id(), self.__x__, self.__y__, self.__dx, self.__dy, self.__damage, self.__owner_id)