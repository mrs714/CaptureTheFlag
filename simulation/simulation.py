from simulation.simulation_consts import * #import all the constants
import pygame #import pygame
from datetime import datetime #import datetime (to get the current date and time)
import numpy as np #import numpy
from moviepy.editor import ImageSequenceClip #import ImageSequenceClip (for saving the mp4 file)
from random import randint #import randint (for generating random numbers)
import log #import log (for logging into files)
import database.db_access as db #import db_access (for accessing the database)
from simulation.bot import Bot #import Bot
from simulation.bullet import Bullet #import Bullet
import json #import json (for parsing the bot config)
from RestrictedPython import compile_restricted, safe_builtins #import compile_restricted and safe_builtins (for executing the bot code)
from io import StringIO #import StringIO (for capturing the bot output)
import sys #import sys
import traceback #import traceback (for printing the traceback in case of an error)

class Simulation:

    def __init__(self):
        log.d("Initializing pygame...")
        pygame.init()
        log.d("Pygame initialized")
        
        log.d("Creating the screen...")
        self.__screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        log.d("Screen created")

        log.d("Initializing simulation object variables...")
        self.__clock = pygame.time.Clock()
        self.__current_tick = 0
        self.__frames = []
        self.__id_counter = 0
        self.__entities = {
            "bots": {},
            "dead_bots": {},
            "bullets": {}
        }
        log.d("Simulation object variables initialized")
    
    def get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def run(self):

        log.d("Preparing to run the simulation...")
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
        log.d("Simulation prepared")

        log.d("Running the simulation loop...")
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
        log.d("Simulation loop finished")

    


##########################################################################################




    def __generate_actions(self, bot):
        def move(dx, dy):
            bot.move(dx, dy)
        
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


        #TODO: se puede mover varias veces wtf



        move, shoot = self.__generate_actions(bot) #for the context enviroment
        context = {
            "__builtins__": safe_builtins,
            "move": move,
            "shoot": shoot
        }

        temp_out = StringIO()
        sys.stdout = temp_out
        sys.stderr = temp_out

        try:
            #bot_code = compile_restricted(bot.code(), '<string>', 'exec')
            print('prueba')
            exec(bot.code(), context, {}) #execute the bot code
        except Exception as e:
            log.i(f"Error while executing the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {e}")
            traceback.print_exc()
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
            log.d(f"Bot with db_id = {db_bot} removed")

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

        log.d("Saving the mp4 file...")
        video_clip = ImageSequenceClip(self.__frames, fps=FPS)
        video_clip.write_videofile(SIM_MP4_NAME, fps=FPS)
        log.d("Mp4 file saved")

        log.d("Saving the simulation info file...")
        with open(SIM_INFO_NAME, "w") as f:
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        log.d("Simulation info file saved")