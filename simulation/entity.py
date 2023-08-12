class Entity:
    def __init__(self, sim_id, db_id, name, x, y):
        self.__sim_id = sim_id
        self.__db_id = db_id
        self.__name = name
        self.__x = x
        self.__y = y
    
    def x(self):
        return self.__x
    
    def y(self):
        return self.__y
