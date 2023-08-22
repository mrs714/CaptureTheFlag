from simulation.entity import Entity
from math import sqrt
from simulation.simulation_consts import *
from simulation.player_context.bullet_info import BulletInfo

class Bullet(Entity):
    def __init__(self, sim_id, x, y, dx, dy, damage, type, owner_id):
        super().__init__(sim_id, x, y)
        self.__damage = damage
        self.__owner_id = owner_id
        self.__to_remove = False

        #Normalize the vector
        vec_norm = sqrt(dx**2 + dy**2)
        dx /= vec_norm
        dy /= vec_norm

        #Normalized direction
        self.__dx = dx
        self.__dy = dy

        self.__type = type
    
    def get_owner_id(self):
        return self.__owner_id

    def move(self):        
        #Escalate the vector with the speed
        dx = self.__dx * BULLET_SPEED
        dy = self.__dy * BULLET_SPEED

        #Move the bullet
        self.__x__ += dx
        self.__y__ += dy

        #If outside the map, mark it for removal
        if self.__keep_bullet_within_map():
            self.__to_remove = True


    def __keep_bullet_within_map(self):
        remove = False
        if self.__x__ < MAP_PADDING + BULLET_RADIUS:
            self.__x__ = MAP_PADDING + BULLET_RADIUS
            remove = True
        elif self.__x__ > MAP_WIDTH + MAP_PADDING - BULLET_RADIUS:
            self.__x__ = MAP_WIDTH + MAP_PADDING - BULLET_RADIUS
            remove = True
        if self.__y__ < MAP_PADDING + BULLET_RADIUS:
            self.__y__ = MAP_PADDING + BULLET_RADIUS
            remove = True
        elif self.__y__ > MAP_HEIGHT + MAP_PADDING - BULLET_RADIUS:
            self.__y__ = MAP_HEIGHT + MAP_PADDING - BULLET_RADIUS
            remove = True
        return remove
    
    def get_info(self):
        return BulletInfo(self.id(), self.__relative_x__, self.__relative_y__, self.__dx, self.__dy, self.__damage, self.__type, self.__owner_id)
    
    def to_remove(self):
        return self.__to_remove
    
    def get_type(self):
        return self.__type