class ZoneInfo():
    def __init__(self, sim_id, x, y, contains_flag, bot):
        self.id = sim_id
        self.x = x
        self.y = y
        self.contains_flag = contains_flag
        self.owner_id = int(bot.id) if bot is not None else None