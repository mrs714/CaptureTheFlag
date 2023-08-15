from simulation.simulation_consts import * #import all the constants
import pygame #import pygame
from datetime import datetime #import datetime (to get the current date and time)
import numpy as np #import numpy
from moviepy.editor import ImageSequenceClip #import ImageSequenceClip (for saving the mp4 file)
from random import randint #import randint (for generating random numbers)
import database.db_access as db #import db_access (for accessing the database)
from simulation.bot import Bot #import Bot
from simulation.bullet import Bullet #import Bullet
import json #import json (for parsing the bot config)
from RestrictedPython import safe_builtins, compile_restricted #import safe_builtins (for executing the bot code)
from io import StringIO #import StringIO (for capturing the bot output)
import sys #import sys


class Simulation:

    def __init__(self, logger):
        
        self.__logger = logger

        self.__logger.debug("Initializing pygame...")
        pygame.init()
        self.__logger.debug("Pygame initialized")
        
        self.__logger.debug("Creating the screen...")
        self.__screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.__logger.debug("Screen created")

        self.__logger.debug("Initializing simulation object variables...")
        self.__clock = pygame.time.Clock()
        self.__current_tick = 0
        self.__frames = []
        self.__id_counter = 0
        self.__entities = {
            "bots": {},
            "dead_bots": {},
            "bullets": {}
        }
        self.__logger.debug("Simulation object variables initialized")
    
    def get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def run(self):

        self.__logger.debug("Preparing to run the simulation...")
        list_of_bots = db.get_bots_to_execute()
        for bot in list_of_bots:
            config = json.loads(bot["config"])
            sim_id = self.get_id()
            self.__entities["bots"][sim_id] = Bot(sim_id, 
                                                  bot["id"], 
                                                  bot["username"], 
                                                  randint(100, 900), 
                                                  randint(100, 900), 
                                                  bot["code"], 
                                                  config["health"], 
                                                  config["shield"], 
                                                  config["attack"])
        self.__logger.debug("Simulation prepared")

        self.__logger.debug("Running the simulation loop...")
        running = True
        while self.__current_tick < DURATION and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.__perform_actions()
            self.__update_frame()
            pygame.display.flip()

            self.__save_frame()

            self.__current_tick += 1
            self.__clock.tick(FPS)

        pygame.quit()
        self.__logger.debug("Simulation loop finished")

        self.__logger.debug("Performing post-simulation tasks...")

        all_bots = [val for d in (self.__entities["bots"], self.__entities["dead_bots"]) for val in d.values()]
        for bot in all_bots:
            db.update_info(bot.get_db_id(), bot.get_last_position(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bot.get_events(), 0 if bot.get_last_position() == -1 else 1)

        self.__logger.debug("Post-simulation tasks performed")

##########################################################################################




    def __generate_actions(self, bot):
        def move(dx, dy):
            bot.move(dx, dy, self.__current_tick)
        
        def shoot(dx, dy):
            if bot.shoot(self.__current_tick):
                sim_id = self.get_id()
                self.__entities["bullets"][sim_id] = Bullet(sim_id, 
                                                            bot.x(), 
                                                            bot.y(), 
                                                            dx, 
                                                            dy, 
                                                            BULLET_DAMAGE,
                                                            bot.id())
        def debug(msg):
            print(msg)

        return move, shoot, debug

    def __execute_bot_code(self, bot, bots_to_remove):

        move, shoot, debug = self.__generate_actions(bot) #for the context enviroment
        context = {
            "__builtins__": safe_builtins,
            "move": move,
            "shoot": shoot,
            "debug": debug
        }

        temp_out = StringIO()
        sys.stdout = temp_out
        sys.stderr = temp_out

        try:
            bot_code = compile_restricted(bot.code(), '<string>', 'exec')
            exec(bot_code, context, {}) #execute the bot code
        except Exception as e:
            self.__logger.warning(f"Error while executing the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {e}")
            #traceback.print_exc() #too much info
            print(e)
            bot.set_last_position(-1)
            bots_to_remove.append(bot.id())
        finally:
            event = temp_out.getvalue()
            if event != "":
                bot.add_event(event)
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            temp_out.close()




##########################################################################################






    def __perform_actions(self):
        bots_to_remove = []
        for bot in self.__entities["bots"].values():
            self.__execute_bot_code(bot, bots_to_remove)
        
        for bot_id in bots_to_remove:
            db_bot = self.__entities["bots"][bot_id].get_db_id()
            self.__entities["dead_bots"][bot_id] = self.__entities["bots"].pop(bot_id)
            self.__logger.debug(f"Bot with db_id = {db_bot} removed")

        for bullet in self.__entities["bullets"].values():
            bullet.move()
    
    def __update_frame(self):
        self.__screen.fill(BACKGROUND_COLOR)
        for bot in self.__entities["bots"].values():
            pygame.draw.circle(self.__screen, BOT_COLOR, bot.pos(), BOT_RADIUS)
        for bullet in self.__entities["bullets"].values():
            pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
    
    def __save_frame(self):
        frame = pygame.surfarray.array3d(self.__screen)
        
        frame = np.rot90(frame, k=-1)
        frame = np.fliplr(frame)

        self.__frames.append(frame)
    
    def save_replay(self):

        self.__logger.debug("Saving the mp4 file...")
        video_clip = ImageSequenceClip(self.__frames, fps=FPS)
        video_clip.write_videofile(SIM_MP4_NAME, fps=FPS)
        self.__logger.debug("Mp4 file saved")

        self.__logger.debug("Saving the simulation info file...")
        with open(SIM_INFO_NAME, "w") as f:
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.__logger.debug("Simulation info file saved")