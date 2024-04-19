class BotInfo:
    def __init__(self, sim_id, x, y, health, shield, attack, carrying_flag_id=None):
        self.id = sim_id
        self.x = x
        self.y = y
        self.health = health
        self.shield = shield
        self.attack = attack
        self.carrying_flag_id = carrying_flag_id