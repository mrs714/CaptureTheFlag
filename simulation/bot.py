from simulation.entity import Entity

class Bot(Entity):
    def __init__(self, sim_id, db_id, name, x, y, code, health, shield, attack):
        super().__init__(sim_id, db_id, name, x, y)
        self.__code = code
        self.__health = health
        self.__attack = attack
        self.__shield = shield