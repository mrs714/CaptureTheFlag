from simulation.entity import Entity
from simulation.effect import Effect
from math import sqrt
from simulation.simulation_consts import *
from simulation.player_context.bot_info import BotInfo
from numpy import clip

class Bot(Entity):
    def __init__(self, sim_id, db_id, name, x, y, code, health, shield, attack):
        super().__init__(sim_id, x, y)
        self.__code = code
        self.__life = health # Bot attributes (changes)
        self.__defense = shield
        self.__health = health # Config (doesn't change)
        self.__shield = shield # Config
        self.__attack = MELEE_DAMAGE * attack / 100 # Percentage applied
        self.__db_id = db_id
        self.__name = name
        self.__exec_events = [] #List of strings captured from stdout and stderr
        self.__last_position = None #Last position of the bot (-1 if the bot code raised an exception)
        self.__last_actions = {"shoot": 0, "move": 0, "melee": 0, "dash": 0, "super_shot": 0, "super_melee": 0} #Last time the bot took an action
        self.__state = {"last_hit": -1} # Dictionary with the state of the bot, shooting, being shot, etc
        self.__points = 0 # Points earned by the bot

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
    
    def receive_life_damage(self, damage): # Returns wether the player is dead
        self.__life = clip(self.__life - damage, 0, self.__health)
        return self.__life == 0
    
    def recieve_life(self, life_points):
        self.__life = clip(self.__life + life_points, 0, self.__health)
    
    # To use on all attacks that might deal damage to shield, no matter if the shield is up or not
    # Returns wether the player is dead
    def receive_shield_damage(self, damage): 
        self.__defense -= damage
        if self.__defense <= 0:
            damage = -self.__defense
            self.__defense = 0
            return self.receive_life_damage(damage)
        return False
    
    def recieve_shield_damage_extra(self, damage):
        self.__defense -= damage * 2
        if self.__defense <= 0:
            damage = -self.__defense // 2
            self.__defense = 0
            return self.receive_life_damage(damage)
        return False
    
    def recieve_shield(self, shield_points):
        if self.__defense == 0:
            self.__defense == 1
        else:
            self.__defense = clip(self.__defense + shield_points, 0, self.__shield)
    
    def get_drop(self, type):
        if type == "health":
            self.recieve_life(HEALTH_PER_DROP)
        
        elif type == "shield":
            self.recieve_shield(SHIELD_PER_DROP)
        elif type == "points":
            self.__points += POINTS_PER_DROP
    
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
    
    def get_points(self):
        return self.__points
    
    def add_points(self, points):
        self.__points += points

    def get_life(self):
        return self.__life
    
    def get_health(self):
        return self.__health
    
    def get_defense(self):
        return self.__defense
        
    def get_shield(self):
        return self.__shield
    
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
    
    def death_effect(self, id):
        return Effect(id, self.__x__, self.__y__, "player_death")
         
    def code(self):
        return self.__code
    
    def get_state(self):
        return self.__state
    
    def update_state(self, state):
        self.__state = state

    def update_bot(self, ticks):
        if self.__defense > 0 and ticks % (FPS // 5) == 0 and (ticks - self.__state["last_hit"]) > (FPS * SECONDS_TO_REGAIN_SHIELD): # If bot has shield, regain 5 shield points per second, but only if it hasn't been hit in the last 2 seconds
            self.recieve_shield(1)

    def hit(self, ticks):
        self.__state["last_hit"] = ticks

    def get_info(self):
        return BotInfo(self.id(), self.__x__, self.__y__, self.__health, self.__shield, self.__attack)