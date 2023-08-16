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
from RestrictedPython import compile_restricted_exec, safe_globals #import safe_builtins (for executing the bot code)
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem #import default_guarded_getiter (for executing the bot code)
from RestrictedPython.Guards import guarded_iter_unpack_sequence, safer_getattr, full_write_guard
from io import StringIO #import StringIO (for capturing the bot output)
import sys #import sys
import traceback #import traceback (for printing the bot errors)
from simulation.player_context.game import Game

class Simulation:

    def __init__(self, logger):
        
        self.__logger = logger

        self.__logger.debug("Initializing pygame...")
        pygame.init()
        self.__logger.debug("Pygame initialized")
        
        self.__logger.debug("Creating the screen...")
        self.__screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT), pygame.NOFRAME)
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
        
        return move, shoot

    def __execute_bot_code(self, bot, bots_to_remove):

        game = Game(bot, self.__entities, self.__generate_actions(bot), self.__current_tick)
        
        player_globals = safe_globals.copy()
        player_globals["game"] = game
        player_globals["__metaclass__"] = type
        player_globals["__name__"] = "simulation_sandbox"
        player_globals["_getiter_"] = default_guarded_getiter
        player_globals["_getitem_"] = default_guarded_getitem
        player_globals["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
        player_globals["_write_"] = full_write_guard
        #player_globals["_getattr_"] = safer_getattr

        temp_out = StringIO()
        sys.stdout = temp_out
        sys.stderr = temp_out

        filename = "<user_string>"

        bot_code_compiled = compile_restricted_exec(bot.code(), filename=filename)

        try:
            if bot_code_compiled.errors:
                for error in bot_code_compiled.errors:
                    temp_out.write(error)
                self.__logger.warning(f"Error while compiling the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {bot_code_compiled.errors}")
            else:
                exec(bot_code_compiled.code, player_globals, {}) #execute the bot code
        except:
            self.__logger.warning(f"Error while executing the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {traceback.format_exc()}")
            cl, exc, tb = sys.exc_info() #cl: class, exc: exception, tb: traceback
            tb2 = traceback.extract_tb(tb)
            for i in range(len(tb2)-1, -1, -1): #iterate through the traceback in reverse order
                if tb2[i].filename == filename: #get the last traceback frame that is in the user code
                    break
            temp_out.write(f"Line {tb2[i].lineno}: {cl.__name__}: {exc}")
            
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


    def get_entities(self):
        return self.__entities



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