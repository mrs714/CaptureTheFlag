import log

class Entity:
    def __init__(self, sim_id, x, y):
        self.__sim_id = sim_id
        self.__x__ = x
        self.__y__ = y
    
    def id(self):
        return self.__sim_id

    def x(self):
        return self.__x__
    
    def y(self):
        return self.__y__
    
    def pos(self):
        return self.__x__, self.__y__

    def dx(self):
        return self.__dx
    
    def dy(self):
        return self.__dy
    
    def dir(self):
        return self.__dx, self.__dy