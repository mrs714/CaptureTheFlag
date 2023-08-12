import log

class Entity:
    def __init__(self, sim_id, x, y):
        self.__sim_id = sim_id
        self.__x = x
        self.__y = y
    
    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
    
    def pos(self):
        return self.__x, self.__y

    def dx(self):
        return self.__dx
    
    def dy(self):
        return self.__dy
    
    def dir(self):
        return self.__dx, self.__dy