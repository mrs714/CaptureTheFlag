from simulation.entity import Entity
from math import sqrt
from simulation.simulation_consts import *

class Bullet(Entity):
    def __init__(self, x, y, dx, dy, damage, owner_id):
        super().__init__(x, y)
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

    def move(self, dx, dy):
        #Normalize the vector
        vec_norm = sqrt(dx**2 + dy**2)
        dx /= vec_norm
        dy /= vec_norm
        
        #Escalate the vector with the speed
        dx *= BULLET_SPEED
        dy *= BULLET_SPEED

        #Move the bullet
        self.__x += dx
        self.__y += dy