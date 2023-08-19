from simulation.entity import Entity
from simulation.bullet import Bullet
from math import sqrt
from simulation.simulation_consts import *
from simulation.player_context.bot_info import BotInfo

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
        self.__last_actions = {"shoot": 0, "move": 0, "melee": 0, "dash": 0, "super_shot": 0, "super_melee": 0} #Last time the bot took an action

    def shoot(self, actual_tick):
        if actual_tick - self.__last_actions["shoot"] >= BOT_SHOOT_COOLDOWN:
            self.__last_actions["shoot"] = actual_tick
            return True
        return False
    
    def melee(self, actual_tick):
        if actual_tick - self.__last_actions["melee"] >= BOT_MELEE_COOLDOWN:
            self.__last_actions["melee"] = actual_tick
            return True
        return False

    def super_shot(self, actual_tick):
        if actual_tick - self.__last_actions["super_shot"] >= BOT_SUPER_SHOT_COOLDOWN:
            self.__last_actions["super_shot"] = actual_tick
            return True
        return False
    
    def super_melee(self, actual_tick):
        if actual_tick - self.__last_actions["super_melee"] >= BOT_SUPER_MELEE_COOLDOWN:
            self.__last_actions["super_melee"] = actual_tick
            return True
        return False
    
    def receive_life_damage(self, damage):
        self.__health -= damage
        if self.__health <= 0:
            self.__health = 0
        return self.__health
    
    def receive_shield_damage(self, damage):
        self.__shield -= damage
        if self.__shield <= 0:
            self.receive_life_damage(-self.__shield)
            self.__shield = 0
        return self.__health
    
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

        #Keep the bot inside the map
        self.keep_bot_within_map()

    def dash(self, dx, dy, actual_tick):
        if actual_tick - self.__last_actions["dash"] < BOT_DASH_COOLDOWN:
            return
        self.__last_actions["dash"] = actual_tick

        #Normalize the vector
        vec_norm = sqrt(dx**2 + dy**2)
        dx /= vec_norm
        dy /= vec_norm

        #Escalate the vector (to simulate a teleport, the speed is multiplied by 100)
        dx *= BOT_SPEED * 100
        dy *= BOT_SPEED * 100

        #Move the bot
        self.__x__ += dx
        self.__y__ += dy

        #Keep the bot inside the map 
        self.keep_bot_within_map()

    def keep_bot_within_map(self):
        if self.__x__ < MAP_PADDING + BOT_RADIUS:
            self.__x__ = MAP_PADDING + BOT_RADIUS
        elif self.__x__ > MAP_WIDTH + MAP_PADDING - BOT_RADIUS:
            self.__x__ = MAP_WIDTH + MAP_PADDING - BOT_RADIUS
        if self.__y__ < MAP_PADDING + BOT_RADIUS:
            self.__y__ = MAP_PADDING + BOT_RADIUS
        elif self.__y__ > MAP_HEIGHT + MAP_PADDING - BOT_RADIUS:
            self.__y__ = MAP_HEIGHT + MAP_PADDING - BOT_RADIUS
         
    def code(self):
        return self.__code

    def get_info(self):
        return BotInfo(self.id(), self.__x__, self.__y__, self.__health, self.__shield, self.__attack)