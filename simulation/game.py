class Game:

    def __init__(self, bot, entities):
        self.move, self.shoot = self.__generate_actions(bot)
        
    def move(self, dx, dy):
        pass
    
    def shoot(self, dx, dy):
        pass


    def __generate_actions(self, bot):
        def move(self, dx, dy):
            bot.move(dx, dy)
        
        def shoot(self, dx, dy):
            if bot.shoot(self.__current_tick):
                sim_id = self.get_id()
                self.__entities["bullets"][sim_id] = Bullet(sim_id, 
                                                            bot.x(), 
                                                            bot.y(), 
                                                            dx, 
                                                            dy, 
                                                            BULLET_DAMAGE,
                                                            bot.id())

        return move, shoot