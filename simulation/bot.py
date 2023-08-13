from simulation.entity import Entity
from simulation.bullet import Bullet
from math import sqrt
from simulation.simulation_consts import *

class Bot(Entity):
    def __init__(self, sim_id, db_id, name, x, y, code, health, shield, attack):
        super().__init__(sim_id, x, y)
        self.__code = code
        self.__health = health
        self.__attack = attack
        self.__shield = shield
        self.__db_id = db_id
        self.__name = name
        self.__exec_events = [] #List of strings captured from stdout and stderr
        self.__last_shot = 0 #Last time the bot shot a bullet in ticks

    def shoot(self, actual_tick):
        if actual_tick - self.__last_shot >= BOT_SHOOT_COOLDOWN:
            self.__last_shot = actual_tick
            return True
        return False
        

    def get_db_id(self):
        return self.__db_id
    
    def get_name(self):
        return self.__name
    
    def add_event(self, event):
        self.__exec_events.append(event)
    
    def move(self, dx, dy):
        #Normalize the vector
        vec_norm = sqrt(dx**2 + dy**2)
        dx /= vec_norm
        dy /= vec_norm
        
        #Escalate the vector with the speed
        dx *= BOT_SPEED
        dy *= BOT_SPEED

        #Move the bot
        self.__x__ += dx
        self.__y__ += dy
    
    def code(self):
        return self.__code