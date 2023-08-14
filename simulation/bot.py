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
        self.__last_position = None #Last position of the bot (-1 if the bot code raised an exception)
        self.__last_actions = {"shoot": 0, "move": 0} #Last time the bot shot a bullet in ticks

    def shoot(self, actual_tick):
        if actual_tick - self.__last_actions["shoot"] >= BOT_SHOOT_COOLDOWN:
            self.__last_actions["shoot"] = actual_tick
            return True
        return False
    
    def set_last_position(self, pos):
        self.__last_position = pos
    
    def get_last_position(self):
        return self.__last_position
    
    def get_events(self):
        return "\n".join(self.__exec_events) + "\n"

    def get_db_id(self):
        return self.__db_id
    
    def get_name(self):
        return self.__name
    
    def add_event(self, event):
        self.__exec_events.append(event)
    
    def move(self, dx, dy, actual_tick):
        if actual_tick - self.__last_actions["move"] < BOT_MOVE_COOLDOWN:
            return
        self.__last_actions["move"] = actual_tick
        
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

