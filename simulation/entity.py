from simulation.simulation_consts import MAP_PADDING

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
    
    def relative_x(self):
        return self.__x__ - MAP_PADDING

    def relative_y(self):
        return self.__y__ - MAP_PADDING
    
    def relative_position(self):
        return self.__x__ - MAP_PADDING, self.__y__ - MAP_PADDING